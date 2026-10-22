// T-1610: the hero's proof chain, alive. build.py inlines this as a module script after the poster it sits over; it
// loads nothing. From plugin/skills/playbooks/references/ui/templates/scene.html (ui/scene-3d.md): raw WebGL2, the
// survival contract kept. The scene reads its stations from the poster on show (the 4-wide row, or the 2x2 under
// 720px), so it matches the still exactly: each 45° diamond becomes a lit octahedron (seen face-on, the same
// diamond), and a pulse of light runs the track, red where the work starts and green where it is proved, lighting
// each station as it passes; the station makes one quarter turn, which leaves it as it was. One pass when the hero
// comes into view, then no frames at all. The box's data-state: poster (no script yet) | live | still (reduced
// motion) | no-webgl2 | lost | failed; anything but live shows the poster.
const box = document.querySelector(".hero-scene");
const reduce = matchMedia("(prefers-reduced-motion: reduce)");
const PASS = 4.2, FADE = 1.4, LEAD = 0.6, TRAIL = 120;  // seconds: the run, its fade, the wait after a fade-in; units

const TO_SRGB = `vec3 toSrgb(vec3 c) { return mix(c * 12.92, 1.055 * pow(max(c, 1e-6), vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c)); }
float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }`;
// The track, one quad per row in the poster's units: a 4-unit round-capped line, the trail behind the head tinted
// by where it ran, and the head's soft light. Premultiplied out, since the canvas is see-through.
const TRACK_VS = `#version 300 es
uniform vec4 uBox;  // x0, y0, x1, y1
uniform vec2 uView;
out vec2 vP;
void main() { vP = mix(uBox.xy, uBox.zw, vec2(gl_VertexID & 1, gl_VertexID >> 1));
  gl_Position = vec4(2.0 * vP.x / uView.x - 1.0, 1.0 - 2.0 * vP.y / uView.y, 0.0, 1.0); }`;
const TRACK_FS = `#version 300 es
precision highp float;
in vec2 vP;
uniform vec4 uRow;   // x1, x2, y, the chain length before this row
uniform vec3 uHead;  // the head's place along the chain, the chain's length, its light (0-1)
uniform float uPx;   // poster units per device pixel
uniform vec3 uRule, uStop, uMid, uOk;  // linear
out vec4 outColor;
${TO_SRGB}
vec3 chain(float u) { return u < 0.5 ? mix(uStop, uMid, u * 2.0) : mix(uMid, uOk, u * 2.0 - 1.0); }
void main() {
  float x = clamp(vP.x, uRow.x, uRow.y), along = uRow.w + x - uRow.x, behind = uHead.x - along;
  float line = clamp((2.0 - length(vP - vec2(x, uRow.z))) / uPx + 0.5, 0.0, 1.0);
  float trail = behind >= 0.0 ? exp(-behind / ${TRAIL.toFixed(1)}) * uHead.z : 0.0;
  vec3 base = mix(uRule, chain(along / uHead.y), trail * (2.0 - trail));  // eased, or a light page washes it out
  float here = step(uRow.w, uHead.x) * step(uHead.x, uRow.w + uRow.y - uRow.x);
  float r = length(vP - vec2(uRow.x + uHead.x - uRow.w, uRow.z));
  float head = here * uHead.z * clamp(clamp((5.0 - r) / uPx + 0.5, 0.0, 1.0) + 0.7 * exp(-r * r / 260.0), 0.0, 1.0);
  float a = head + line * (1.0 - head);
  vec3 c = (chain(uHead.x / uHead.y) * head + base * line * (1.0 - head)) / max(a, 1e-4);
  outColor = vec4((toSrgb(c) + (hash(gl_FragCoord.xy) - 0.5) / 255.0) * a, a);
}`;
// A station: an octahedron of the poster diamond's half-diagonal, flat-shaded facets, one key light from the upper
// left, the pulse as a moving point light that glints on the facets it faces.
const FORM_VS = `#version 300 es
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
uniform vec4 uAt;  // centre x, y (y up), half-diagonal, turn about the vertical
uniform vec2 uView;
out vec3 vN, vP;
void main() { float c = cos(uAt.w), s = sin(uAt.w); mat3 turn = mat3(c, 0.0, -s, 0.0, 1.0, 0.0, s, 0.0, c);
  vP = turn * aPos * uAt.z + vec3(uAt.xy, 0.0); vN = turn * aNormal;
  gl_Position = vec4(2.0 * vP.x / uView.x - 1.0, 2.0 * vP.y / uView.y + 1.0, 0.0, 1.0); }`;
