"""T-1630: fm img, a stdlib PNG codec. Decode 8-bit (and 1/2/4-bit grey and palette) images with all five filters
into RGBA; encode RGB or RGBA with filter 0; diff two images into a changed-pixel count and a bounding box.
T-1631: fmraster, an integer rasteriser (edge functions, a z-buffer, flat shading): a lit cube, the same bytes always."""
import hashlib
import importlib.util
import json
import os
import random
import stat
import struct
import tracemalloc
import unittest
import zlib

from helpers import ForemanTestCase

import fmimg
import fmraster


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

    def test_idat_split_across_chunks(self):
        rows = [bytes(range(i, i + 12)) for i in range(3)]
        data = zlib.compress(filtered(rows, 4, (4, 1, 2)))
        parts = b"".join(chunk(b"IDAT", data[i:i + 7]) for i in range(0, len(data), 7))
        ihdr = struct.pack(">IIBBBBB", 3, 3, 8, 6, 0, 0, 0)
        im = fmimg.decode(fmimg.SIGNATURE + chunk(b"IHDR", ihdr) + parts + chunk(b"IEND", b""))
        self.assertEqual(im.rgba, b"".join(rows))

    def test_refuses_what_it_does_not_read(self):
        rows = [bytes(8)] * 2
        good = png(2, 2, 6, rows)
        plte = chunk(b"PLTE", bytes(9))  # three entries
        cases = [("interlaced", png(2, 2, 6, rows, interlace=1)),
                 ("16-bit", png(1, 2, 6, rows, depth=16)),
                 ("bad IHDR", png(1, 2, 3, rows, depth=16, extra=plte)),  # palettes stop at 8 bits
                 ("not a PNG", b"GIF89a" + bytes(40)),
                 ("CRC", good[:41] + bytes([good[41] ^ 1]) + good[42:]),  # a byte inside IDAT's data
                 ("truncated", good[:40]),
                 ("short", png(2, 3, 6, rows)),
                 ("too large", png(1 << 20, 1 << 20, 6, None, raw=b"")),
                 ("too large", png(fmimg.MAX_SIDE, fmimg.MAX_PIXELS // fmimg.MAX_SIDE + 1, 6, None, raw=b"")),
                 ("empty", png(0, 2, 6, None, raw=b"")),
                 ("filter", png(2, 2, 6, None, raw=b"\x05" + bytes(8) + b"\x00" + bytes(8))),
                 ("IHDR", fmimg.SIGNATURE + chunk(b"IEND", b"")),
                 ("critical", good.replace(chunk(b"IEND", b""), chunk(b"CgBI", b"") + chunk(b"IEND", b""))),
                 ("palette index past PLTE", png(2, 1, 3, [b"\x02\x03"], extra=plte)),
                 ("palette index past PLTE", png(4, 1, 3, [b"\x0c"], depth=2, extra=plte))]  # 0, 0, 3, 0
        for expect, data in cases:
            with self.subTest(expect):
                with self.assertRaises(ValueError) as e:
                    fmimg.decode(data)
                self.assertIn(expect, str(e.exception))

    def test_chunk_names_reach_the_terminal_escaped(self):
        # a chunk type is four bytes of the file's choosing: ESC [ 2 J clears the screen it is printed on
        good, iend = png(2, 2, 6, [bytes(8)] * 2), chunk(b"IEND", b"")
        evil = chunk(b"\x1b[2J", b"")
        cases = [good.replace(iend, evil + iend),  # an unknown critical chunk, its CRC right
                 good.replace(iend, evil[:-1] + bytes([evil[-1] ^ 1]) + iend),  # its CRC wrong
                 good[:33] + struct.pack(">I", 99) + b"\x1b[2J" + bytes(8)]  # running past the end
        for i, data in enumerate(cases):
            with self.subTest(i):
                with self.assertRaises(ValueError) as e:
                    fmimg.decode(data)
                self.assertNotIn("\x1b", str(e.exception))
                path = os.path.join(self.tmp, f"evil{i}.png")
                with open(path, "wb") as f:
                    f.write(data)
                p = self.fm("img", "diff", path, path, check=False)
                self.assertEqual(p.returncode, 2, p.stdout)
                self.assertNotIn("\x1b", p.stderr)
                self.assertIn("[2J", p.stderr)

    def test_inflate_is_capped_by_the_header(self):
        # a bomb: the header says 1x1, the stream inflates to 64 MB; decode stops at what the header allows
        bomb = zlib.compress(bytes(64 << 20), 9)
        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
        data = fmimg.SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"IDAT", bomb) + chunk(b"IEND", b"")
        tracemalloc.start()
        try:
            self.assertEqual(fmimg.decode(data).rgba, bytes(4))
            peak = tracemalloc.get_traced_memory()[1]
        finally:
            tracemalloc.stop()
        self.assertLess(peak, 8 << 20, "the whole stream was inflated")

    def test_diff_counts_changed_pixels_and_their_box(self):
        a = fmimg.decode(fmimg.encode(4, 4, rgba4x4()))
        self.assertEqual(fmimg.diff(a, a), {"changed": 0, "total": 16, "bbox": None})
        px = bytearray(a.rgba)
        for x, y in ((1, 1), (3, 2)):
            px[(y * 4 + x) * 4] ^= 1  # one channel, one bit
        b = fmimg.decode(fmimg.encode(4, 4, bytes(px)))
        self.assertEqual(fmimg.diff(a, b), {"changed": 2, "total": 16, "bbox": [1, 1, 4, 3]})
        d = fmimg.diff(a, b, image=True)  # one walk gives the count and the picture
        out = d.pop("image")
        self.assertEqual(d["changed"], 2)
        self.assertEqual(len(out), 64)
        self.assertEqual(out[(1 * 4 + 1) * 4:(1 * 4 + 1) * 4 + 4], bytes(fmimg.CHANGED))
        self.assertNotEqual(out[:4], bytes(fmimg.CHANGED))
        with self.assertRaises(ValueError):
            fmimg.diff(a, fmimg.decode(fmimg.encode(2, 2, bytes(16))))

    def test_diff_tolerance_and_transparent_pixels(self):
        a = fmimg.Image(3, 1, "rgba", 8, bytes([10, 10, 10, 255, 0, 0, 0, 0, 5, 5, 5, 255]))
        b = fmimg.Image(3, 1, "rgba", 8, bytes([13, 8, 10, 255, 255, 9, 1, 0, 5, 5, 5, 254]))
        self.assertEqual(fmimg.diff(a, b)["changed"], 2, "two alpha-0 pixels are equal whatever their RGB")
        self.assertEqual(fmimg.diff(a, b, tol=2), {"changed": 1, "total": 3, "bbox": [0, 0, 1, 1]})
        self.assertEqual(fmimg.diff(a, b, tol=3)["changed"], 0, "tol is the per-channel maximum difference")
        c = fmimg.Image(3, 1, "rgba", 8, bytes([10, 10, 10, 255, 0, 0, 0, 1, 5, 5, 5, 255]))
        self.assertEqual(fmimg.diff(a, c)["bbox"], [1, 0, 2, 1], "alpha 0 against alpha 1 differs")

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
        self.assertEqual(stat.S_IMODE(os.stat(c).st_mode), 0o600, "a copy of a screenshot stays private")
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
        out = os.path.join(self.tmp, "none.png")
        p = self.fm("img", "diff", a, c, "--out", out, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("sizes differ", p.stdout)
        self.assertIn("no diff image written", p.stdout)
        self.assertFalse(os.path.exists(out))
        fifo = os.path.join(self.tmp, "fifo.png")
        os.mkfifo(fifo)
        p = self.fm("img", "info", fifo, check=False)  # open() alone would wait for a writer forever
        self.assertEqual(p.returncode, 2)
        self.assertIn("not a regular file", p.stderr)

    def test_a_worker_of_fm_code_may_read_but_not_write(self):
        a, b, c = (os.path.join(self.tmp, n) for n in ("a.png", "b.png", "c.png"))
        fmimg.save(a, 1, 1, bytes(4))
        fmimg.save(b, 1, 1, b"\x01\x00\x00\xff")
        env = {"FOREMAN_WORKER_OF": "run-1"}
        self.assertIn("1x1 rgba", self.fm("img", "info", a, env=env).stdout)
        p = self.fm("img", "diff", a, b, env=env, check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        p = self.fm("img", "diff", a, b, "--out", c, env=env, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("refused", p.stderr)
        self.assertFalse(os.path.exists(c))


RED, GREEN = (255, 0, 0), (0, 255, 0)


def facing(z, colour=RED, half=5):
    """A triangle across the frame's middle at depth z, clockwise as the camera sees it (so its front faces it)."""
    return (-half, -half, z), (0, half, z), (half, -half, z), colour


def centre(rgb, w=8, h=8):
    i = (h // 2 * w + w // 2) * 3
    return tuple(rgb[i:i + 3])


class Cube(ForemanTestCase):
    # sha256 of the default 64x64 lit cube's RGB bytes: integers only, so this holds on every machine and Python
    GOLDEN = "7de0f1d8b428074210b6ae99fb6b5eb6e8247bd6322ba044fef9ec6adda326e4"

    def test_two_renders_are_byte_identical_pngs(self):
        a, b = (os.path.join(self.tmp, n) for n in ("a.png", "b.png"))
        fmraster.save(a, fmraster.cube(), 64, 64)
        fmraster.save(b, fmraster.cube(), 64, 64)
        with open(a, "rb") as f, open(b, "rb") as g:
            self.assertEqual(f.read(), g.read())
        rgb = fmraster.render(fmraster.cube(), 64, 64)
        self.assertEqual(hashlib.sha256(rgb).hexdigest(), self.GOLDEN)
        self.assertEqual(fmimg.load(a).rgba, b"".join(rgb[i:i + 3] + b"\xff" for i in range(0, len(rgb), 3)))

    def test_three_faces_take_three_flat_shades(self):
        rgb = fmraster.render(fmraster.cube(), 64, 64)
        shades = {rgb[i:i + 3] for i in range(0, len(rgb), 3)} - {b"\x00\x00\x00"}
        self.assertEqual(len(shades), 3, "three faces show, each one flat colour")
        self.assertLess(rgb.count(b"\x00\x00\x00"), 64 * 64 * 0.9, "the cube fills a fair part of the frame")

    def test_light_facing_gets_full_colour_and_away_gets_ambient(self):
        lit = fmraster.render([facing(10)], 8, 8, light=(0, 0, -1))
        self.assertEqual(centre(lit), RED)
        dark = fmraster.render([facing(10)], 8, 8, light=(0, 0, 1))
        self.assertEqual(centre(dark), (255 * fmraster.AMBIENT >> 8, 0, 0))

    def test_the_nearer_triangle_wins_whatever_the_order(self):
        near, far = facing(10, RED), facing(20, GREEN, half=20)
        for tris in ([near, far], [far, near]):
            self.assertEqual(centre(fmraster.render(tris, 8, 8, light=(0, 0, -1))), RED)

    def test_back_faces_and_the_near_plane_are_dropped(self):
        a, b, c, colour = facing(10)
        self.assertEqual(fmraster.render([(a, c, b, colour)], 8, 8), bytes(8 * 8 * 3), "a back face is culled")
        dot = (1, 1, 10)
        self.assertEqual(fmraster.render([(dot, dot, dot, colour)], 8, 8), bytes(8 * 8 * 3),
                         "a zero-area triangle has every edge function 0: its depth would divide by zero")
        self.assertEqual(fmraster.render([((-5, -5, 0), b, c, colour)], 8, 8), bytes(8 * 8 * 3),
                         "a vertex on the camera's plane would divide by zero")
        far = facing(10**6)
        self.assertEqual(fmraster.render([far], 8, 8), bytes(8 * 8 * 3), "too far to cover a pixel's centre")

    def test_only_integers_go_in(self):
        a, b, c, colour = facing(10)
        for bad in ([((-5.0, -5, 10), b, c, colour)], [(a, b, c, (255, 0))], [(a, b, c, (256, 0, 0))]):
            with self.subTest(bad=bad), self.assertRaises((TypeError, ValueError)):
                fmraster.render(bad, 8, 8)
        with self.assertRaises(ValueError):
            fmraster.render([], 0, 8)
        with self.assertRaises(ValueError):
            fmraster.render([], 1 << 12, 1 << 12)


if __name__ == "__main__":
    unittest.main()
