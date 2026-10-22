"""fm scene (T-1633): scene.json, a 3D scene described once as plain data, checked and compiled to a three.js module.

validate() returns the scene with every default filled in: one shape for each renderer that reads it (three.js here;
a rasteriser or a web component later reads the same dict). compile_three() emits an ES module modelled on
references/ui/templates/scene.html: no WebGL keeps the poster, context loss is survived, the DPR is capped, reduced
motion holds one still frame, nothing draws offscreen or hidden, a failure ends at the poster, dispose() frees it all.
"""
import json
import math
import os
import re
import stat

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
  animations  {name: {target: a mesh's name; property: position | rotation | scale; times: [seconds, rising];
              values: [[x,y,z], ...], one per time; loop: true}}: linear between keys, held outside them; a loop
              restarts at its last time, so its last value should equal its first (or turn a whole 360)
What a second renderer must not guess (three.js's conventions; world space is right-handed with +Y up):
  rotation    the matrix is Rx * Ry * Rz (three.js's Euler order "XYZ"), so on a point Z turns first
  transform   a mesh's model matrix is T * R * S: scale, then rotate, then move
  camera      its up is +Y and it looks down -Z of its own frame, toward target (one straight above or below is
              refused); a renderer whose view space looks along +z, as fmraster's does, negates view-space z
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
        if target not in names:
            _fail(f"{w}.target", f"no mesh named {target}")
        prop = a["property"]
        if prop not in PROPERTIES:
            _fail(f"{w}.property", f"wants {' | '.join(PROPERTIES)}, not {_show(prop)}")
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
    try:
        data = json.loads(text.removeprefix("﻿"), object_pairs_hook=_pairs, parse_constant=_constant)
    except RecursionError:
        raise ValueError("nested too deeply") from None
    return validate(data)


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
  // A fresh canvas each mount: a context released by dispose() never comes back on its old canvas.
  const old = fig.querySelector("canvas"), canvas = old.cloneNode(false), setState = s => { fig.dataset.state = s; };
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
  const pose = t => { for (const a of anims) { const v = sample(a, t); a.mesh[a.property].set(...(a.property === "rotation" ? v.map(d => d * RAD) : v)); } };
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
    anims = Object.values(SCENE.animations).map(a => ({ ...a, mesh: named.get(a.target) }));
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


def compile_three(scene):
    """A validated scene → the ES module's text: SCENE (one top-level key a line), then the runtime that builds it.
    The same scene gives the same bytes, so a second compile changes nothing."""
    body = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, separators=(',', ':'))}" for k, v in scene.items())
    return HEAD + "export const SCENE = {\n" + body + "\n};\n" + RUNTIME


def cmd_scene(args):
    import sys
    import fmcli
    import fmcore
    try:
        text = compile_three(load(args.path))  # --to has one target, three, until T-1634 adds component
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
