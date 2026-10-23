"""T-1530: 3D verification that needs no GPU: glTF files checked offline, and a soak of a compiled scene in headless
Chrome (SwiftShader) when a browser and a three.js build are here, skipped with the reason when they aren't."""
import base64
import glob
import json
import os
import pwd
import struct
import unittest

from helpers import ForemanTestCase

import fmscene
import fmshot

TRIANGLE = struct.pack("<9f", 0, 0, 0, 1, 0, 0, 0, 1, 0)  # three VEC3 floats: 36 bytes


def gltf(**over):
    doc = {"asset": {"version": "2.0"}, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}],
           "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
           "accessors": [{"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3"}],
           "bufferViews": [{"buffer": 0, "byteLength": 36}],
           "buffers": [{"byteLength": 36, "uri": "data:application/octet-stream;base64,"
                        + base64.b64encode(TRIANGLE).decode()}]}
    doc.update(over)
    return doc


def glb(doc, binary=TRIANGLE, length=None):
    text = json.dumps(doc).encode()
    text += b" " * (-len(text) % 4)
    body = struct.pack("<II", len(text), 0x4E4F534A) + text + struct.pack("<II", len(binary), 0x004E4942) + binary
    return struct.pack("<III", 0x46546C67, 2, length or 12 + len(body)) + body


def three():
    """A three.js build to soak with: FOREMAN_THREE, else one bun or a project installed, else None."""
    home = pwd.getpwuid(os.getuid()).pw_dir
    found = [os.environ.get("FOREMAN_THREE", "")] + sorted(glob.glob(os.path.join(
        home, ".bun", "install", "cache", "three@*", "build", "three.module.js"))) + sorted(glob.glob(os.path.join(
            home, "projects", "*", "*", "node_modules", "three", "build", "three.module.js")))
    return next((p for p in found if p and os.path.isfile(p)), None)


class Gltf(ForemanTestCase):
    def write(self, name, data):
        path = os.path.join(self.tmp, name)
        with open(path, "wb" if isinstance(data, bytes) else "w") as f:
            f.write(data if isinstance(data, bytes) else json.dumps(data))
        return path

    def test_a_good_file_passes_and_each_break_is_named(self):
        self.assertEqual(fmscene.gltf_problems(self.write("ok.gltf", gltf())), [])
        cases = [(gltf(asset={"version": "1.0"}), "asset.version is '1.0'"),
                 (gltf(nodes=[{"mesh": 3}]), "nodes[0].mesh: meshes index 3 out of range"),
                 (gltf(accessors=[{"bufferView": 0, "componentType": 5126, "count": 4, "type": "VEC3"}]),
                  "accessors[0] needs 48 bytes of bufferViews[0], which has 36"),
                 (gltf(bufferViews=[{"buffer": 0, "byteLength": 40}]), "bufferViews[0] ends at byte 40 of buffers[0]"),
                 (gltf(buffers=[{"byteLength": 36, "uri": "../../secret.bin"}]), "outside the asset's folder"),
                 (gltf(buffers=[{"byteLength": 36, "uri": "missing.bin"}]), "missing.bin isn't there")]
        for k, (doc, said) in enumerate(cases):
            with self.subTest(said=said):
                found = fmscene.gltf_problems(self.write(f"bad{k}.gltf", doc))
                self.assertTrue(any(said in x for x in found), found)
        self.assertIn("not JSON", fmscene.gltf_problems(self.write("junk.gltf", b"{nope"))[0])

    def test_a_glb_reads_its_binary_chunk(self):
        doc = gltf(buffers=[{"byteLength": 36}])
        self.assertEqual(fmscene.gltf_problems(self.write("ok.glb", glb(doc))), [])
        self.assertTrue(any("header says" in x for x in fmscene.gltf_problems(self.write("long.glb", glb(doc, length=999)))))
        short = fmscene.gltf_problems(self.write("short.glb", glb(doc, binary=TRIANGLE[:24])))
        self.assertTrue(any("buffers[0] declares 36 bytes, has 24" in x for x in short), short)

    def test_fm_scene_check_reads_gltf_too(self):
        good, bad = self.write("ok.gltf", gltf()), self.write("bad.gltf", gltf(nodes=[{"mesh": 3}]))
        self.assertIn("✓", self.fm("scene", "check", good).stdout)
        p = self.fm("scene", "check", bad, check=False)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("meshes index 3", p.stdout)


class Soak(ForemanTestCase):
    def test_the_verdict_from_samples(self):
        steady = [{"state": "live", "s": {"geometries": 3, "textures": 0, "frames": 90, "frame_ms": [2] * 90}}] * 3
        self.assertEqual(fmscene.soak_problems(steady, after="poster", budget_ms=16), [])
        grew = steady[:1] + [{"state": "live", "s": {"geometries": 9, "textures": 2, "frames": 200,
                                                      "frame_ms": [2] * 180 + [40] * 20}}]
        found = fmscene.soak_problems(grew, after="live", budget_ms=16)
        self.assertTrue(any("geometries grew from 3 to 9" in x for x in found), found)
        self.assertTrue(any("textures grew from 0 to 2" in x for x in found), found)
        self.assertTrue(any("p95 frame time 40 ms is over the 16 ms budget" in x for x in found), found)
        self.assertTrue(any("still live after dispose()" in x for x in found), found)
        dead = [{"state": "failed", "s": None, "error": "boom"}]
        self.assertTrue(any("never drew" in x for x in fmscene.soak_problems(dead, after="poster")))

    def test_it_says_why_it_skips(self):
        path = os.path.join(self.tmp, "scene.json")
        with open(path, "w") as f:
            json.dump({"camera": {"fov": 40, "position": [0, 0, 5]}}, f)
        out = self.fm("scene", "soak", path, env={"FOREMAN_THREE": os.path.join(self.tmp, "nothing.js"),
                                                  "PATH": "/nonexistent"}, check=False)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("skipped:", out.stdout)

    @unittest.skipUnless(fmshot.chrome() and three(), "needs headless Chrome and a three.js build")
    def test_a_moving_scene_soaks_in_a_real_browser(self):
        path = os.path.join(self.tmp, "scene.json")
        with open(path, "w") as f:
            json.dump({"camera": {"fov": 40, "position": [0, 0.5, 5]}, "materials": {"m": {"color": "#c99c74"}},
                       "lights": [{"type": "directional", "position": [1, 2, 3]}],
                       "meshes": [{"name": "ball", "geometry": {"type": "sphere"}, "material": "m"}],
                       "animations": {"spin": {"target": "ball", "property": "rotation", "times": [0, 2],
                                               "values": [[0, 0, 0], [0, 360, 0]]}}}, f)
        got = fmscene.soak(path, three(), seconds=3, budget_ms=1000)
        self.assertNotIn("skipped", got, got)
        self.assertEqual(got["problems"], [], got)
        self.assertGreater(got["frames"], 10, got)
        self.assertEqual(got["geometries"][0], got["geometries"][-1])
        self.assertEqual(got["after"], "poster")


if __name__ == "__main__":
    unittest.main()
