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


# Before <fm-scene> is defined the page's own CSS gives it its box, so the module loading shifts nothing.
PREDEFINED = ("fm-scene:not(:defined){display:block;position:relative;aspect-ratio:16/10}",
              "fm-scene:not(:defined)>[slot=poster]{width:100%;height:100%;object-fit:cover}")


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
  setClearColor(c, a) { this.clear = [c, a]; } render() { this.frames++; }
  forceContextLoss() { this.released = true; this.args[0].canvas.lost = true; }
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
let ro, io;
globalThis.ResizeObserver = class { constructor(cb) { ro = this; this.cb = cb; } observe() {} disconnect() { this.off = true; } };
globalThis.IntersectionObserver = class { constructor(cb) { io = this; this.cb = cb; } observe() {} disconnect() { this.off = true; } };
// <fm-scene>'s platform, stubbed: an element whose open shadow root's markup makes the one canvas. A second
// attachShadow throws, as a browser's does once a root is there.
const defined = new Map(), shadow = mode => ({ mode, querySelector: () => fig.canvas ?? null,
                                              set innerHTML(h) { fig.canvas = makeCanvas(); } });
globalThis.customElements = { get: n => defined.get(n), define: (n, c) => defined.set(n, c) };
globalThis.HTMLElement = class { dataset = {}; attrs = {}; getAttribute(k) { return this.attrs[k] ?? null; }
  attachShadow(o) { if (this.shadowRoot) throw new Error("a shadow root is there already");
                    return this.shadowRoot = shadow(o.mode); } };
// A canvas keeps its one context for life, as a browser's does: once lost for good, only a new canvas draws again.
let fig = { dataset: { state: "poster" }, querySelector: () => fig.canvas };
const makeCanvas = (attrs = {}) => { const cv = Object.assign(events(), { clientWidth: 800, clientHeight: 500, lost: false,
  attrs, setAttribute(k, v) { cv.attrs[k] = v; }, removeAttribute(k) { delete cv.attrs[k]; },
  getContext(kind, attrs) { cv.asked = [kind, attrs]; return mode === "nogl" ? null : cv.gl ??= {
    canvas: cv, isContextLost: () => cv.lost, getProgramInfoLog: () => "ERROR: 0:1: oops",
    getExtension: () => ({ loseContext() { cv.lost = true; } }) }; },
  cloneNode: () => makeCanvas({ ...cv.attrs }), replaceWith(n) { fig.canvas = n; } }); return cv; };
fig.canvas = makeCanvas();
const { mount } = await import("./scene.mjs");
let start = () => mount(fig);
const element = mode === "component" || mode === "declarative";
if (element) {  // the element mounts on connect and frees on disconnect; the rest of the run is the same
  const el = fig = new (customElements.get("fm-scene"))();
  el.attrs.label = "A clay pebble";
  if (mode === "declarative") el.shadowRoot = shadow("open");  // the page's <template shadowrootmode>, no canvas
  start = () => { el.connectedCallback(); return () => el.disconnectedCallback(); };
}
const dispose = start(), canvas = fig.canvas, find = name => made.find(o => o.constructor.name === name);
const r = find("WebGLRenderer"), cam = find("PerspectiveCamera"), pebble = find("Mesh");
const out = { asked: canvas.asked, renderer: !!r };
await 0;  // what fail() queued runs now
out.early = { freed: made.filter(o => o.disposed).length, released: !!r?.released };
ro?.cb([]);
out.first = fig.dataset.state;
if (r) Object.assign(out, { dpr: r.dpr, size: r.size, clear: r.clear, camera: cam.args, aspect: cam.aspect,
                            at: cam.position.v, look: cam.look, tone: r.toneMapping });