const FORM_FS = `#version 300 es
precision highp float;
in vec3 vN, vP;
uniform vec3 uForm, uLight;  // linear: the station's one hue, the pulse's colour now
uniform vec4 uPulse;         // the pulse light: position (y up), strength
uniform float uGlow;         // 0-1: this station just passed
out vec4 outColor;
${TO_SRGB}
const vec3 KEY = normalize(vec3(-0.5, 0.6, 0.62));
void main() {
  vec3 N = normalize(vN), toL = uPulse.xyz - vP;
  float r = length(toL), fall = uPulse.w / (1.0 + r * r / 1600.0);
  vec3 L = toL / max(r, 1e-3);
  vec3 c = uForm * (0.42 + 0.78 * max(dot(N, KEY), 0.0) + 0.5 * uGlow);
  c += uLight * fall * (0.3 * max(dot(N, L), 0.0) + 0.8 * pow(max(dot(N, normalize(L + vec3(0.0, 0.0, 1.0))), 0.0), 12.0));
  outColor = vec4(toSrgb(min(c, vec3(1.0))) + (hash(gl_FragCoord.xy) - 0.5) / 255.0, 1.0);
}`;

// Eight flat facets, wound counter-clockwise from outside: [position, normal] per corner.
function octahedron() {
  const out = [];
  for (const sx of [1, -1]) for (const sy of [1, -1]) for (const sz of [1, -1]) {
    const a = [sx, 0, 0], b = [0, sy, 0], c = [0, 0, sz], n = [sx, sy, sz].map(v => v / Math.sqrt(3));
    for (const p of sx * sy * sz > 0 ? [a, b, c] : [a, c, b]) out.push(...p, ...n);
  }
  return new Float32Array(out);
}
const linear = c => c.map(v => v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

function mountScene(box) {
  const canvas = box.querySelector("canvas"), setState = s => {
    box.dataset.state = s;
    s === "live" ? canvas.removeAttribute("aria-hidden") : canvas.setAttribute("aria-hidden", "true");
  };
  // Survival 1: no WebGL2 (or only a software renderer) -> the poster stays, nothing throws.
  const gl = canvas.getContext("webgl2", { alpha: true, premultipliedAlpha: true, antialias: true, depth: false,
    powerPreference: "low-power", failIfMajorPerformanceCaveat: true });
  if (!gl) return setState("no-webgl2");
  const mesh = octahedron(), off = new AbortController();
  const on = (target, type, fn) => target.addEventListener(type, fn, { signal: off.signal });
  let res = null, raf = 0, last = 0, stopped = false, visible = !document.hidden, onscreen = true;
  let tau = 0, running = false, geo = null, palette = null;

  // Survival 8: any failure ends at the poster, logged once, its GPU resources and context given back.
  const fail = err => { if (stopped) return; stopped = true; cancelAnimationFrame(raf); off.abort(); free();
    console.error("hero scene: showing the poster", err); setState("failed"); };
  function free() {
    if (res && !gl.isContextLost()) { gl.deleteProgram(res.track.p); gl.deleteProgram(res.form.p); gl.deleteVertexArray(res.vao); gl.deleteBuffer(res.vbo); }
    res = null; gl.getExtension("WEBGL_lose_context")?.loseContext();  // after off.abort(): no "lost" state follows
  }
  function program(vs, fs) {
    const p = gl.createProgram();
    for (const [type, src] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS) && !gl.isContextLost()) throw new Error(gl.getShaderInfoLog(s));
      gl.attachShader(p, s); gl.deleteShader(s);
    }
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS) && !gl.isContextLost()) throw new Error(gl.getProgramInfoLog(p));
    const u = {};
    for (let i = 0, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS) || 0; i < n; i++) {
      const name = gl.getActiveUniform(p, i).name; u[name] = gl.getUniformLocation(p, name);
    }
    return { p, u };
  }
  // Every GPU resource made here; a restored context runs it again (survival 3).
  function init() {
    const vao = gl.createVertexArray(), vbo = gl.createBuffer();
    gl.bindVertexArray(vao);
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo); gl.bufferData(gl.ARRAY_BUFFER, mesh, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 24, 0);
    gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 24, 12);
    gl.bindVertexArray(null);
    res = { track: program(TRACK_VS, TRACK_FS), form: program(FORM_VS, FORM_FS), vao, vbo };
  }
  // The palette is the page's tokens; a 1x1 2D canvas resolves any CSS colour to sRGB bytes.
  const probe = document.createElement("canvas").getContext("2d", { willReadFrequently: true });
  const cssColour = name => { probe.fillStyle = "#808080"; probe.fillStyle = getComputedStyle(box).getPropertyValue(name).trim() || "#808080";
    probe.clearRect(0, 0, 1, 1); probe.fillRect(0, 0, 1, 1); return linear([...probe.getImageData(0, 0, 1, 1).data.slice(0, 3)].map(v => v / 255)); };
  const readPalette = () => { palette = Object.fromEntries(["signal", "rule", "stop", "ok"].map(k => [k, cssColour(`--${k}`)])); };
  // The stations and track as the visible poster draws them, in its own units.
  function readPoster() {
    const svg = [...box.querySelectorAll("svg.poster")].find(s => s.getClientRects().length);
    if (!svg) return null;
    const rows = [...svg.querySelectorAll(".track")].map(l => ({ x1: l.x1.baseVal.value, x2: l.x2.baseVal.value, y: l.y1.baseVal.value }));
    let span = 0;
    for (const r of rows) { r.start = span; span += r.x2 - r.x1; }
    const stations = [...svg.querySelectorAll(".st")].map(el => {
      const s = el.width.baseVal.value, x = el.x.baseVal.value + s / 2, y = el.y.baseVal.value + s / 2;
      const row = rows.find(r => Math.abs(r.y - y) < 1), u = row && span ? (row.start + x - row.x1) / span : 0;
      return { x, y, half: s / Math.SQRT2, hit: PASS * Math.acos(1 - 2 * u) / Math.PI };  // when the head reaches it
    });
    return { w: svg.viewBox.baseVal.width, h: svg.viewBox.baseVal.height, rows, span, stations };
  }

  function draw() {
    if (!geo || !geo.span) return false;  // no poster on show to follow: stay the poster
    const t = running ? tau : -1, along = geo.span * (0.5 - 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, t / PASS))));
    const light = smooth(0, 0.35, t) * (1 - smooth(PASS, PASS + FADE, t)), u = along / geo.span;
    const pulse = u < 0.5 ? mix(palette.stop, palette.signal, u * 2) : mix(palette.signal, palette.ok, u * 2 - 1);
    const row = geo.rows.find(r => along <= r.start + r.x2 - r.x1) || geo.rows[geo.rows.length - 1];
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    const tr = res.track;
    gl.useProgram(tr.p);
    gl.uniform2f(tr.u.uView, geo.w, geo.h); gl.uniform3f(tr.u.uHead, along, geo.span, light);
    gl.uniform1f(tr.u.uPx, geo.w / canvas.width);
    gl.uniform3fv(tr.u.uRule, palette.rule); gl.uniform3fv(tr.u.uStop, palette.stop);
    gl.uniform3fv(tr.u.uMid, palette.signal); gl.uniform3fv(tr.u.uOk, palette.ok);
    for (const r of geo.rows) {
      gl.uniform4f(tr.u.uBox, r.x1 - 30, r.y - 30, r.x2 + 30, r.y + 30); gl.uniform4f(tr.u.uRow, r.x1, r.x2, r.y, r.start);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    gl.disable(gl.BLEND); gl.enable(gl.CULL_FACE);
    const f = res.form;
    gl.useProgram(f.p);
    gl.uniform2f(f.u.uView, geo.w, geo.h); gl.uniform3fv(f.u.uForm, palette.signal); gl.uniform3fv(f.u.uLight, pulse);
    gl.uniform4f(f.u.uPulse, row.x1 + along - row.start, -row.y, 18, light);
    gl.bindVertexArray(res.vao);
    for (const s of geo.stations) {
      const since = t - s.hit, turn = since > 0 ? 1 - (1 - Math.min(1, since)) ** 3 : 0;
      gl.uniform4f(f.u.uAt, s.x, -s.y, s.half, turn * Math.PI / 2);  // a quarter turn ends where it began
      gl.uniform1f(f.u.uGlow, since > 0 ? Math.exp(-since / 0.5) : 0);
      gl.drawArrays(gl.TRIANGLES, 0, 24);
    }
    gl.bindVertexArray(null); gl.disable(gl.CULL_FACE);
    return true;
  }
  // Draw now; the first good frame fades the canvas in over the poster (survival 2).
  function render() {
    if (stopped || !res || gl.isContextLost() || reduce.matches) return;
    try { if (!draw()) return; } catch (err) { return fail(err); }
    if (box.dataset.state !== "live") setState("live");
  }
  function frame(now) {
    raf = 0;
    tau += Math.min((now - (last || now)) / 1000, 0.1); last = now;
    if (tau > PASS + FADE) running = false;  // the pass is over: the still frame, and no more frames
    render();
    if (running) wake();
  }
  // Survival 9: no frames offscreen, in a hidden tab, under reduced motion, or once the pass is over.
  function wake() { if (!raf && running && !stopped && visible && onscreen && res && !gl.isContextLost() && !reduce.matches) raf = requestAnimationFrame(frame); }
  function sleep() { cancelAnimationFrame(raf); raf = 0; last = 0; }
  const pass = () => { if (!running) { running = true; tau = -LEAD; } wake(); };  // the pulse waits out the fade-in

  // Budget: DPR capped at 2 (1.5 on touch screens); resize redraws in the same callback, so no blank frame.
  const ro = new ResizeObserver(() => {
    const dpr = Math.min(window.devicePixelRatio || 1, matchMedia("(pointer: coarse)").matches ? 1.5 : 2);
    canvas.width = Math.max(1, Math.round(canvas.clientWidth * dpr)); canvas.height = Math.max(1, Math.round(canvas.clientHeight * dpr));
    try { geo = readPoster(); } catch (err) { return fail(err); }
    render();
  });
  const io = new IntersectionObserver(entries => { onscreen = entries.at(-1).isIntersecting; onscreen ? pass() : sleep(); });  // oldest first
  on(document, "visibilitychange", () => { visible = !document.hidden; visible ? wake() : sleep(); });
  // Survival 5: reduced motion turned on mid-visit puts the poster back; turned off, the scene returns.
  on(reduce, "change", () => { if (reduce.matches) { sleep(); running = false; setState("still"); } else { render(); pass(); } });
  // Light or dark, by the system or the page's switch: the tokens change, the frame follows.
  const recolour = () => { readPalette(); render(); };
  on(matchMedia("(prefers-color-scheme: dark)"), "change", recolour);
  const mo = new MutationObserver(recolour);
  mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  // Survival 3: preventDefault or the browser never restores; the poster covers the gap.
  on(canvas, "webglcontextlost", e => { e.preventDefault(); sleep(); res = null; setState("lost"); });
  on(canvas, "webglcontextrestored", () => { try { init(); } catch (err) { return fail(err); }
    if (reduce.matches) setState("still"); render(); wake(); });
  off.signal.addEventListener("abort", () => { ro.disconnect(); io.disconnect(); mo.disconnect(); });

  try { readPalette(); init(); } catch (err) { return fail(err); }
  ro.observe(canvas); io.observe(box);
}

// One scene, one context: the poster is the page's only canvas. Reduced motion never makes a context at all.
if (box) {
  if (!reduce.matches) mountScene(box);
  else {
    box.dataset.state = "still";
    reduce.addEventListener("change", () => mountScene(box), { once: true });
  }
}
