"""fm scene (T-1633): scene.json, a 3D scene described once as plain data, checked and compiled to a three.js module.

validate() returns the scene with every default filled in: one shape for each renderer that reads it (three.js here;
a rasteriser or a web component later reads the same dict). compile_three() emits an ES module modelled on
references/ui/templates/scene.html: no WebGL keeps the poster, context loss is survived, the DPR is capped, reduced
motion holds one still frame, nothing draws offscreen or hidden, a failure ends at the poster, dispose() frees it all.
compile_component() (T-1634) is that module whole plus <fm-scene>, a custom element mounting it in its shadow DOM.
"""
import base64
import json
import math
import os
import re
import stat
import struct

SCHEMA = """scene.json (only camera is required; numbers are finite, colours "#rgb" or "#rrggbb" in sRGB, angles in
degrees, names a letter then letters, digits, - or _; an unknown key is refused, so a typo never passes silently):
  background  the page's colour, so the canvas edge has no seam; null (the default): a transparent canvas
  camera      {fov: vertical, 1-179; position: [x,y,z]; target: [0,0,0]; near: 0.1; far: 100, at most 10,000 x near}
  lights      [{type: ambient | hemisphere | directional | point; color: "#ffffff"; intensity: 1 (three.js r155+
              units); position: [0,1,0] (directional: it shines from there toward the origin; point)}], a hemisphere
              taking sky: "#ffffff" and ground: "#444444" in place of color; at most 3 directional and point lights
  materials   {name: {color: "#cccccc"; roughness: 0.8, above 0, at most 1; metalness: 0, 0-1; emissive: "#000000";
              emissiveIntensity: 1}}
  meshes      [{name; material: a materials name; geometry; position: [0,0,0]; rotation: [0,0,0] (about X, Y, Z);
              scale: [1,1,1]}], geometry one of {type: box, size: [1,1,1]}, {type: sphere, radius: 1, segments:
              32}, {type: plane, size: [1,1]} (in XY, facing +Z), {type: vertices, vertices: [[x,y,z], ...], faces:
              [[a,b,c], ...] (indices, counter-clockwise seen from the front)}
  animations  {name: {target: a mesh's name, or camera for a camera path (position only: it keeps looking at
              camera.target, and no mesh may be named camera); property: position | rotation | scale; times: [seconds, rising];
              values: [[x,y,z], ...], one per time; loop: true}}: linear between keys, held outside them; a loop
              restarts at its last time, so its last value should equal its first (or turn a whole 360)
What a second renderer must not guess (three.js's conventions; world space is right-handed with +Y up):
  rotation    the matrix is Rx * Ry * Rz (three.js's Euler order "XYZ"), so on a point Z turns first
  transform   a mesh's model matrix is T * R * S: scale, then rotate, then move
  camera      its up is +Y and it looks down -Z of its own frame, toward target (one straight above or below is
              refused); a renderer whose view space looks along +z, as fmraster's does, negates view-space z
              and reverses each triangle's winding (the mirror keeps the screen winding, so three's front
              faces would be culled)
  sphere      width segments are segments, height segments max(2, segments >> 1)
  point       a point light falls off as intensity / distance^2: decay 2, no cutoff distance
  vertices    smooth normals in three.js, flat per face in the rasteriser (three sums the faces' normals at
              each vertex, area-weighted)"""

MAX_FILE = 16 << 20  # a scene with a million vertices fits; the module carries all of it
NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,63}")  # never __proto__: the module's object literal would eat it
HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")
LIGHTS = {"ambient": {"color": "#ffffff"}, "hemisphere": {"sky": "#ffffff", "ground": "#444444"},
          "directional": {"color": "#ffffff", "position": [0, 1, 0]}, "point": {"color": "#ffffff", "position": [0, 1, 0]}}
DIRECT = 3  # scene-3d.md: at most three direct lights
GEOMETRIES = ("box", "sphere", "plane", "vertices")
PROPERTIES = ("position", "rotation", "scale")


def _fail(where, what):
    raise ValueError(f"{where}: {what}")


def _show(v):
    s = repr(v)  # repr escapes control characters: nothing from the file reaches the terminal raw
    return s if len(s) <= 40 else s[:39] + "…"


def _obj(v, where, required=(), optional=()):
    if not isinstance(v, dict):
        _fail(where, f"wants an object, not {_show(v)}")
    for k in v:
        if k not in required and k not in optional:
            _fail(where, f"unknown key {_show(k)} (known: {', '.join([*required, *optional])})")
    for k in required:
        if k not in v:
            _fail(where, f"{k} is missing")
    return v


def _list(v, where):
    if not isinstance(v, list):
        _fail(where, f"wants a list, not {_show(v)}")
    return v


def _num(v, where, lo=-math.inf, hi=math.inf, above=False, integer=False):
    ok = not isinstance(v, bool) and isinstance(v, int if integer else (int, float))
    try:
        ok = ok and math.isfinite(v) and (v > lo if above else v >= lo) and v <= hi
    except OverflowError:  # an int past a float's range
        ok = False
    if not ok:
        bounds = [f"{'above' if above else 'at least'} {lo:g}"] * (lo > -math.inf) + [f"at most {hi:g}"] * (hi < math.inf)
        _fail(where, f"wants {'an integer' if integer else 'a number'}{' ' if bounds else ''}{' and '.join(bounds)}, "
                     f"not {_show(v)}")
    return v


def _vec(v, where, n=3, **bounds):
    if not isinstance(v, list) or len(v) != n:
        _fail(where, f"wants a list of {n} numbers, not {_show(v)}")
    return [_num(x, f"{where}[{i}]", **bounds) for i, x in enumerate(v)]


def _colour(v, where):
    if not isinstance(v, str) or not HEX.fullmatch(v):
        _fail(where, f'wants a colour, "#rgb" or "#rrggbb", not {_show(v)}')
    v = v.lower()
    return v if len(v) == 7 else "#" + "".join(ch * 2 for ch in v[1:])


def _name(v, where):
    if not isinstance(v, str) or not NAME.fullmatch(v):
        _fail(where, f"wants a name (a letter, then up to 63 letters, digits, - or _), not {_show(v)}")
    return v


def _geometry(g, w):
    if not isinstance(g, dict) or g.get("type") not in GEOMETRIES:
        _fail(w, f"wants a type: {' | '.join(GEOMETRIES)}")
    t = g["type"]
    if t == "box":
        _obj(g, w, ["type"], ["size"])
        return {"type": t, "size": _vec(g.get("size", [1, 1, 1]), f"{w}.size", lo=0, above=True)}
    if t == "sphere":
        _obj(g, w, ["type"], ["radius", "segments"])
        return {"type": t, "radius": _num(g.get("radius", 1), f"{w}.radius", 0, above=True),
                "segments": _num(g.get("segments", 32), f"{w}.segments", 3, 256, integer=True)}
    if t == "plane":
        _obj(g, w, ["type"], ["size"])
        return {"type": t, "size": _vec(g.get("size", [1, 1]), f"{w}.size", 2, lo=0, above=True)}
    _obj(g, w, ["type", "vertices", "faces"])
    vs = [_vec(v, f"{w}.vertices[{i}]") for i, v in enumerate(_list(g["vertices"], f"{w}.vertices"))]
    if len(vs) < 3:
        _fail(f"{w}.vertices", f"wants at least 3, not {len(vs)}")
    faces = [_vec(f, f"{w}.faces[{i}]", lo=0, hi=len(vs) - 1, integer=True)
             for i, f in enumerate(_list(g["faces"], f"{w}.faces"))]
    if not faces:
        _fail(f"{w}.faces", "wants at least one face")
    return {"type": t, "vertices": vs, "faces": faces}


