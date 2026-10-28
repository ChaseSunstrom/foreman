"""T-1846: fmshade runs a GLSL ES fragment-shader subset per pixel on the CPU, so a shader card previews offline."""
import glob
import os
from unittest import mock

from helpers import PLUGIN, ForemanTestCase

import fmimg
import fmshade

CARDS = sorted(glob.glob(os.path.join(PLUGIN, "skills", "library", "cards", "looks", "shader-*.md")))
XS = (32, 96, 159, 223)  # uv.x 0.125, 0.375, 0.625, 0.875 at 4 px wide, as round(x * 255)


def pixels(rgb):
    return [tuple(rgb[i:i + 3]) for i in range(0, len(rgb), 3)]


def pcg(v):  # the shader cards' integer hash, written out in plain Python as the reference
    s = (v * 747796405 + 2891336453) & 0xFFFFFFFF
    w = (((s >> ((s >> 28) + 4)) ^ s) * 277803737) & 0xFFFFFFFF
    return ((w >> 22) ^ w) & 0xFFFFFFFF


class Shade(ForemanTestCase):
    def test_uv_gradient_matches_hand_computed_pixels_rows_top_down(self):
        rgb, _ = fmshade.render("#version 300 es\nprecision highp float;\nin vec2 vUv;\nout vec4 outColor;\n"
                                "void main() { outColor = vec4(vUv, 0.25, 1.0); }", 4, 2)
        self.assertEqual(pixels(rgb), [(x, 191, 64) for x in XS] + [(x, 64, 64) for x in XS])

    def test_shadertoy_main_image_with_itime_iresolution_and_swizzles(self):
        src = "void mainImage(out vec4 c, in vec2 p) { vec2 uv = p / iResolution.xy;\n" \
              "  c = vec4(uv.yx, fract(iTime), 1.0).bgra; }"
        rgb, _ = fmshade.render(src, 4, 2, time=2.25)
        self.assertEqual(pixels(rgb), [(64, x, 191) for x in XS] + [(64, x, 64) for x in XS])

    def test_functions_overloads_loops_mat2_swizzle_writes_and_branches(self):
        src = """out vec4 o;
const float K = 0.5;
float f(float x) { return x * K; }
float f(vec2 v) { return v.x + v.y; }
void main() {
  float s = 0.0, a = 1.0;
  for (int i = 0; i < 3; i++) { s += a; a *= 0.5; }
  vec2 r = mat2(0.0, 1.0, -1.0, 0.0) * vec2(1.0, 0.0);
  vec3 c = vec3(0.0);
  c.x = f(s) - 0.5;
  c.yz = r.yx * 0.5;
  c.z = s > 1.0 ? 0.25 : 1.0;
  if (f(r) > 2.0) c = vec3(1.0); else c.z += 0.125;
  o = vec4(c, 1.0);
}"""
        rgb, _ = fmshade.render(src, 2, 2)  # s 1.75; mat2 is column-major, so r is (0, 1); c (0.375, 0.5, 0.375)
        self.assertEqual(pixels(rgb), [(96, 128, 96)] * 4)

    def test_uint_wraps_and_int_bits_like_32_bit_hardware(self):
        src = """out vec4 o;
uint pcg(uint v) { uint s = v * 747796405u + 2891336453u; uint w = ((s >> ((s >> 28u) + 4u)) ^ s) * 277803737u;
  return (w >> 22u) ^ w; }
void main() {
  uint h = pcg(uint(gl_FragCoord.x));
  o = vec4(float(h & 255u) / 255.0, float((h >> 8u) & 255u) / 255.0, float(ivec2(-3, 4).x & 0xff) / 255.0, 1.0);
}"""
        rgb, _ = fmshade.render(src, 3, 1)
        self.assertEqual(pixels(rgb), [(pcg(x) & 255, pcg(x) >> 8 & 255, 253) for x in range(3)])

    def test_derivatives_come_from_the_2x2_quad_like_a_gpu(self):
        src = "in vec2 vUv;\nout vec4 o;\nvoid main() { o = vec4(dFdx(vUv.x) * 2.0, dFdy(vUv.y), fwidth(vUv.x), 1.0); }"
        rgb, _ = fmshade.render(src, 4, 2)  # a pixel is 0.25 of uv across and 0.5 up
        self.assertEqual(pixels(rgb), [(128, 128, 64)] * 8)

    def test_every_shader_card_renders(self):
        self.assertEqual(len(CARDS), 8)
        for card in CARDS:
            with self.subTest(card=os.path.basename(card)):
                src, first = fmshade.source(card)
                rgb, notes = fmshade.render(src, 8, 5, first_line=first)
                self.assertEqual((len(rgb), notes["undefined"]), (8 * 5 * 3, 0))
                self.assertGreater(len(set(rgb)), 1, "not one flat colour: the preview defaults show the look")

    def test_unset_uniforms_take_preview_defaults_and_set_overrides(self):
        src = "uniform vec3 uCol;\nuniform float uIntensity;\nout vec4 o;\nvoid main() { o = vec4(uCol * uIntensity, 1.0); }"
        rgb, notes = fmshade.render(src, 1, 1, {"uCol": [1, 0, 0.5]})
        self.assertEqual((pixels(rgb), notes["defaulted"]), ([(255, 0, 128)], ["uIntensity"]))
        with self.assertRaisesRegex(fmshade.ShadeError, r"uNope.*uCol, uIntensity"):
            fmshade.render(src, 1, 1, {"uNope": [1]})
        with self.assertRaisesRegex(fmshade.ShadeError, r"uCol is a vec3: 3 numbers"):
            fmshade.render(src, 1, 1, {"uCol": [1, 2]})

    def test_outside_the_subset_is_refused_naming_the_line(self):
        cases = {
            "#define N 3\nout vec4 o;\nvoid main() { o = vec4(1.0); }": r"^line 1: #define",
            "out vec4 o;\nuniform float t;\nvoid main() {\n  t = 1.0;\n  o = vec4(t);\n}": r"^line 4: t is read-only",
            "out vec4 o;\nuniform sampler2D tex;\nvoid main() { o = vec4(1.0); }": r"^line 2: sampler2D",
            "out vec4 o;\nvoid main() {\n  vec3 a = vec3(1.0);\n  o = vec4(a + vec2(1.0), 1.0);\n}": r"^line 4: vec3 \+ vec2",
            "out vec4 o;\nvoid main() {\n  for (int i = 0; i < 3; i++) { if (i == 1) continue; }\n  o = vec4(1.0);\n}":
                r"^line 3: continue",
            "out vec4 o;\nvoid main() {\n  o = vec4(nope(1.0));\n}": r"^line 3: nope\(\) is not declared",
            "out vec4 o;\nvoid main() { o = vec4(1e999); }": r"^line 2: 1e999",
            "out vec4 o;\nfloat f(float x) { return x; }": r"no main\(\)",
        }
        for src, said in cases.items():
            with self.subTest(said=said), self.assertRaisesRegex(fmshade.ShadeError, said):
                fmshade.render(src, 1, 1)
        with self.assertRaisesRegex(fmshade.ShadeError, r"^line 14: "):  # a card's lines count from the file's top
            fmshade.render("out vec4 o;\nvoid main() { o = vec4(nope); }", 1, 1, first_line=13)

    def test_hostile_input_stops_with_a_reason_not_a_hang_a_traceback_or_a_black_pixel(self):
        chain = "".join(f"float f{i}(float x) {{ return f{i - 1}(x) + f{i - 1}(x); }}\n" for i in range(1, 41))
        cases = {
            "precision highp float": r"ends early",
            "layout(location = 0": r"ends early",
            "out vec4 o;\n/* never closed\nvoid main() { o = vec4(1.0); }": r"^line 2: a /\* comment never ends",
            "out vec4 o;\nvoid main() {\n  float x = 0.0;\n  for (;;) x += 1.0;\n  o = vec4(x);\n}": r"^line 4: .*100000",
            "out vec4 o;\nfloat f0(float x) { return x; }\n" + chain + "void main() { o = vec4(f40(1.0)); }": r"100000",
            "in vec2 v;\nout vec4 o;\nvoid main() {\n  float x = 0.0;\n  for (int i = 0; i < 100; i++) "
            "x += dFdx(v.x);\n  o = vec4(x);\n}": r"^line 5: .*derivatives",
            "out vec4 o;\nvoid main() { o = vec4(" + "(" * 300 + "1.0" + ")" * 300 + "); }": r"too deep",
            "out vec4 o;\nvoid main() { o = vec4(" + " + ".join(["1.0"] * 300) + "); }": r"too deep",
            "out vec4 o;\nconst float k = 1.0 / 0.0;\nvoid main() { o = vec4(k); }": r"ZeroDivisionError",
        }
        for src, said in cases.items():
            with self.subTest(said=said), self.assertRaisesRegex(fmshade.ShadeError, said):
                fmshade.render(src, 2, 2)
        loop = "out vec4 o;\nvoid main() {\n  float x = 0.0;\n  for (int i = 0; i < 50; i++) x += 1.0;\n  o = vec4(x);\n}"
        with mock.patch.object(fmshade, "TOTAL", 1000), self.assertRaisesRegex(fmshade.ShadeError, r"1000 steps"):
            fmshade.render(loop, 8, 8)  # 50 a pixel is fine; 64 pixels of it is past the whole render's budget
        rgb, _ = fmshade.render("out vec4 o;\n/*\n#define X 1\n*/\nvoid main() { o = vec4(1.0); }", 1, 1)
        self.assertEqual(rgb, b"\xff\xff\xff")  # a # inside a comment is comment

    def test_derivatives_hold_at_odd_sizes_with_only_a_few_rows_kept(self):
        src = "in vec2 vUv;\nout vec4 o;\nvoid main() { o = vec4(dFdx(vUv.x) * 3.0, dFdy(vUv.y) * 3.0, 0.0, 1.0); }"
        rgb, _ = fmshade.render(src, 3, 3)  # every pixel, the top row's lone quad half too, differences one third
        self.assertEqual(pixels(rgb), [(255, 255, 0)] * 9)

    def test_cli_writes_the_png_and_rejects_bad_flags(self):
        png = os.path.join(self.tmp, "halftone.png")
        card = [c for c in CARDS if c.endswith("halftone.md")][0]
        r = self.fm("scene", "shade", card, "--size", "12x8", "--out", png)
        self.assertIn("12x8", r.stdout)
        self.assertEqual(fmimg.load(png)[:2], (12, 8))
        frag = os.path.join(self.tmp, "flat.frag")
        with open(frag, "w") as f:
            f.write("uniform vec3 uCol;\nout vec4 o;\nvoid main() { o = vec4(uCol, 1.0); }\n")
        self.fm("scene", "shade", frag, "--size", "2x1", "--set", "uCol=1,0,0.5", "--out", png)
        self.assertEqual(fmimg.load(png).rgba[:4], bytes((255, 0, 128, 255)))
        for flags, said in ((["--size", "0x8"], "WxH"), (["--set", "uNope=1"], "uNope"), (["--set", "uCol"], "NAME="),
                            (["--out", frag], "is FILE")):
            r = self.fm("scene", "shade", frag, "--out", png, *flags, check=False)
            self.assertEqual((r.returncode, said in r.stderr), (2, True), r.stderr)
        with open(frag) as f:
            self.assertIn("uCol", f.read())  # --out naming the shader itself never wrote over it
