"""T-1630: fm img, a stdlib PNG codec. Decode 8-bit (and 1/2/4-bit grey and palette) images with all five filters
into RGBA; encode RGB or RGBA with filter 0; diff two images into a changed-pixel count and a bounding box."""
import importlib.util
import json
import os
import random
import struct
import unittest
import zlib

from helpers import ForemanTestCase

import fmimg


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def filtered(rows, bpp, kinds):
    """The forward filters, written apart from fmimg's inverse: row y gets filter kinds[y % len(kinds)]."""
    out, prev = b"", bytes(len(rows[0]))
    for y, row in enumerate(rows):
        k = kinds[y % len(kinds)]
        line = bytearray()
        for i, x in enumerate(row):
            a = row[i - bpp] if i >= bpp else 0
            b, c = prev[i], prev[i - bpp] if i >= bpp else 0
            line.append((x - (0, a, b, (a + b) // 2, paeth(a, b, c))[k]) & 255)
        out += bytes([k]) + bytes(line)
        prev = row
    return out


def png(w, h, colour, rows, depth=8, kinds=(0,), extra=b"", interlace=0, raw=None):
    """raw: the filtered scanlines as they are, in place of rows filtered by kinds."""
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colour]
    ihdr = struct.pack(">IIBBBBB", w, h, depth, colour, 0, 0, interlace)
    data = zlib.compress(raw if raw is not None else filtered(rows, max(1, channels * depth // 8), kinds))
    return fmimg.SIGNATURE + chunk(b"IHDR", ihdr) + extra + chunk(b"IDAT", data) + chunk(b"IEND", b"")


def rgba4x4(seed=1630):
    rnd = random.Random(seed)
    return bytes(rnd.randrange(256) for _ in range(4 * 4 * 4))


class Img(ForemanTestCase):
    def test_round_trip_keeps_the_pixels(self):
        px = rgba4x4()
        im = fmimg.decode(fmimg.encode(4, 4, px))
        self.assertEqual((im.width, im.height, im.mode, im.depth), (4, 4, "rgba", 8))
        self.assertEqual(im.rgba, px)
        rgb = bytes(b for i, b in enumerate(px) if i % 4 != 3)
        im = fmimg.decode(fmimg.encode(4, 4, rgb, mode="rgb"))
        self.assertEqual(im.mode, "rgb")
        self.assertEqual(im.rgba, bytes(b if i % 4 != 3 else 255 for i, b in enumerate(px)))
        with self.assertRaises(ValueError):
            fmimg.encode(4, 4, px[:-1])

    def test_every_filter_decodes(self):
        rnd = random.Random(5)
        rows = [bytes(rnd.randrange(256) for _ in range(5 * 4)) for _ in range(7)]
        for kinds in ((0,), (1,), (2,), (3,), (4,), (4, 3, 2, 1, 0)):
            with self.subTest(kinds=kinds):
                im = fmimg.decode(png(5, 7, 6, rows, kinds=kinds))
                self.assertEqual(im.rgba, b"".join(rows))
        rgb = [bytes(rnd.randrange(256) for _ in range(3 * 3)) for _ in range(4)]
        im = fmimg.decode(png(3, 4, 2, rgb, kinds=(4, 1, 3, 2)))
        self.assertEqual(im.rgba, b"".join(bytes(r[i:i + 3]) + b"\xff" for r in rgb for i in range(0, 9, 3)))

    def test_grey_grey_alpha_and_palette(self):
        im = fmimg.decode(png(2, 2, 0, [b"\x00\x80", b"\xff\x10"], kinds=(3,)))
        self.assertEqual((im.mode, im.rgba), ("grey", bytes([0, 0, 0, 255, 128, 128, 128, 255,
                                                              255, 255, 255, 255, 16, 16, 16, 255])))
        im = fmimg.decode(png(2, 1, 4, [b"\x40\x80\xc0\x00"], kinds=(1,)))
        self.assertEqual((im.mode, im.rgba), ("grey+alpha", bytes([64, 64, 64, 128, 192, 192, 192, 0])))
        plte = chunk(b"PLTE", bytes([255, 0, 0, 0, 255, 0, 0, 0, 255]))
        trns = chunk(b"tRNS", b"\x00\x80")  # entry 2 keeps 255: a short tRNS
        im = fmimg.decode(png(3, 1, 3, [b"\x02\x01\x00"], kinds=(4,), extra=plte + trns))
        self.assertEqual((im.mode, im.rgba), ("palette", bytes([0, 0, 255, 255, 0, 255, 0, 128, 255, 0, 0, 0])))
        # 2-bit palette: 5 pixels in two bytes, the last six bits padding
        im = fmimg.decode(png(5, 1, 3, [bytes([0b00011000, 0b01000000])], depth=2, extra=plte))
        self.assertEqual(im.rgba, bytes([255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255,
                                         0, 255, 0, 255]))
        im = fmimg.decode(png(3, 1, 0, [bytes([0b10100000])], depth=1))  # 1-bit grey scales to 0/255
        self.assertEqual(im.rgba[::4], bytes([255, 0, 255]))
        key = chunk(b"tRNS", b"\x00\x80")  # grey colour key: value 128 is transparent
        im = fmimg.decode(png(2, 1, 0, [b"\x80\x81"], extra=key))
        self.assertEqual(im.rgba[3::4], b"\x00\xff")
        key = chunk(b"tRNS", struct.pack(">HHH", 1, 2, 3))
        im = fmimg.decode(png(2, 1, 2, [b"\x01\x02\x03\x01\x02\x04"], extra=key))
        self.assertEqual(im.rgba[3::4], b"\x00\xff")

    def test_refuses_what_it_does_not_read(self):
        rows = [bytes(8)] * 2
        good = png(2, 2, 6, rows)
        cases = {"interlaced": png(2, 2, 6, rows, interlace=1),
                 "16-bit": png(1, 2, 6, rows, depth=16),
                 "not a PNG": b"GIF89a" + bytes(40),
                 "CRC": good[:41] + bytes([good[41] ^ 1]) + good[42:],  # a byte inside IDAT's data
                 "truncated": good[:40],
                 "short": png(2, 3, 6, rows),
                 "too large": png(1 << 20, 1 << 20, 6, None, raw=b""),
                 "filter": png(2, 2, 6, None, raw=b"\x05" + bytes(8) + b"\x00" + bytes(8)),
                 "IHDR": fmimg.SIGNATURE + chunk(b"IEND", b""),
                 "critical": good.replace(chunk(b"IEND", b""), chunk(b"CgBI", b"") + chunk(b"IEND", b""))}
        for name, data in cases.items():
            with self.subTest(name), self.assertRaises(ValueError) as e:
                fmimg.decode(data)
            self.assertIn(name, str(e.exception))

    def test_inflate_is_capped_by_the_header(self):
        # a bomb: the header says 1x1, the stream inflates to 64 MB; decode stops at what the header allows
        bomb = zlib.compress(bytes(64 << 20), 9)
        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
        data = fmimg.SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"IDAT", bomb) + chunk(b"IEND", b"")
        self.assertEqual(fmimg.decode(data).rgba, bytes(4))

    def test_diff_counts_changed_pixels_and_their_box(self):
        a = fmimg.decode(fmimg.encode(4, 4, rgba4x4()))
        self.assertEqual(fmimg.diff(a, a), {"changed": 0, "total": 16, "bbox": None})
        px = bytearray(a.rgba)
        for x, y in ((1, 1), (3, 2)):
            px[(y * 4 + x) * 4] ^= 1  # one channel, one bit
        b = fmimg.decode(fmimg.encode(4, 4, bytes(px)))
        self.assertEqual(fmimg.diff(a, b), {"changed": 2, "total": 16, "bbox": [1, 1, 4, 3]})
        out = fmimg.diff_image(a, b)
        self.assertEqual(len(out), 64)
        self.assertEqual(out[(1 * 4 + 1) * 4:(1 * 4 + 1) * 4 + 4], bytes(fmimg.CHANGED))
        self.assertNotEqual(out[:4], bytes(fmimg.CHANGED))
        with self.assertRaises(ValueError):
            fmimg.diff(a, fmimg.decode(fmimg.encode(2, 2, bytes(16))))

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow is an optional cross-check")
    def test_pillow_written_files_decode_the_same(self):
        from PIL import Image
        rnd = random.Random(9)
        w, h = 37, 23
        base = Image.frombytes("RGBA", (w, h), bytes(rnd.randrange(256) for _ in range(w * h * 4)))
        four = base.convert("RGB").quantize(4)  # optimize writes it 2-bit
        images = {m: base.convert(m) for m in ("RGBA", "RGB", "L", "LA", "P", "1")}
        images.update({"P4": four, "P4+tRNS": (four, {"transparency": 1})})
        for name, im in images.items():
            im, extra = im if isinstance(im, tuple) else (im, {})
            with self.subTest(name):
                path = os.path.join(self.tmp, f"{name}.png")
                im.save(path, optimize=True, **extra)  # Pillow's adaptive filters pick all five over these rows
                if extra:
                    im = Image.open(path)
                self.assertEqual(fmimg.load(path).rgba, im.convert("RGBA").tobytes())
        self.assertEqual(fmimg.info(os.path.join(self.tmp, "P4.png"))["depth"], 2)

    def test_fm_img_info_and_diff(self):
        a, b, c = (os.path.join(self.tmp, n) for n in ("a.png", "b.png", "c.png"))
        px = rgba4x4()
        fmimg.save(a, 4, 4, px)
        fmimg.save(b, 4, 4, bytes([px[0] ^ 255]) + px[1:])
        self.assertIn("4x4 rgba", self.fm("img", "info", a).stdout)
        self.assertEqual(self.fm_json("img", "info", a)["width"], 4)
        self.assertEqual(self.fm("img", "diff", a, a).returncode, 0)
        p = self.fm("img", "diff", a, b, "--out", c, check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("1 of 16 pixels changed", p.stdout)
        self.assertEqual(fmimg.load(c).rgba[:4], bytes(fmimg.CHANGED))
        d = json.loads(self.fm("img", "diff", a, b, "--json", check=False).stdout)
        self.assertEqual((d["changed"], d["bbox"]), (1, [0, 0, 1, 1]))
        p = self.fm("img", "diff", a, b, "--out", b, check=False)  # the baseline is never overwritten
        self.assertEqual((p.returncode, fmimg.load(b).rgba[1:]), (2, px[1:]), p.stderr)
        link, target = os.path.join(self.tmp, "link.png"), os.path.join(self.tmp, "target.txt")
        with open(target, "w") as f:
            f.write("keep")
        os.symlink(target, link)
        self.fm("img", "diff", a, b, "--out", link, check=False)  # the link is replaced, not written through
        self.assertEqual((open(target).read(), os.path.islink(link)), ("keep", False))
        with open(c, "wb") as f:
            f.write(b"not a png")
        p = self.fm("img", "info", c, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not a PNG", p.stderr)
        fmimg.save(c, 2, 2, bytes(16))
        p = self.fm("img", "diff", a, c, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("sizes differ", p.stdout)


if __name__ == "__main__":
    unittest.main()