def validate(scene):
    """A parsed scene.json → the same scene with every default filled in; ValueError names the first bad place."""
    _obj(scene, "scene", ["camera"], ["background", "lights", "materials", "meshes", "animations"])
    bg = scene.get("background")
    c = _obj(scene["camera"], "camera", ["fov", "position"], ["target", "near", "far"])
    cam = {"fov": _num(c["fov"], "camera.fov", 1, 179), "position": _vec(c["position"], "camera.position"),
           "target": _vec(c.get("target", [0, 0, 0]), "camera.target"),
           "near": _num(c.get("near", 0.1), "camera.near", 0, above=True),
           "far": _num(c.get("far", 100), "camera.far", 0, above=True)}
    if not cam["near"] < cam["far"] <= 10000 * cam["near"]:  # scene-3d.md: clip planes as tight as the scene allows
        _fail("camera.far", f"wants a number above near and at most 10,000 x near, not {_show(cam['far'])}")
    if cam["position"] == cam["target"]:
        _fail("camera.target", "is where the camera stands, so it has no direction to look")
    dx, dy, dz = (t - p for t, p in zip(cam["target"], cam["position"]))
    if math.hypot(dx, dz) <= 1e-9 * abs(dy):  # along up (+Y): the view has no sideways axis to build
        _fail("camera.target", f"straight {'above' if dy > 0 else 'below'} the camera, along its up (+Y): move one "
                               "of them aside a little")

    lights, direct = [], 0
    for i, l in enumerate(_list(scene.get("lights", []), "lights")):
        w = f"lights[{i}]"
        if not isinstance(l, dict) or not isinstance(l.get("type"), str) or l["type"] not in LIGHTS:
            _fail(w, f"wants a type: {' | '.join(LIGHTS)}")
        t, extra = l["type"], LIGHTS[l["type"]]
        _obj(l, w, ["type"], ["intensity", *extra])
        out = {"type": t, "intensity": _num(l.get("intensity", 1), f"{w}.intensity", 0)}
        for k, d in extra.items():
            out[k] = _vec(l.get(k, d), f"{w}.{k}") if k == "position" else _colour(l.get(k, d), f"{w}.{k}")
        if t == "directional" and not any(out["position"]):  # its direction would be the zero vector: NaN light
            _fail(f"{w}.position", "is where it shines from toward the origin, so not the origin itself")
        direct += t in ("directional", "point")
        lights.append(out)
    if direct > DIRECT:
        _fail("lights", f"at most {DIRECT} directional and point lights (scene-3d.md), not {direct}")

    materials = {}
    if not isinstance(scene.get("materials", {}), dict):
        _fail("materials", "wants an object of named materials")
    for name, m in scene.get("materials", {}).items():
        w = f"materials.{_name(name, 'materials')}"
        _obj(m, w, (), ["color", "roughness", "metalness", "emissive", "emissiveIntensity"])
        materials[name] = {"color": _colour(m.get("color", "#cccccc"), f"{w}.color"),
                           "roughness": _num(m.get("roughness", 0.8), f"{w}.roughness", 0, 1, above=True),
                           "metalness": _num(m.get("metalness", 0), f"{w}.metalness", 0, 1),
                           "emissive": _colour(m.get("emissive", "#000000"), f"{w}.emissive"),
                           "emissiveIntensity": _num(m.get("emissiveIntensity", 1), f"{w}.emissiveIntensity", 0)}

    meshes, names = [], set()
    for i, m in enumerate(_list(scene.get("meshes", []), "meshes")):
        w = f"meshes[{i}]"
        _obj(m, w, ["geometry", "material"], ["name", "position", "rotation", "scale"])
        name = None if m.get("name") is None else _name(m["name"], f"{w}.name")
        if name and name in names:
            _fail(f"{w}.name", f"{name} names an earlier mesh too")
        if name == "camera":  # T-1530: an animation's target camera is the camera's path
            _fail(f"{w}.name", "camera names the camera, which an animation can move: call the mesh something else")
        names.add(name)
        mat = _name(m["material"], f"{w}.material")
        if mat not in materials:
            _fail(f"{w}.material", f"no material named {mat}")
        meshes.append({"name": name, "geometry": _geometry(m["geometry"], f"{w}.geometry"), "material": mat,
                       "position": _vec(m.get("position", [0, 0, 0]), f"{w}.position"),
                       "rotation": _vec(m.get("rotation", [0, 0, 0]), f"{w}.rotation"),
                       "scale": _vec(m.get("scale", [1, 1, 1]), f"{w}.scale")})
    names.discard(None)

    animations, moved = {}, {}
    if not isinstance(scene.get("animations", {}), dict):
        _fail("animations", "wants an object of named animations")
    for name, a in scene.get("animations", {}).items():
        w = f"animations.{_name(name, 'animations')}"
        _obj(a, w, ["target", "property", "times", "values"], ["loop"])
        target = _name(a["target"], f"{w}.target")
        if target not in names and target != "camera":
            _fail(f"{w}.target", f"no mesh named {target} (or camera, for a camera path)")
        prop = a["property"]
        if prop not in PROPERTIES:
            _fail(f"{w}.property", f"wants {' | '.join(PROPERTIES)}, not {_show(prop)}")
        if target == "camera" and prop != "position":  # T-1530: it looks at camera.target, so only its place moves
            _fail(f"{w}.property", f"a camera path moves the camera's position (it keeps looking at camera.target), "
                                   f"not its {prop}")
        if (target, prop) in moved:  # two would fight over it, the last one silently winning
            _fail(w, f"{moved[target, prop]} moves {target}'s {prop} already")
        moved[target, prop] = name
        times = [_num(t, f"{w}.times[{j}]", 0) for j, t in enumerate(_list(a["times"], f"{w}.times"))]
        if not times or any(b <= t for t, b in zip(times, times[1:])):
            _fail(f"{w}.times", "must rise, from at least one time")
        values = _list(a["values"], f"{w}.values")
        if len(values) != len(times):
            _fail(f"{w}.values", f"one per time: {len(times)} wanted, not {len(values)}")
        loop = a.get("loop", True)
        if not isinstance(loop, bool):
            _fail(f"{w}.loop", f"wants true or false, not {_show(loop)}")
        animations[name] = {"target": target, "property": prop, "times": times,
                            "values": [_vec(v, f"{w}.values[{j}]") for j, v in enumerate(values)], "loop": loop}

    return {"background": None if bg is None else _colour(bg, "background"), "camera": cam, "lights": lights,
            "materials": materials, "meshes": meshes, "animations": animations}


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:  # json keeps the last silently: a second "camera" would hide the first
            raise ValueError(f"key {_show(k)} appears twice in one object")
        out[k] = v
    return out


