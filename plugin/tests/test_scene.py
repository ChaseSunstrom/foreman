"""T-1633: scene.json, a 3D scene as plain data. fmscene validates it (every default filled in) and compiles it to an
ES module that builds the scene with three.js and keeps templates/scene.html's survival clauses."""
import copy
import json
import os
import re
import shutil
import subprocess
import unittest

from helpers import ForemanTestCase

import fmscene

SCENE = {
    "background": "#14161C",
    "camera": {"fov": 28, "position": [0, 1.2, 6], "target": [0, 0, 0], "near": 1, "far": 20},
    "lights": [{"type": "hemisphere", "sky": "#f2e4d2", "ground": "#34425e", "intensity": 1.5},
               {"type": "directional", "color": "#fff0dc", "intensity": 2, "position": [-3, 4, 2]}],
    "materials": {"clay": {"color": "#c99c74", "roughness": 0.8}, "glow": {"emissive": "#86b6ff", "emissiveIntensity": 2}},
    "meshes": [{"name": "pebble", "geometry": {"type": "sphere", "radius": 1}, "material": "clay"},
               {"geometry": {"type": "vertices", "vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0]], "faces": [[0, 1, 2]]},
                "material": "glow", "rotation": [0, 90, 0]},
               {"geometry": {"type": "plane", "size": [8, 8]}, "material": "clay", "rotation": [-90, 0, 0]}],
    "animations": {"spin": {"target": "pebble", "property": "rotation", "times": [0, 4],
                            "values": [[0, 0, 0], [0, 360, 0]]}},
}


def embedded(module):
    """The SCENE object the module carries, read back as JSON."""
    m = re.search(r"^export const SCENE = (\{.*?\});$", module, re.M | re.S)
    return json.loads(m.group(1))


# three.js and the browser, stubbed: enough for mount() to run and say what it did.
THREE_STUB = """
export const made = [];
class V { constructor() { this.v = [0, 0, 0]; } set(...v) { this.v = v; return this; } }
class O {
  constructor(...args) { this.args = args; this.position = new V(); this.rotation = new V(); this.scale = new V();
    this.kids = []; made.push(this); }
  add(o) { this.kids.push(o); } lookAt(...v) { this.look = v; } updateProjectionMatrix() { this.updated = true; }
  dispose() { this.disposed = true; } setAttribute(k, a) { this[k] = a; } setIndex(i) { this.index = i; }
  computeVertexNormals() { this.normals = true; }
}
export class Scene extends O {}
export class PerspectiveCamera extends O {}
export class Mesh extends O {}
export class BoxGeometry extends O {}
export class SphereGeometry extends O {}
export class PlaneGeometry extends O {}
export class BufferGeometry extends O {}
export class Float32BufferAttribute extends O {}
export class MeshStandardMaterial extends O {}
export class AmbientLight extends O {}
export class HemisphereLight extends O {}
export class DirectionalLight extends O {}
export class PointLight extends O {}
export const ACESFilmicToneMapping = 4;
export class WebGLRenderer extends O {
  debug = {}; frames = 0;
  setPixelRatio(d) { this.dpr = d; } setSize(w, h, css) { this.size = [w, h, css]; }
  setClearColor(c, a) { this.clear = [c, a]; } render() { this.frames++; } forceContextLoss() { this.released = true; }
  compile() { if (globalThis.shaderFails) this.debug.onShaderError?.(this.args[0].context, "program"); }
}
"""
DRIVER = """
import { made } from "three";
const mode = process.argv[2], errors = [];
console.error = (...a) => errors.push(a.map(String).join(" "));
const events = () => { const on = {}; return {
  addEventListener(t, f, o) { (on[t] ??= new Set()).add(f); o?.signal?.addEventListener("abort", () => on[t].delete(f)); },
  fire(t, e = {}) { for (const f of on[t] ?? []) f(e); },
  live: () => Object.values(on).reduce((n, s) => n + s.size, 0) }; };
const reduce = Object.assign(events(), { matches: mode === "reduce" });
globalThis.matchMedia = q => q.includes("reduced-motion") ? reduce : Object.assign(events(), { matches: false });
globalThis.document = Object.assign(events(), { hidden: false });
globalThis.window = { devicePixelRatio: 3 };
globalThis.shaderFails = mode === "shader";
const queued = new Map(); let ids = 0;
globalThis.requestAnimationFrame = f => { queued.set(++ids, f); return ids; };
globalThis.cancelAnimationFrame = id => queued.delete(id);
const tick = now => { const fs = [...queued.values()]; queued.clear(); fs.forEach(f => f(now)); };
let ro, io, lost = false;
globalThis.ResizeObserver = class { constructor(cb) { ro = this; this.cb = cb; } observe() {} disconnect() { this.off = true; } };
globalThis.IntersectionObserver = class { constructor(cb) { io = this; this.cb = cb; } observe() {} disconnect() { this.off = true; } };
const gl = { isContextLost: () => lost, getProgramInfoLog: () => "ERROR: 0:1: oops",
             getExtension: () => ({ loseContext() { lost = true; } }) };
const canvas = Object.assign(events(), { clientWidth: 800, clientHeight: 500,
  getContext(kind, attrs) { canvas.asked = [kind, attrs]; return mode === "nogl" ? null : gl; } });
const fig = { dataset: { state: "poster" }, querySelector: () => canvas };
const { mount } = await import("./scene.mjs");
const dispose = mount(fig), find = name => made.find(o => o.constructor.name === name);
const r = find("WebGLRenderer"), cam = find("PerspectiveCamera"), pebble = find("Mesh");
const out = { asked: canvas.asked, renderer: !!r };
ro?.cb([]);
out.first = fig.dataset.state;
if (r) Object.assign(out, { dpr: r.dpr, size: r.size, clear: r.clear, camera: cam.args, aspect: cam.aspect,
                            at: cam.position.v, look: cam.look, tone: r.toneMapping });
tick(1000); tick(2000); tick(2500);
out.yaw = pebble?.rotation.v[1]; out.queued = queued.size;
let prevented = false;
lost = true; canvas.fire("webglcontextlost", { preventDefault() { prevented = true; } });
out.lost = [fig.dataset.state, prevented, queued.size];
lost = false; canvas.fire("webglcontextrestored");
out.restored = fig.dataset.state;
document.hidden = true; document.fire("visibilitychange"); out.hidden = queued.size;
document.hidden = false; document.fire("visibilitychange"); out.shown = queued.size;
io?.cb([{ isIntersecting: false }]); out.offscreen = queued.size;
dispose();
out.after = { state: fig.dataset.state, released: r ? r.released : lost, freed: made.filter(o => o.disposed).length,
              listeners: canvas.live() + document.live() + reduce.live(), observers: !ro || (ro.off && io.off) };
out.errors = errors;
console.log(JSON.stringify(out));
"""


class Three(ForemanTestCase):
    def test_the_module_holds_the_camera_it_was_given(self):
        module = fmscene.compile_three(fmscene.validate(copy.deepcopy(SCENE)))
        self.assertIn('import * as THREE from "three";', module)
        self.assertIn("export function mount(fig)", module)
        got = embedded(module)
        self.assertEqual(got["camera"], SCENE["camera"])
        self.assertEqual(got["background"], "#14161c", "colours come out as lowercase #rrggbb")
        self.assertEqual(got["materials"]["clay"]["color"], "#c99c74")
        for clause in ("failIfMajorPerformanceCaveat", "webglcontextlost", "preventDefault", "prefers-reduced-motion",
                       "IntersectionObserver", "visibilitychange", "forceContextLoss", "? 1.5 : 2"):
            self.assertIn(clause, module)
        self.assertEqual(module, fmscene.compile_three(fmscene.validate(copy.deepcopy(SCENE))), "the same bytes twice")

    def run_module(self, mode):
        d = os.path.join(self.tmp, mode)
        os.makedirs(os.path.join(d, "node_modules", "three"))
        files = {"scene.mjs": fmscene.compile_three(fmscene.validate(copy.deepcopy(SCENE))), "drive.mjs": DRIVER,
                 "node_modules/three/package.json": '{"name": "three", "type": "module", "main": "index.js"}',
                 "node_modules/three/index.js": THREE_STUB}
        for name, text in files.items():
            with open(os.path.join(d, name), "w") as f:
                f.write(text)
        p = subprocess.run(["node", "drive.mjs", mode], cwd=d, capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    @unittest.skipUnless(shutil.which("node"), "no node here to run the module against a stubbed three.js")
    def test_the_module_survives_in_a_stubbed_browser(self):
        o = self.run_module("live")
        self.assertEqual(o["asked"][0], "webgl2")
        self.assertTrue(o["asked"][1]["failIfMajorPerformanceCaveat"], "a software renderer gets the poster")
        self.assertEqual((o["camera"], o["at"], o["look"]), ([28, 1, 1, 20], [0, 1.2, 6], [0, 0, 0]))
        self.assertEqual((o["dpr"], o["size"], o["aspect"]), (2, [800, 500, False], 1.6), "DPR capped at 2")
        self.assertEqual((o["clear"], o["tone"], o["first"]), (["#14161c", 1], 4, "live"))
        self.assertAlmostEqual(o["yaw"], 0.2 / 4 * 360 * 3.141592653589793 / 180, 6, "dt capped at 0.1 s a frame")
        self.assertEqual(o["queued"], 1, "an animated scene keeps its loop")
        self.assertEqual((o["lost"], o["restored"]), (["lost", True, 0], "live"))
        self.assertEqual((o["hidden"], o["shown"], o["offscreen"]), (0, 1, 0), "no frames hidden or offscreen")
        self.assertEqual(o["after"], {"state": "poster", "released": True, "freed": 6, "listeners": 0, "observers": True},
                         "3 geometries, 2 materials and the renderer freed, the context released")
        self.assertEqual(o["errors"], [])

    @unittest.skipUnless(shutil.which("node"), "no node here to run the module against a stubbed three.js")
    def test_reduced_motion_no_webgl_and_a_shader_error(self):
        o = self.run_module("reduce")
        self.assertEqual((o["first"], o["yaw"], o["queued"]), ("live", 0, 0), "one still frame, no loop")
        o = self.run_module("nogl")
        self.assertEqual((o["renderer"], o["first"], o["errors"]), (False, "poster", []), "the poster stays, no throw")
        o = self.run_module("shader")
        self.assertEqual((o["first"], o["restored"], o["queued"]), ("failed", "failed", 0))
        self.assertEqual(len(o["errors"]), 1, "logged once")
        self.assertIn("oops", o["errors"][0])

    def test_fm_scene_compile(self):
        src, js = os.path.join(self.tmp, "scene.json"), os.path.join(self.tmp, "scene.js")
        with open(src, "w") as f:
            json.dump(SCENE, f)
        p = self.fm("scene", "compile", src, "--to", "three")
        self.assertEqual(embedded(p.stdout)["camera"]["fov"], 28)
        self.fm("scene", "compile", src, "--out", "scene.js", cwd=self.tmp)  # a bare name lands in the cwd
        with open(js) as f:
            self.assertEqual(f.read(), p.stdout)
        p = self.fm("scene", "compile", src, "--out", src, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("is the scene it compiles", p.stderr)
        with open(src) as f:
            self.assertEqual(json.load(f), SCENE, "the source is never overwritten")
        with open(src, "w") as f:
            f.write('{"camera": {"fov": 28, "position": [0, 0, 5], "fov": 30}}')
        p = self.fm("scene", "compile", src, check=False)
        self.assertEqual((p.returncode, p.stdout), (2, ""))
        self.assertIn("'fov' appears twice", p.stderr)
        fifo = os.path.join(self.tmp, "fifo.json")
        os.mkfifo(fifo)
        p = self.fm("scene", "compile", fifo, check=False)  # open() alone would wait for a writer forever
        self.assertEqual(p.returncode, 2)
        self.assertIn("not a regular file", p.stderr)


class Schema(ForemanTestCase):
    def test_defaults_are_filled_in(self):
        s = fmscene.validate({"camera": {"fov": 30, "position": [0, 0, 5]}, "materials": {"m": {}},
                              "meshes": [{"geometry": {"type": "box"}, "material": "m"}]})
        self.assertEqual(s["camera"], {"fov": 30, "position": [0, 0, 5], "target": [0, 0, 0], "near": 0.1, "far": 100})
        self.assertEqual(s["background"], None)
        self.assertEqual(s["materials"]["m"], {"color": "#cccccc", "roughness": 0.8, "metalness": 0,
                                               "emissive": "#000000", "emissiveIntensity": 1})
        self.assertEqual(s["meshes"], [{"name": None, "geometry": {"type": "box", "size": [1, 1, 1]}, "material": "m",
                                        "position": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}])
        self.assertEqual((s["lights"], s["animations"]), ([], {}))
        s = fmscene.validate(copy.deepcopy(SCENE))
        self.assertEqual(s["lights"][0], {"type": "hemisphere", "intensity": 1.5, "sky": "#f2e4d2", "ground": "#34425e"})
        self.assertEqual(s["meshes"][0]["geometry"], {"type": "sphere", "radius": 1, "segments": 32})
        self.assertTrue(s["animations"]["spin"]["loop"])

    def test_what_it_refuses_names_the_place(self):
        def bad(path, value):
            s = copy.deepcopy(SCENE)
            *head, last = path
            node = s
            for k in head:
                node = node[k]
            if value is KeyError:
                del node[last]
            else:
                node[last] = value
            return s
        cases = [
            (bad(["camera"], KeyError), "scene: camera is missing"),
            (bad(["camera", "fov"], 0), "camera.fov: wants a number at least 1 and at most 179, not 0"),
            (bad(["camera", "fov"], True), "camera.fov"),
            (bad(["camera", "fov"], 10 ** 400), "camera.fov"),
            (bad(["camera", "position"], [0, 0]), "camera.position: wants a list of 3 numbers"),
            (bad(["camera", "near"], 0.001), "camera.far: wants a number above near and at most 10,000 x near"),
            (bad(["camera", "target"], [0, 1.2, 6]), "camera.target"),
            (bad(["camera", "zoom"], 2), "camera: unknown key 'zoom'"),
            (bad(["background"], "red"), "background: wants a colour"),
            (bad(["lights", 0, "type"], ["spot"]), "lights[0]: wants a type"),
            (bad(["lights", 0, "color"], "#fff"), "lights[0]: unknown key 'color'"),
            (bad(["lights", 1, "position"], [0, 0, 0]), "lights[1].position"),
            (bad(["lights"], [{"type": "point"}] * 4), "lights: at most 3 directional and point lights"),
            (bad(["materials", "clay", "roughness"], 0), "materials.clay.roughness: wants a number above 0"),
            (bad(["materials", "__proto__"], {}), "materials: wants a name"),
            (bad(["meshes", 0, "material"], "stone"), "meshes[0].material: no material named stone"),
            (bad(["meshes", 0, "material"], ["clay"]), "meshes[0].material: wants a name"),
            (bad(["meshes", 0, "geometry", "type"], "torus"), "meshes[0].geometry: wants a type"),
            (bad(["meshes", 0, "geometry", "segments"], 2.5), "meshes[0].geometry.segments: wants an integer"),
            (bad(["meshes", 1, "geometry", "faces"], [[0, 1, 3]]), "meshes[1].geometry.faces[0]"),
            (bad(["meshes", 1, "geometry", "vertices"], [[0, 0, 0]]), "meshes[1].geometry.vertices: wants at least 3"),
            (bad(["meshes", 1, "name"], "pebble"), "meshes[1].name: pebble names an earlier mesh too"),
            (bad(["animations", "spin", "target"], "rock"), "animations.spin.target: no mesh named rock"),
            (bad(["animations", "spin", "times"], [0, 0]), "animations.spin.times: must rise"),
            (bad(["animations", "spin", "values"], [[0, 0, 0]]), "animations.spin.values: one per time"),
            (bad(["animations", "twice"], dict(SCENE["animations"]["spin"])), "animations.twice: spin moves"),
        ]
        for scene, want in cases:
            with self.subTest(want=want), self.assertRaises(ValueError) as e:
                fmscene.validate(scene)
            self.assertIn(want, str(e.exception))

    def test_loads_refuses_what_json_lets_through(self):
        for text, want in [('{"camera": {"fov": NaN, "position": [0, 0, 5]}}', "NaN"),
                           ('{"camera": {"fov": 1e400, "position": [0, 0, 5]}}', "camera.fov"),
                           ("[" * 100000 + "]" * 100000, "nested too deeply")]:
            with self.subTest(want=want), self.assertRaises(ValueError) as e:
                fmscene.loads(text)
            self.assertIn(want, str(e.exception))
        self.assertEqual(fmscene.loads('﻿{"camera": {"fov": 30, "position": [0, 0, 5]}}')["camera"]["fov"], 30)


if __name__ == "__main__":
    unittest.main()