tick(1000); tick(2000); tick(2500);
out.yaw = pebble?.rotation.v[1]; out.queued = queued.size;
let prevented = false;
canvas.lost = true; canvas.fire("webglcontextlost", { preventDefault() { prevented = true; } });
out.lost = [fig.dataset.state, prevented, queued.size];
canvas.lost = false; canvas.fire("webglcontextrestored");
out.restored = fig.dataset.state;
document.hidden = true; document.fire("visibilitychange"); out.hidden = queued.size;
document.hidden = false; document.fire("visibilitychange"); out.shown = queued.size;
io?.cb([{ isIntersecting: true }, { isIntersecting: false }]); out.offscreen = queued.size;  // a batch: the last counts
io?.cb([{ isIntersecting: false }, { isIntersecting: true }]); out.onscreen = queued.size;
dispose();
out.after = { state: fig.dataset.state, released: r ? r.released : canvas.lost, freed: made.filter(o => o.disposed).length,
              listeners: canvas.live() + document.live() + reduce.live(), observers: !ro || (ro.off && io.off) };
if (mode === "live" || element) {  // a second mount, after dispose() lost the first canvas's context for good
  const again = start(); ro.cb([]);
  out.remount = [fig.dataset.state, fig.canvas !== canvas, fig.canvas.lost]; again();
}
if (fig.shadowRoot) out.element = [fig.shadowRoot.mode, canvas.attrs["aria-label"], fig.canvas.attrs["aria-label"]];
if (element) {  // T-1706: label is watched: a new one reaches the canvas; taken away, the canvas hides and the twin speaks
  out.observed = customElements.get("fm-scene").observedAttributes;
  fig.attrs.label = "A wet pebble"; fig.attributeChangedCallback("label", "A clay pebble", "A wet pebble");
  const named = fig.canvas.attrs["aria-label"];
  delete fig.attrs.label; fig.attributeChangedCallback("label", "A wet pebble", null);
  out.relabel = [named, fig.canvas.attrs["aria-label"] ?? null, fig.canvas.attrs["aria-hidden"] ?? null];
  const bare = new (customElements.get("fm-scene"))();  // before it is connected (an upgrade sets attributes first)
  bare.attributeChangedCallback("label", null, "x"); out.early_label = "ok";
}
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
        self.assertNotIn("</", module, "pasted into a <script>, nothing in it closes the tag")
        self.assertTrue(module.isascii(), "no character an encoding mix-up could mangle")

    def test_the_latest_intersection_entry_counts(self):
        """A batch of entries comes oldest first: reading the first one leaves the loop running offscreen."""
        template = os.path.join(os.path.dirname(fmscene.__file__), "..", "skills", "playbooks", "references", "ui",
                                "templates", "scene.html")
        with open(template) as f:
            for name, text in (("scene.html", f.read()), ("the module", fmscene.RUNTIME)):
                self.assertIn("IntersectionObserver(entries => { onscreen = entries.at(-1).isIntersecting;", text, name)

    def run_module(self, mode):
        d = os.path.join(self.tmp, mode)
        os.makedirs(os.path.join(d, "node_modules", "three"))
        emit = fmscene.compile_component if mode in ("component", "declarative") else fmscene.compile_three
        files = {"scene.mjs": emit(fmscene.validate(copy.deepcopy(SCENE))), "drive.mjs": DRIVER,
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
        self.assertEqual((o["hidden"], o["shown"]), (0, 1), "no frames in a hidden tab")
        self.assertEqual((o["offscreen"], o["onscreen"]), (0, 1), "the latest entry of a batch decides")
        self.assertEqual(o["early"], {"freed": 0, "released": False})
        self.assertEqual(o["after"], {"state": "poster", "released": True, "freed": 6, "listeners": 0, "observers": True},
                         "3 geometries, 2 materials and the renderer freed, the context released")
        self.assertEqual(o["remount"], ["live", True, False], "a second mount draws on a fresh canvas")
        self.assertEqual(o["errors"], [])

    @unittest.skipUnless(shutil.which("node"), "no node here to run the module against a stubbed three.js")
    def test_reduced_motion_no_webgl_and_a_shader_error(self):
        o = self.run_module("reduce")
        self.assertEqual((o["first"], o["yaw"], o["queued"]), ("live", 0, 0), "one still frame, no loop")
        o = self.run_module("nogl")
        self.assertEqual((o["renderer"], o["first"], o["errors"]), (False, "poster", []), "the poster stays, no throw")
        o = self.run_module("shader")
        self.assertEqual((o["first"], o["restored"], o["queued"]), ("failed", "failed", 0))
        self.assertEqual(o["early"], {"freed": 6, "released": True}, "a failed scene frees all it made at once")
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
        link = os.path.join(self.tmp, "link.js")
        os.symlink(src, link)
        p = self.fm("scene", "compile", src, "--out", link, check=False)  # a link to the source is the source
        self.assertEqual(p.returncode, 2)
        self.assertIn("is the scene it compiles", p.stderr)
        self.assertTrue(os.path.islink(link))
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


class Component(ForemanTestCase):
    """T-1634: --to component wraps the same module in <fm-scene>, a custom element mounting it in its shadow DOM."""
    def test_the_component_holds_the_same_camera_and_materials(self):
        scene = fmscene.validate(copy.deepcopy(SCENE))
        three, component = fmscene.compile_three(scene), fmscene.compile_component(scene)
        self.assertEqual(embedded(component), embedded(three), "one SCENE: camera, materials and all")
        self.assertIn(fmscene.RUNTIME, component, "mount() and its survival code whole, not a fork")
        for part in ('attachShadow({ mode: "open" })', '<slot name="poster">', "<canvas role=\"img\">",
                     ":host([data-state=\"live\"]) canvas", "prefers-reduced-motion: reduce",
                     'customElements.define("fm-scene", FmScene)', '::slotted([slot="poster"]) { object-fit: cover; }',
                     *PREDEFINED, "::part(stage)"):
            self.assertIn(part, component)
        playbook = os.path.join(os.path.dirname(fmscene.__file__), "..", "skills", "playbooks", "references", "ui",
                                "scene-3d.md")
        with open(playbook) as f:
            text = f.read()
        for part in ("--to component", *PREDEFINED, "::part(stage)", 'define("fm-scene-2", FmScene)'):
            self.assertIn(part, text, "the playbook says how to place the element without a layout shift")
        self.assertEqual(component, fmscene.compile_component(fmscene.validate(copy.deepcopy(SCENE))), "same bytes")
        self.assertNotIn("</", component, "pasted into a <script>, nothing in it closes the tag")
        self.assertTrue(component.isascii())
        src = os.path.join(self.tmp, "scene.json")
        with open(src, "w") as f:
            json.dump(SCENE, f)
        self.assertEqual(self.fm("scene", "compile", src, "--to", "component").stdout.rstrip("\n"),
                         component.rstrip("\n"))

    run_module = Three.run_module

    @unittest.skipUnless(shutil.which("node"), "no node here to run the element against a stubbed three.js")
    def test_the_element_survives_as_the_module_does(self):
        live, o = self.run_module("live"), self.run_module("component")
        self.assertEqual(o.pop("element"), ["open", "A clay pebble", "A clay pebble"],
                         "a shadow root; the label reaches the canvas, and the fresh one a remount makes")
        self.assertEqual((o.pop("observed"), o.pop("relabel"), o.pop("early_label")),
                         (["label"], ["A wet pebble", None, "true"], "ok"), "label is watched (T-1706)")
        self.assertEqual(o, live, "the same camera, frames, survival and freeing, the state on the element itself")
        o = self.run_module("declarative")
        self.assertEqual(o.pop("element"), ["open", "A clay pebble", "A clay pebble"])
        for k in ("observed", "relabel", "early_label"):
            o.pop(k)
        self.assertEqual(o, live, "a declarative shadow root with no canvas is filled in, not attached again")


class Tag(ForemanTestCase):  # T-1706
    def test_a_tag_names_the_element_so_two_scenes_share_a_page(self):
        scene = fmscene.validate(copy.deepcopy(SCENE))
        two = fmscene.compile_component(scene, tag="pebble-scene")
        self.assertIn('customElements.define("pebble-scene", FmScene)', two)
        self.assertIn("pebble-scene:not(:defined){display:block", two, "the page's box rule names it too")
        self.assertNotIn("fm-scene", two.replace(fmscene.RUNTIME, ""), "nothing outside the shared runtime says fm-scene")
        self.assertEqual(fmscene.compile_component(scene), fmscene.compile_component(scene, tag="fm-scene"))
        for bad in ("pebble", "Pebble-scene", "1-scene", "font-face", "pebble-scène", 'a-"b', "a-b</script"):
            with self.assertRaises(ValueError, msg=bad):
                fmscene.compile_component(scene, tag=bad)
        src = os.path.join(self.tmp, "scene.json")
        with open(src, "w") as f:
            json.dump(SCENE, f)
        self.assertEqual(self.fm("scene", "compile", src, "--to", "component", "--tag", "pebble-scene").stdout.rstrip("\n"),
                         two.rstrip("\n"))
        p = self.fm("scene", "compile", src, "--tag", "pebble-scene", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--tag names the element: use it with --to component", p.stderr)


class Schema(ForemanTestCase):
    def test_the_schema_states_what_a_second_renderer_must_not_guess(self):
        for fact in ("Rx * Ry * Rz", "T * R * S", "up is +Y", "looks down -Z", "negates view-space z",
                     "and reverses each triangle's winding",  # T-1693: or three's front faces are culled
                     "max(2, segments >> 1)", "decay 2", "smooth normals in three.js, flat"):
            self.assertIn(fact, " ".join(fmscene.SCHEMA.split()))

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
            (bad(["camera", "position"], [0, 6, 0]), "camera.target: straight below"),
            (bad(["camera", "target"], [0, 9, 6]), "camera.target: straight above"),
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


CARDS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(fmscene.__file__))), "skills", "library", "cards",
                     "looks")