def _constant(name):
    raise ValueError(f"{name} is not a number JSON allows")


def loads(text):
    """scene.json's text → the validated scene (a leading byte-order mark is fine)."""
    text = text.removeprefix("﻿")
    if _depth(text) > MAX_DEPTH:  # T-1799: json's own limit is the C stack's, so it differs by platform and Python
        raise ValueError("nested too deeply")
    try:
        return validate(json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant))
    except RecursionError:
        raise ValueError("nested too deeply") from None


MAX_DEPTH = 256


def _depth(text):
    """The deepest [ or { nesting outside strings."""
    d = top = 0
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"|[\[{\]}]', text):
        t = m.group()
        if t in ("[", "{"):
            d += 1
            top = max(top, d)
        elif t in ("]", "}"):
            d -= 1
    return top


def load(path):
    """A scene.json file → the validated scene; ValueError for a file that isn't regular, is too big or is wrong."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)  # a plain open() of a FIFO waits for a writer
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            raise ValueError("not a regular file")
        with os.fdopen(fd, "rb") as f:
            data = f.read(MAX_FILE + 1)
        if len(data) > MAX_FILE:
            raise ValueError(f"too large a file (over {MAX_FILE >> 20} MB)")
        return loads(data.decode("utf-8"))
    except ValueError as e:
        raise ValueError(f"{path}: {e}") from None


HEAD = """// Built by fm scene compile (T-1633) from a scene.json: edit that and compile again. Needs three.js r155 or later,
// resolved as "three" by an import map or a bundler. Modelled on Foreman's templates/scene.html (references/ui/
// scene-3d.md): the page holds <figure class="scene" data-state="poster"> with the poster, a <canvas role="img"
// aria-label="..."> and the text twin, and its CSS fades the canvas in at data-state="live". Load it after first paint:
//   import("./scene.js").then(m => m.mount(figure)).catch(err => console.error("scene: showing the poster", err));
// mount() returns dispose(), which frees everything it made, the WebGL context included.
import * as THREE from "three";

"""

COMPONENT_HEAD = """// Built by fm scene compile --to component (T-1634) from a scene.json: edit that and compile again. Needs three.js
// r155 or later, resolved as "three" by an import map or a bundler. This is the three.js module (SCENE, mount()) plus
// <fm-scene>, a custom element mounting it in its own shadow DOM. The page holds <fm-scene label="what it shows">
// with the poster inside as <img slot="poster" alt=""> and the text twin after it, and loads this after first paint:
//   import("./scene.js").catch(err => console.error("scene: showing the poster", err));
// Until then, or with no WebGL, the poster and the twin show. The element's data-state (poster | live | lost |
// failed) is the first-frame flag; taking it out of the page frees all mount() made, the WebGL context included.
// No layout shift: the page's CSS gives it its box before it is defined (once defined, fm-scene::part(stage) sets the
// ratio):  fm-scene:not(:defined){display:block;position:relative;aspect-ratio:16/10}
//          fm-scene:not(:defined)>[slot=poster]{width:100%;height:100%;object-fit:cover}
import * as THREE from "three";

"""

RUNTIME = """
const RAD = Math.PI / 180;

function geometry(g) {
  if (g.type === "box") return new THREE.BoxGeometry(...g.size);
  if (g.type === "sphere") return new THREE.SphereGeometry(g.radius, g.segments, Math.max(2, g.segments >> 1));
  if (g.type === "plane") return new THREE.PlaneGeometry(...g.size);
  const geo = new THREE.BufferGeometry();  // vertices: smooth normals from the faces
  geo.setAttribute("position", new THREE.Float32BufferAttribute(g.vertices.flat(), 3));
  geo.setIndex(g.faces.flat());
  geo.computeVertexNormals();
  return geo;
}

function light(l) {
  if (l.type === "ambient") return new THREE.AmbientLight(l.color, l.intensity);
  if (l.type === "hemisphere") return new THREE.HemisphereLight(l.sky, l.ground, l.intensity);
  const o = new (l.type === "point" ? THREE.PointLight : THREE.DirectionalLight)(l.color, l.intensity);
  o.position.set(...l.position);  // a directional light shines from here toward the origin
  return o;
}

// Linear between keys, held outside them; a loop restarts at its last time.
function sample(a, t) {
  const ts = a.times, end = ts[ts.length - 1];
  if (a.loop && end > 0) t %= end;
  let i = 0;
  while (i < ts.length - 1 && ts[i + 1] <= t) i++;
  if (i === ts.length - 1 || t <= ts[i]) return a.values[i];
  const k = (t - ts[i]) / (ts[i + 1] - ts[i]);
  return a.values[i].map((v, j) => v + (a.values[i + 1][j] - v) * k);
}

export function mount(fig) {
  // A fresh canvas each mount: a context released by dispose() never comes back on its old canvas. fig: the page's
  // figure, or an <fm-scene> holding its canvas in its shadow root.
  const old = (fig.shadowRoot ?? fig).querySelector("canvas"), canvas = old.cloneNode(false), setState = s => { fig.dataset.state = s; };
  old.replaceWith(canvas);
  const off = new AbortController(), on = (target, type, fn) => target.addEventListener(type, fn, { signal: off.signal });
  // Survival 1: no WebGL2 (or only a software renderer) -> the poster and the text twin stay, nothing throws.
  const gl = canvas.getContext("webgl2", { antialias: true, alpha: true, powerPreference: "low-power", failIfMajorPerformanceCaveat: true });
  if (!gl) return () => {};
  const reduce = matchMedia("(prefers-reduced-motion: reduce)"), c = SCENE.camera, owned = [];
  const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(c.fov, 1, c.near, c.far);
  let renderer = null, anims = [], raf = 0, last = 0, time = 0, stopped = false, freed = false, visible = !document.hidden, onscreen = true;

  // Once, from fail() or dispose(): free what was made, then release the context (survival 4).
  const free = () => {
    if (freed) return; freed = true;
    for (const o of owned) o.dispose();
    if (renderer) { renderer.dispose(); renderer.forceContextLoss(); renderer = null; } else gl.getExtension("WEBGL_lose_context")?.loseContext();
  };
  // Survival 8: any failure ends at the poster, logged once; the freeing waits until three.js's own call has returned.
  const fail = err => { if (stopped) return; stopped = true; cancelAnimationFrame(raf); raf = 0; console.error("scene: showing the poster", err); setState("failed"); queueMicrotask(free); };
  const pose = t => { for (const a of anims) { const v = sample(a, t); a.mesh[a.property].set(...(a.property === "rotation" ? v.map(d => d * RAD) : v)); } camera.lookAt(...c.target); };
  try {
    renderer = new THREE.WebGLRenderer({ canvas, context: gl });
    renderer.debug.onShaderError = (g, p) => { if (!g.isContextLost()) fail(new Error(g.getProgramInfoLog(p) || "a shader failed to compile")); };
    renderer.toneMapping = THREE.ACESFilmicToneMapping;  // one tone mapper; the output stays sRGB, three's default
    renderer.setClearColor(SCENE.background ?? "#000000", SCENE.background ? 1 : 0);  // no seam: the page's colour, or none
    camera.position.set(...c.position); camera.lookAt(...c.target);
    const mats = new Map(Object.entries(SCENE.materials).map(([k, m]) => [k, new THREE.MeshStandardMaterial(m)]));
    const named = new Map();
    owned.push(...mats.values());
    for (const m of SCENE.meshes) {
      const geo = geometry(m.geometry), mesh = new THREE.Mesh(geo, mats.get(m.material));
      owned.push(geo);
      mesh.position.set(...m.position); mesh.rotation.set(...m.rotation.map(d => d * RAD)); mesh.scale.set(...m.scale);
      if (m.name) named.set(m.name, mesh);
      scene.add(mesh);
    }
    for (const l of SCENE.lights) scene.add(light(l));
    anims = Object.values(SCENE.animations).map(a => ({ ...a, mesh: a.target === "camera" ? camera : named.get(a.target) }));
    pose(0);
    renderer.compile(scene, camera);  // shaders compile before the reveal: no hitch once it shows
  } catch (err) { fail(err); }
  const moving = anims.length > 0;

  // Draw now; the first good frame fades the canvas in over the poster (survival 2).
  function render() {
    if (stopped || !renderer || gl.isContextLost()) return;
    try { renderer.render(scene, camera); } catch (err) { return fail(err); }
    if (!stopped && fig.dataset.state !== "live") setState("live");
  }
  // Survival 5: reduced motion holds the first pose and draws only when something changes.
  function frame(now) {
    raf = 0;
    const dt = Math.min((now - (last || now)) / 1000, 0.1); last = now;
    pose(reduce.matches ? 0 : (time += dt));
    render();
    if (moving && !reduce.matches) wake();
  }
  // Survival 9: no frames offscreen, in a hidden tab, or with nothing moving.
  function wake() { if (!raf && !stopped && visible && onscreen && renderer && !gl.isContextLost()) raf = requestAnimationFrame(frame); }
  function sleep() { cancelAnimationFrame(raf); raf = 0; last = 0; }

  // Budget: DPR capped at 2 (1.5 on touch screens); a resize redraws in the same callback, so no black frame.
  const ro = new ResizeObserver(() => {
    if (stopped || !renderer) return;
    const dpr = Math.min(window.devicePixelRatio || 1, matchMedia("(pointer: coarse)").matches ? 1.5 : 2);
    const w = Math.max(1, canvas.clientWidth), h = Math.max(1, canvas.clientHeight);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    render();
  });
  const io = new IntersectionObserver(entries => { onscreen = entries.at(-1).isIntersecting; onscreen ? wake() : sleep(); });  // oldest first
  on(document, "visibilitychange", () => { visible = !document.hidden; visible ? wake() : sleep(); });
  on(reduce, "change", wake);
  // Survival 3: preventDefault or the browser never restores; the poster covers the gap; three.js rebuilds its own state.
  on(canvas, "webglcontextlost", e => { e.preventDefault(); sleep(); if (!stopped) setState("lost"); });
  on(canvas, "webglcontextrestored", () => { render(); wake(); });
  ro.observe(canvas); io.observe(canvas); wake();
  // Survival 4 and 9: cancel the loop, remove the listeners, free what was made, release the context.
  return () => { off.abort(); ro.disconnect(); io.disconnect(); sleep(); stopped = true; free(); setState("poster"); };
}
"""


# <\/ in the markup: the module pasted into a <script> has nothing in it that closes the tag.
ELEMENT = r"""
// <fm-scene> (T-1634): mount() in a shadow DOM. The child with slot="poster" sits under the canvas; any other child
// (the text twin) shows below. The element itself carries data-state, so the page's CSS and tests read it there.
const SHADOW = `<style>
  :host { display: block; }
  .stage { position: relative; aspect-ratio: 16 / 10; }
  @media (max-aspect-ratio: 3/4) { .stage { aspect-ratio: 4 / 5; } }
  ::slotted([slot="poster"]), canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  ::slotted([slot="poster"]) { object-fit: cover; }
  canvas { opacity: 0; touch-action: pan-y; pointer-events: none; }
  :host([data-state="live"]) canvas { opacity: 1; pointer-events: auto; transition: opacity 400ms ease-out; }
  @media (prefers-reduced-motion: reduce) { :host([data-state="live"]) canvas { transition: none; } }
<\/style><div class="stage" part="stage"><slot name="poster"><\/slot><canvas role="img"><\/canvas><\/div><slot><\/slot>`;