def plate(**geometry):
    """One red mesh in front of a camera on +Z, on black."""
    return fmscene.validate({"camera": {"fov": 40, "position": [0, 0, 5]}, "background": "#000000",
                             "materials": {"red": {"color": "#ff0000"}},
                             "meshes": [{"geometry": geometry, "material": "red"}]})


def lit(w, h, rgb, cols, k):
    """How many pixels of tile k of a contact sheet aren't the black background."""
    tw, x0, y0 = w // cols, (k % cols) * (w // cols), 0
    return sum(rgb[3 * (y * w + x):3 * (y * w + x) + 3] != b"\0\0\0" for y in range(y0, y0 + h)
               for x in range(x0, x0 + tw))


class Offline(ForemanTestCase):
    """T-1530: 3D checks with no browser or GPU: a camera path, the --hud dev build, a turntable contact sheet drawn by
    fmraster, and GLSL checks of the shader cards."""

    def test_a_camera_path_moves_the_camera_and_keeps_its_aim(self):
        scene = copy.deepcopy(SCENE)
        fly = {"target": "camera", "property": "position", "times": [0, 4], "values": [[0, 1.2, 6], [6, 1.2, 0]]}
        scene["animations"]["fly"] = fly
        module = fmscene.compile_three(fmscene.validate(scene))
        self.assertIn('a.target === "camera" ? camera', module)
        self.assertIn("camera.lookAt(...c.target); };", module)  # every pose keeps the aim
        for bad, said in [({"fly": dict(fly, property="rotation")}, "a camera path moves the camera's position"),
                          ({"fly": dict(fly, target="drone")}, "no mesh named drone (or camera")]:
            with self.subTest(said=said), self.assertRaises(ValueError) as e:
                fmscene.validate(dict(scene, animations=bad))
            self.assertIn(said, str(e.exception))
        named = copy.deepcopy(SCENE)
        named["meshes"][0]["name"] = "camera"
        named["animations"] = {}
        with self.assertRaises(ValueError) as e:
            fmscene.validate(named)
        self.assertIn("camera names the camera", str(e.exception))

    def test_the_hud_is_only_in_a_hud_build(self):
        scene = fmscene.validate(SCENE)
        plain, hud = fmscene.compile_three(scene), fmscene.compile_three(scene, hud=True)
        self.assertNotIn("__fmScene", plain)
        self.assertIn("hud(renderer, fig, performance.now() - t0); }", hud)
        self.assertIn("globalThis.__fmScene", hud)
        self.assertIn("globalThis.__fmScene", fmscene.compile_component(scene, hud=True))
        if shutil.which("node"):  # the dev build still parses as a module
            path = os.path.join(self.tmp, "hud.mjs")
            with open(path, "w", encoding="utf-8") as f:
                f.write(hud)
            p = subprocess.run(["node", "--check", path], capture_output=True, text=True, timeout=30)
            self.assertEqual(p.returncode, 0, p.stderr)

    def test_turntable_shows_front_faces_and_culls_back_ones(self):
        w, h, rgb = fmscene.turntable(plate(type="plane", size=[2, 1]), frames=2, size=(40, 30), cols=2)
        self.assertEqual((w, h, len(rgb)), (80, 30, 80 * 30 * 3))
        self.assertGreater(lit(w, h, rgb, 2, 0), 100)  # facing the camera: drawn
        self.assertEqual(lit(w, h, rgb, 2, 1), 0)  # turned half round: its back, culled as three.js culls it
        w, h, rgb = fmscene.turntable(plate(type="box", size=[2, 1, 0.2]), frames=4, size=(40, 30), cols=4)
        side, front, back = lit(w, h, rgb, 4, 1), lit(w, h, rgb, 4, 0), lit(w, h, rgb, 4, 2)
        self.assertGreater(front, 3 * side)  # a slab face-on, then edge-on
        self.assertLess(abs(front - back), front // 10)
        ball = fmscene.turntable(plate(type="sphere", radius=1, segments=12), frames=1, size=(40, 30), cols=1)
        self.assertGreater(lit(*ball, 1, 0), 100)  # outward faces, whatever order the grid made them in

    def test_fm_scene_check_and_turntable(self):
        path = os.path.join(self.tmp, "scene.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(SCENE, f)
        got = json.loads(self.fm("scene", "check", path, "--json").stdout)
        self.assertEqual((got["meshes"], got["lights"], got["animations"]), (3, 2, 1))
        self.assertEqual(got["triangles"], 32 * 16 * 2 - 2 * 32 + 1 + 2)  # sphere (no empty pole faces), 1, plane
        out = os.path.join(self.tmp, "sheet.png")
        self.fm("scene", "turntable", path, "--out", out, "--frames", "2")
        import fmimg
        info = fmimg.info(out)
        self.assertEqual((info["width"], info["height"]), (320, 100))
        p = self.fm("scene", "turntable", path, check=False)
        self.assertNotEqual(p.returncode, 0, "it writes a PNG: --out")

    def test_the_shipped_shader_cards_pass(self):
        paths = fmscene.shader_paths(CARDS)
        self.assertGreaterEqual(len(paths), 8)
        validator = shutil.which("glslangValidator")
        self.assertEqual([x for p in paths for x in fmscene.shader_problems(p, validator)], [])

    def test_a_card_whose_code_and_table_disagree(self):
        folder = os.path.join(self.tmp, "shaders")
        os.makedirs(folder)
        card = os.path.join(folder, "shader-x.md")
        with open(card, "w", encoding="utf-8") as f:
            f.write("## Shader\n```glsl\n#version 300 es\nprecision highp float;\nuniform float uA;\nout vec4 o;\n"
                    "void main() { o = vec4(uA); }\n```\n\n## Uniforms\n| Uniform | Type |\n|---|---|\n| `uB` | float |\n")
        found = fmscene.shader_problems(card)
        self.assertIn("shader-x.md: the Uniforms table lists uB, which no block declares", found)
        self.assertIn("shader-x.md: uA is declared but not in the Uniforms table", found)
        bad = os.path.join(folder, "broken.frag")
        with open(bad, "w", encoding="utf-8") as f:
            f.write("#version 300 es\nprecision highp float;\nout vec4 o;\nvoid main() { o = vec4(1.0) }\n")
        validator = shutil.which("glslangValidator")
        if validator:
            self.assertTrue(any("doesn't compile as GLSL (frag)" in x for x in fmscene.shader_problems(bad, validator)))
        p = self.fm("scene", "shader", folder, check=False)
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn("2 shader file(s)", p.stdout)


if __name__ == "__main__":
    unittest.main()