export class FmScene extends HTMLElement {
  static observedAttributes = ["label"];
  #dispose = null;
  connectedCallback() {
    // A root the page declared (<template shadowrootmode>) is kept, filled in if it has no canvas.
    const root = this.shadowRoot ?? this.attachShadow({ mode: "open" });
    if (!root.querySelector("canvas")) root.innerHTML = SHADOW;
    this.#label();
    this.dataset.state = "poster";
    this.#dispose = mount(this);
  }
  // label="..." names the canvas (an id reference can't cross the shadow boundary); with none, the twin speaks. It is
  // watched (T-1706): a page that changes it, or takes it away, is heard.
  attributeChangedCallback() { this.#label(); }
  #label() {
    const canvas = this.shadowRoot?.querySelector("canvas"), label = this.getAttribute("label");
    if (!canvas) return;  // not connected yet: connectedCallback names it
    if (label) { canvas.setAttribute("aria-label", label); canvas.removeAttribute("aria-hidden"); }
    else { canvas.removeAttribute("aria-label"); canvas.setAttribute("aria-hidden", "true"); }
  }
  // Out of the page: all mount() made is freed and the context released; put back, it mounts on a fresh canvas.
  disconnectedCallback() { this.#dispose?.(); this.#dispose = null; }
}
// Two scenes on one page: the second finds fm-scene taken and needs a name of its own, in its markup too.
if (!customElements.get("fm-scene")) customElements.define("fm-scene", FmScene);
else console.warn("scene: <fm-scene> is taken; compile this one with fm scene compile --to component --tag NAME");
"""
# T-1706: a valid custom element name (ASCII: a lowercase letter first, a hyphen in it), none the HTML spec reserves
TAG = re.compile(r"[a-z][a-z0-9._]*-[a-z0-9._-]*")
RESERVED_TAGS = {"annotation-xml", "color-profile", "font-face", "font-face-src", "font-face-uri", "font-face-format",
                 "font-face-name", "missing-glyph"}


# T-1530: fm scene compile --hud adds this dev overlay: the frame rate and what three.js holds, over the canvas, and the
# same numbers as globalThis.__fmScene for a test or a soak to read. A development build only.
HUD = """
// --hud (T-1530): a dev overlay, not for production: the frame rate twice a second, draw calls, triangles, geometries
// and textures; globalThis.__fmScene holds the same and each render's milliseconds (the last 2,000), for a soak to read.
function hud(renderer, fig, ms) {
  const el = hud.el ??= Object.assign(document.createElement("output"), { className: "fm-scene-hud" });
  if (!el.isConnected) {
    el.style.cssText = "position:absolute;top:4px;left:4px;z-index:9;font:11px/1.3 ui-monospace,monospace;color:#fff;background:#000b;padding:2px 6px;pointer-events:none;white-space:pre";
    (fig.shadowRoot?.querySelector(".stage") ?? fig).append(el);
  }
  const now = performance.now(), info = renderer.info, times = hud.ms ??= [];
  times.push(ms); if (times.length > 2000) times.shift();
  hud.n = (hud.n ?? 0) + 1; hud.t ??= now; hud.frames = (hud.frames ?? 0) + 1;
  const s = globalThis.__fmScene = { fps: hud.fps ?? 0, frames: hud.frames, calls: info.render.calls,
    triangles: info.render.triangles, geometries: info.memory.geometries, textures: info.memory.textures, frame_ms: times };
  if (now - hud.t < 500) return;
  s.fps = hud.fps = Math.round(hud.n * 1000 / (now - hud.t)); hud.n = 0; hud.t = now;
  el.textContent = `${s.fps} fps  ${s.calls} calls  ${s.triangles} triangles\\n${s.geometries} geometries  ${s.textures} textures`;
}
"""
RENDER_CALL = "try { renderer.render(scene, camera); }"
TIMED_CALL = "try { const t0 = performance.now(); renderer.render(scene, camera); hud(renderer, fig, performance.now() - t0); }"


def compile_three(scene, head=HEAD, tail="", hud=False):
    """A validated scene → the ES module's text: SCENE (one top-level key a line), then the runtime that builds it.
    The same scene gives the same bytes, so a second compile changes nothing. hud (T-1530): with the dev overlay."""
    body = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, separators=(',', ':'))}" for k, v in scene.items())
    runtime = RUNTIME.replace(RENDER_CALL, TIMED_CALL) + HUD \
        if hud else RUNTIME
    return head + "export const SCENE = {\n" + body + "\n};\n" + runtime + tail


def compile_component(scene, tag="fm-scene", hud=False):
    """A validated scene → compile_three's module, the same SCENE and mount(), with <fm-scene> defined after it, or
    the custom element name tag (T-1706: two scenes on one page, each its own)."""
    if not TAG.fullmatch(tag) or tag in RESERVED_TAGS:
        raise ValueError(f"--tag {tag!r} isn't a custom element name: lowercase ASCII, a letter first, a hyphen in it "
                         "(pebble-scene), and none the HTML spec reserves (font-face, …)")
    return compile_three(scene, COMPONENT_HEAD.replace("fm-scene", tag), ELEMENT.replace("fm-scene", tag), hud)


# T-1530: offline checks: no browser, no GPU
def _rot(p, deg):
    """p turned by Rx * Ry * Rz (three.js's Euler order XYZ: on a point, Z turns first), angles in degrees."""
    x, y, z = p
    ax, ay, az = (math.radians(d) for d in deg)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    return x, y, z


def _cross3(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]


def _unit(v):
    n = math.sqrt(sum(a * a for a in v))
    return tuple(a / n for a in v)


def faces(g):
    """A geometry's triangles in its own space, front faces counter-clockwise seen from outside, as three.js builds
    them (a sphere's poles drop their empty triangles)."""
    if g["type"] == "vertices":
        return [tuple(tuple(g["vertices"][i]) for i in f) for f in g["faces"]]
    if g["type"] == "plane":
        w, h = (s / 2 for s in g["size"])
        q = [(-w, -h, 0), (w, -h, 0), (w, h, 0), (-w, h, 0)]
        return [(q[0], q[1], q[2]), (q[0], q[2], q[3])]
    if g["type"] == "box":
        half, tris = [s / 2 for s in g["size"]], []
        for i in range(3):
            j, k = (i + 1) % 3, (i + 2) % 3
            for s in (1, -1):  # the face whose outward normal is s along axis i: u along j, v along s * k
                q = []
                for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                    p = [0.0, 0.0, 0.0]
                    p[i], p[j], p[k] = s * half[i], a * half[j], s * b * half[k]
                    q.append(tuple(p))
                tris += [(q[0], q[1], q[2]), (q[0], q[2], q[3])]
        return tris
    r, ws = g["radius"], g["segments"]
    hs = max(2, ws >> 1)
    grid = [[(-r * math.cos(2 * math.pi * u / ws) * math.sin(math.pi * v / hs), r * math.cos(math.pi * v / hs),
              r * math.sin(2 * math.pi * u / ws) * math.sin(math.pi * v / hs)) for u in range(ws + 1)]
            for v in range(hs + 1)]
    tris = []
    for v in range(hs):
        for u in range(ws):
            for t in ((grid[v][u], grid[v + 1][u], grid[v + 1][u + 1]), (grid[v][u], grid[v + 1][u + 1], grid[v][u + 1])):
                n = _cross3([b - a for a, b in zip(t[0], t[1])], [c - a for a, c in zip(t[0], t[2])])
                if any(abs(x) > 1e-12 for x in n):
                    out = sum(x * y for x, y in zip(n, (sum(p[i] for p in t) for i in range(3)))) > 0
                    tris.append(t if out else (t[0], t[2], t[1]))
    return tris


def triangles(scene, turn=0.0, unit=1000):
    """T-1530: the scene's meshes as fmraster triangles: each mesh's T * R * S, then the world turned `turn` degrees
    about +Y (a turntable), seen from its camera, in integer units of 1/unit. From three.js's view space the depth is
    negated and two vertices swapped, as fmraster's docstring says, so its front faces stay front faces."""
    cam = scene["camera"]
    eye = cam["position"]
    f = _unit([t - e for t, e in zip(cam["target"], eye)])
    r = _unit(_cross3(f, (0, 1, 0)))
    up = _cross3(r, f)
    out = []
    for m in scene["meshes"]:
        hexc = scene["materials"][m["material"]]["color"]
        colour = tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
        for tri in faces(m["geometry"]):
            pts = []
            for p in tri:
                p = _rot([a * s for a, s in zip(p, m["scale"])], m["rotation"])
                p = _rot([a + b for a, b in zip(p, m["position"])], (0, turn, 0))
                d = [a - e for a, e in zip(p, eye)]
                pts.append(tuple(round(sum(x * y for x, y in zip(d, axis)) * unit) for axis in (r, up, f)))
            out.append((pts[0], pts[2], pts[1], colour))
    return out


def turntable(scene, frames=8, size=(160, 100), cols=4):
    """T-1530: a contact sheet of the scene turned about +Y in `frames` even steps, drawn by fmraster (flat shading,
    no browser or GPU): (width, height, RGB bytes), frames left to right then down. ponytail: pure Python, about a
    second a megapixel; a scene of many thousand triangles takes a while."""
    w, h = size
    bg = _background(scene)
    tiles = [_frame(scene, 360 * k / frames, w, h) for k in range(frames)]
    cols = min(cols, frames)
    rows = -(-frames // cols)
    sheet = bytearray(bytes(bg) * (w * cols * h * rows))
    for k, tile in enumerate(tiles):
        x0, y0 = (k % cols) * w, (k // cols) * h
        for y in range(h):
            at = ((y0 + y) * w * cols + x0) * 3
            sheet[at:at + w * 3] = tile[y * w * 3:(y + 1) * w * 3]
    return w * cols, h * rows, bytes(sheet)


def _background(scene):
    return tuple(int(scene["background"][i:i + 2], 16) for i in (1, 3, 5)) if scene["background"] else (0, 0, 0)


def _frame(scene, turn, w, h):
    """One w x h RGB frame of the scene turned `turn` degrees about +Y, drawn by fmraster from its camera."""
    import fmraster
    focal = max(1, round(h / 2 / math.tan(math.radians(scene["camera"]["fov"]) / 2)))
    return fmraster.render(triangles(scene, turn), w, h, focal=focal, background=_background(scene))


def cells(scene, cols=64, turn=0.0):
    """T-1635: the scene as terminal text: cols x (cols * 5/8, down to even) pixels from fmraster, two to a cell as
    an upper half block, the top pixel its 24-bit foreground and the bottom its background; one string per row of
    cells, each ending in a reset. ponytail: every cell carries both colours, about 40 bytes; truecolor only."""
    if not 2 <= cols <= 400:
        raise ValueError(f"--cols {cols}: 2 to 400")
    h = max(2, cols * 5 // 8 // 2 * 2)
    rgb = _frame(scene, turn, cols, h)
    lines = []
    for y in range(0, h, 2):
        row = []
        for x in range(cols):
            a, b = 3 * (y * cols + x), 3 * ((y + 1) * cols + x)
            row.append("\x1b[38;2;%d;%d;%dm\x1b[48;2;%d;%d;%dm\u2580" % (*rgb[a:a + 3], *rgb[b:b + 3]))
        lines.append("".join(row) + "\x1b[0m")
    return lines


GLSL = re.compile(r"```glsl\n(.*?)```", re.S)
SHADER_FILES = (".frag", ".vert", ".glsl")


def shader_problems(path, validator=None):
    """T-1530: offline checks of a shader card (looks/shader-*.md) or a .frag/.vert/.glsl file: each GLSL block has a
    main and compiles under glslangValidator when one is given (its stage from gl_Position: vertex, else fragment),
    and a card declares exactly the uniforms its ## Uniforms table lists. [problem], empty when it passes."""
    import subprocess
    import tempfile
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    blocks = GLSL.findall(text) if path.endswith(".md") else [text]
    name = os.path.basename(path)
    if not blocks:  # a guidance card (shader-performance) or an empty file: nothing to compile
        return [] if path.endswith(".md") else [f"{name}: empty"]
    problems, declared = [], set()
    for n, block in enumerate(blocks, 1):
        where = f"{name} block {n}" if len(blocks) > 1 else name
        if not re.search(r"\bvoid\s+main\s*\(", block):
            problems.append(f"{where}: no void main()")
        for decl in re.findall(r"\buniform\s+\w+\s+([^;{]+);", block):
            declared |= {re.sub(r"\[.*", "", x).strip() for x in decl.split(",")}
        if validator:
            stage = "vert" if "gl_Position" in block else "frag"
            with tempfile.TemporaryDirectory(prefix="fm-shader-") as tmp:
                src = os.path.join(tmp, f"shader.{stage}")
                with open(src, "w", encoding="utf-8") as fh:
                    fh.write(block)
                try:
                    r = subprocess.run([validator, src], capture_output=True, text=True, timeout=30,
                                       stdin=subprocess.DEVNULL)
                except (OSError, subprocess.SubprocessError) as e:
                    problems.append(f"{where}: {validator} didn't run ({e})")
                    continue
            if r.returncode:
                said = [x.strip() for x in (r.stdout + r.stderr).splitlines() if "ERROR" in x]
                problems.append(f"{where}: doesn't compile as GLSL ({stage}): "
                                + "; ".join(x.replace(src, "shader") for x in said[:3]))
    table = re.search(r"(?ms)^## Uniforms\n(.*?)(?=^## |\Z)", text) if path.endswith(".md") else None
    if table:
        listed = {x for row in table.group(1).splitlines() if row.startswith("| `")
                  for x in re.findall(r"`(\w+)`", row.split("|")[1])}
        problems += [f"{name}: the Uniforms table lists {u}, which no block declares" for u in sorted(listed - declared)]
        problems += [f"{name}: {u} is declared but not in the Uniforms table" for u in sorted(declared - listed)]
    return problems


def shader_paths(path):
    """The shader cards and files a path names: itself, or the shader-*.md and GLSL files under a folder."""
    if not os.path.isdir(path):
        return [path]
    return sorted(os.path.join(d, f) for d, _, fs in os.walk(path) for f in fs
                  if f.endswith(SHADER_FILES) or f.startswith("shader-") and f.endswith(".md"))


GLTF_MAX = 256 << 20  # bytes of a .gltf or .glb read at most
COMPONENT = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
WIDTH = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT2": 4, "MAT3": 9, "MAT4": 16}


def gltf_problems(path):
    """T-1530: offline structural checks of a .gltf or .glb: the GLB header and chunks, asset.version 2.x, every index
    in range (scene nodes, node children and meshes, primitive accessors and materials, accessor views, view buffers),
    each accessor inside its view, each view inside its buffer, and each buffer as long as it says (a .glb's BIN chunk,
    a base64 data URI, or a file beside it: a URI leaving the asset's folder is a problem, never read). [problem]"""
    name = os.path.basename(path)
    with open(path, "rb") as f:
        data = f.read(GLTF_MAX + 1)
    if len(data) > GLTF_MAX:
        return [f"{name}: over {GLTF_MAX >> 20} MB"]
    problems, chunk = [], None
    if data[:4] == b"glTF" or path.lower().endswith(".glb"):
        if len(data) < 20 or data[:4] != b"glTF":
            return [f"{name}: not a GLB (no glTF magic)"]
        version, length = struct.unpack_from("<II", data, 4)
        if version != 2:
            problems.append(f"{name}: GLB version {version}, not 2")
        if length != len(data):
            problems.append(f"{name}: the header says {length} bytes; the file has {len(data)}")
        size, kind = struct.unpack_from("<II", data, 12)
        if kind != 0x4E4F534A:
            return problems + [f"{name}: the first chunk isn't JSON"]
        text, at = data[20:20 + size], 20 + size
        if at + 8 <= len(data) and struct.unpack_from("<II", data, at)[1] == 0x004E4942:
            chunk = len(data[at + 8:at + 8 + struct.unpack_from("<I", data, at)[0]])
    else:
        text = data
    try:
        doc = json.loads(text)
    except (ValueError, RecursionError) as e:
        return problems + [f"{name}: not JSON ({str(e)[:80]})"]
    if not isinstance(doc, dict):
        return problems + [f"{name}: not a glTF object"]
    version = str((doc.get("asset") or {}).get("version", "")) if isinstance(doc.get("asset"), dict) else ""
    if not version.startswith("2."):
        problems.append(f"{name}: asset.version is {version!r}, not 2.x")

    def rows(key):
        got = doc.get(key, [])
        return [x if isinstance(x, dict) else {} for x in got] if isinstance(got, list) else []

    def index(where, i, key):
        n = len(rows(key))
        if not (isinstance(i, int) and not isinstance(i, bool) and 0 <= i < n):
            problems.append(f"{name}: {where}: {key} index {i!r} out of range ({f'0-{n - 1}' if n else 'there are none'})")
            return False
        return True

    for s, sc in enumerate(rows("scenes")):
        for i in sc.get("nodes", []):
            index(f"scenes[{s}].nodes", i, "nodes")
    for n, node in enumerate(rows("nodes")):
        for i in node.get("children", []):
            index(f"nodes[{n}].children", i, "nodes")
        if "mesh" in node:
            index(f"nodes[{n}].mesh", node["mesh"], "meshes")
    for m, mesh in enumerate(rows("meshes")):
        for k, prim in enumerate(mesh.get("primitives", [])):
            prim = prim if isinstance(prim, dict) else {}
            for attr, i in (prim.get("attributes") or {}).items():
                index(f"meshes[{m}].primitives[{k}].{attr}", i, "accessors")
            for key, rows_of in (("indices", "accessors"), ("material", "materials")):
                if key in prim:
                    index(f"meshes[{m}].primitives[{k}].{key}", prim[key], rows_of)
    folder, lengths = os.path.dirname(os.path.abspath(path)), []
    for b, buf in enumerate(rows("buffers")):
        uri, has = buf.get("uri"), None
        if uri is None:
            has = chunk if b == 0 else None
        elif isinstance(uri, str) and uri.startswith("data:"):
            try:
                has = len(base64.b64decode(uri.split(",", 1)[1], validate=True))
            except (IndexError, ValueError):
                problems.append(f"{name}: buffers[{b}]: its data URI isn't base64")
        elif isinstance(uri, str):
            target = os.path.realpath(os.path.join(folder, uri))
            if os.path.isabs(uri) or not target.startswith(os.path.realpath(folder) + os.sep):
                problems.append(f"{name}: buffers[{b}]: {uri} is outside the asset's folder")
            elif not os.path.isfile(target):
                problems.append(f"{name}: buffers[{b}]: {uri} isn't there")
            else:
                has = os.path.getsize(target)
        want = buf.get("byteLength")
        if has is not None and isinstance(want, int) and has < want:
            problems.append(f"{name}: buffers[{b}] declares {want} bytes, has {has}")
        lengths.append(want if isinstance(want, int) else 0)
    views = rows("bufferViews")
    for v, view in enumerate(views):
        if index(f"bufferViews[{v}].buffer", view.get("buffer"), "buffers"):
            end = (view.get("byteOffset") or 0) + (view.get("byteLength") or 0)
            if end > lengths[view["buffer"]]:
                problems.append(f"{name}: bufferViews[{v}] ends at byte {end} of buffers[{view['buffer']}], which "
                                f"has {lengths[view['buffer']]}")
    for a, acc in enumerate(rows("accessors")):
        if "bufferView" not in acc or not index(f"accessors[{a}].bufferView", acc["bufferView"], "bufferViews"):
            continue
        size = COMPONENT.get(acc.get("componentType"), 0) * WIDTH.get(acc.get("type"), 0)
        view, count = views[acc["bufferView"]], acc.get("count") or 0
        if not size:
            problems.append(f"{name}: accessors[{a}]: componentType {acc.get('componentType')!r} or type "
                            f"{acc.get('type')!r} isn't glTF's")
        elif count > 0:
            need = (acc.get("byteOffset") or 0) + (view.get("byteStride") or size) * (count - 1) + size
            if need > (view.get("byteLength") or 0):
                problems.append(f"{name}: accessors[{a}] needs {need} bytes of bufferViews[{acc['bufferView']}], "
                                f"which has {view.get('byteLength') or 0}")
    return problems


def find_three(*starts):
    """T-1530: a three.js build for the soak: FOREMAN_THREE (its three.module.js), else node_modules/three/build/ in a
    start folder or above it; None when there's none."""
    env = os.environ.get("FOREMAN_THREE")
    if env:
        return env if os.path.isfile(env) else None
    for start in starts:
        d = os.path.abspath(start)
        while True:
            hit = os.path.join(d, "node_modules", "three", "build", "three.module.js")
            if os.path.isfile(hit):
                return hit
            if os.path.dirname(d) == d:
                break
            d = os.path.dirname(d)
    return None


SOAK_PAGE = """<!doctype html><meta charset="utf-8"><title>fm scene soak</title>
<style>html,body{margin:0;background:#000}figure{margin:0;position:relative;width:640px;height:400px}
canvas{position:absolute;inset:0;width:100%;height:100%}</style>
<script type="importmap">{"imports": {"three": "./three/three.module.js"}}</script>
<figure class="scene" data-state="poster"><canvas role="img" aria-label="soak"></canvas></figure>
<script>
// The soak's own shim, never the module's: headless Chrome draws WebGL with SwiftShader, which the module's
// failIfMajorPerformanceCaveat refuses on purpose (a real page keeps its poster rather than draw in software).
const getContext = HTMLCanvasElement.prototype.getContext;
HTMLCanvasElement.prototype.getContext = function (kind, attrs) {
  return getContext.call(this, kind, attrs && { ...attrs, failIfMajorPerformanceCaveat: false });
};
import("./scene.js").then(m => { window.__dispose = m.mount(document.querySelector("figure")); },
                          e => { window.__error = String(e && e.stack || e); });
</script>
"""
SAMPLE = ("JSON.stringify({s: globalThis.__fmScene ? {...globalThis.__fmScene, frame_ms: undefined, "
          "ms: globalThis.__fmScene.frame_ms.slice()} : null, state: document.querySelector('figure').dataset.state, "
          "error: window.__error ?? null, heap: performance.memory ? performance.memory.usedJSHeapSize : null})")


def _p95(times):
    return sorted(times)[max(0, -(-len(times) * 95 // 100) - 1)] if times else None


def soak_problems(samples, after, budget_ms=None):
    """T-1530: the soak's verdict from its samples ({state, s: __fmScene or None, error}) and the state after
    dispose(): it drew, its geometries and textures held steady (growth is a leak), the p95 frame time is within
    budget_ms when one is given, and dispose() put the poster back."""
    drawn = [x for x in samples if x.get("s")]
    if not drawn:
        last = samples[-1] if samples else {}
        return [f"it never drew (state {last.get('state')!r}{': ' + str(last.get('error'))[:200] if last.get('error') else ''})"]
    first, last, problems = drawn[0]["s"], drawn[-1]["s"], []
    for key in ("geometries", "textures"):
        if last.get(key, 0) > first.get(key, 0):
            problems.append(f"{key} grew from {first.get(key, 0)} to {last.get(key, 0)} while it ran: a leak")
    p95 = _p95(last.get("frame_ms") or last.get("ms") or [])
    if budget_ms is not None and p95 is not None and p95 > budget_ms:
        problems.append(f"p95 frame time {p95:g} ms is over the {budget_ms:g} ms budget")
    if after != "poster":
        problems.append(f"still {after} after dispose(): it should be back at the poster")
    return problems


def soak(path, three, seconds=10, budget_ms=None):
    """T-1530: the scene compiled with --hud, mounted in headless Chrome (SwiftShader, through fmshot) from a local
    server on 127.0.0.1, sampled once a second for `seconds`, then disposed: {frames, p95_ms, geometries, textures,
    heap, after, problems}, or {skipped: why} with no browser or no three.js build. Optional: nothing is installed."""
    import functools
    import http.server
    import shutil
    import tempfile
    import threading
    import time
    import fmshot
    scene = load(path)
    browser, why = fmshot.find_browser("fm scene soak")
    if not browser:
        return {"skipped": why}
    if not three or not os.path.isfile(three):
        return {"skipped": "no three.js build: set FOREMAN_THREE to a three.module.js, or install three in "
                           "node_modules beside the scene"}
    with tempfile.TemporaryDirectory(prefix="fm-soak-") as tmp:
        os.makedirs(os.path.join(tmp, "three"))
        for part in ("three.module.js", "three.core.js"):  # r170+ splits the build in two
            src = os.path.join(os.path.dirname(three), part)
            if os.path.isfile(src):
                shutil.copyfile(src, os.path.join(tmp, "three", part))
        with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as f:
            f.write(SOAK_PAGE)
        with open(os.path.join(tmp, "scene.js"), "w", encoding="utf-8") as f:
            f.write(compile_three(scene, hud=True))

        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=tmp))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        b, samples, after = None, [], None
        try:
            b = fmshot.Browser(browser, (640, 400))
            fmshot.load(b, f"http://127.0.0.1:{server.server_address[1]}/index.html")

            def ask(expr):
                got = b.call("Runtime.evaluate", b.sid, expression=expr, returnByValue=True)
                return (got.get("result") or {}).get("value")
            end = time.monotonic() + seconds
            while True:
                samples.append(json.loads(ask(SAMPLE) or "{}"))
                if time.monotonic() >= end:
                    break
                time.sleep(1)
            after = ask("window.__dispose && window.__dispose(), document.querySelector('figure').dataset.state")
        finally:
            if b:
                b.close()
            server.shutdown()
            server.server_close()
    for x in samples:
        if x.get("s"):
            x["s"]["frame_ms"] = x["s"].pop("ms", [])
    drawn = [x["s"] for x in samples if x.get("s")]
    p95 = _p95(drawn[-1]["frame_ms"]) if drawn else None
    return {"frames": drawn[-1]["frames"] if drawn else 0, "p95_ms": None if p95 is None else round(p95, 2),
            "geometries": [x["geometries"] for x in drawn], "textures": [x["textures"] for x in drawn],
            "heap": [x.get("heap") for x in samples], "after": after,
            "problems": soak_problems(samples, after, budget_ms)}


def cmd_scene(args):
    import sys
    import fmcli
    import fmcore
    if args.action == "shader":  # T-1530: GLSL checks with no browser; glslangValidator when it's installed
        import shutil
        validator = shutil.which("glslangValidator")
        paths = shader_paths(args.path)
        try:
            found = [p for path in paths for p in shader_problems(path, validator)]
        except (OSError, UnicodeDecodeError) as e:
            print(f"fm: scene: {e}", file=sys.stderr)
            return 2
        fmcli.out(args, {"checked": paths, "problems": found, "compiled": bool(validator)},
                  "\n".join([f"✗ {x}" for x in found] + [
                      f"{'✗' if found else '✓'} {len(paths)} shader file(s), {len(found)} problem(s)"
                      + ("" if validator else " (glslangValidator not found: compiling skipped, the rest checked)")]))
        return 1 if found else 0
    if args.action == "check" and args.path.lower().endswith((".gltf", ".glb")):  # T-1530: a glTF asset, offline
        try:
            found = gltf_problems(args.path)
        except OSError as e:
            print(f"fm: scene: {e}", file=sys.stderr)
            return 2
        fmcli.out(args, {"problems": found}, "\n".join([f"✗ {x}" for x in found] + [
            f"{'✗' if found else '✓'} {args.path}: {len(found)} problem(s)"]))
        return 1 if found else 0
    if args.action == "soak":  # T-1530: a real browser when there is one; skipped with the reason when not
        if not 1 <= args.seconds <= 600:
            print(f"fm: scene: soak: --seconds {args.seconds}: 1 to 600", file=sys.stderr)
            return 2
        try:
            got = soak(args.path, find_three(os.path.dirname(os.path.abspath(args.path)), os.getcwd()),
                       args.seconds, args.budget_ms)
        except (OSError, ValueError, RuntimeError, TimeoutError) as e:
            print(f"fm: scene: soak: {e}", file=sys.stderr)
            return 2
        if "skipped" in got:
            fmcli.out(args, got, f"skipped: {got['skipped']}")
            return 0
        fmcli.out(args, got, "\n".join([f"✗ {x}" for x in got["problems"]] + [
            f"{'✗' if got['problems'] else '✓'} soak {args.seconds} s: {got['frames']} frames, p95 "
            f"{got['p95_ms'] if got['p95_ms'] is not None else '?'} ms, geometries "
            f"{'→'.join(map(str, sorted(set(got['geometries']), key=got['geometries'].index)))}, after dispose "
            f"{got['after']}"]))
        return 1 if got["problems"] else 0
    if args.action in ("check", "turntable", "cells"):  # T-1530, T-1635
        try:
            scene = load(args.path)
            if args.action == "cells":
                lines = cells(scene, args.cols, args.turn)
                return fmcli.out(args, {"cols": args.cols, "rows": len(lines), "lines": lines}, "\n".join(lines)) or 0
            if args.action == "check":
                tris = sum(len(faces(m["geometry"])) for m in scene["meshes"])
                return fmcli.out(args, {"meshes": len(scene["meshes"]), "triangles": tris,
                                        "lights": len(scene["lights"]), "animations": len(scene["animations"])},
                                 f"✓ {args.path}: {len(scene['meshes'])} mesh(es), {tris} triangles, "
                                 f"{len(scene['lights'])} light(s), {len(scene['animations'])} animation(s)") or 0
            if not args.out:
                raise ValueError("turntable writes a PNG: give --out PATH")
            if not 1 <= args.frames <= 36:
                raise ValueError(f"--frames {args.frames}: 1 to 36")
            w, h, rgb = turntable(scene, args.frames)
            import fmimg
            fmimg.save(args.out, w, h, rgb, "rgb")
        except (OSError, ValueError) as e:
            print(f"fm: scene: {e}", file=sys.stderr)
            return 2
        return fmcli.out(args, {"out": args.out, "frames": args.frames, "size": [w, h]},
                         f"wrote {args.out}: {args.frames} turns of {args.path}, {w}x{h}") or 0
    try:
        tag = getattr(args, "tag", None)
        if tag and args.to != "component":
            raise ValueError("--tag names the element: use it with --to component")
        scene = load(args.path)
        hud = getattr(args, "hud", False)
        text = compile_component(scene, tag or "fm-scene", hud) if args.to == "component" else \
            compile_three(scene, hud=hud)
        out = os.path.abspath(args.out) if args.out else None  # write_atomic makes dirname(path): "" for a bare name
        if out and os.path.exists(out) and os.path.samefile(out, args.path):
            raise ValueError(f"--out {args.out} is the scene it compiles")
        if out:
            fmcore.write_atomic(out, text)  # through a temp file: a symlink at out is replaced, never written through
    except (OSError, ValueError) as e:
        print(f"fm: scene: {e}", file=sys.stderr)
        return 2
    if out:
        fmcli.out(args, {"out": args.out, "bytes": len(text.encode())}, f"wrote {args.out}")
    else:
        fmcli.out(args, {"module": text}, text.rstrip("\n"))
    return 0
