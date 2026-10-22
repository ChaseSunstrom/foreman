<!-- Foreman's own playbook (written for Foreman, not ported). -->
# 3D on the web: a designed scene that never breaks the page

Use when a page gets a WebGL scene: a hero object, a product viewer, a data sculpture, an ambient background. Applies to three.js, React Three Fiber and raw WebGL alike. The API lives in the cards (`fm lib show three-js`, `fm lib show react-three-fiber`, `fm lib show postprocessing`, `fm lib show webgl`, `fm lib show glsl`, `fm lib show shader-performance`); this playbook holds the decisions, the numbers and the failure handling.

The one rule: **the page works without the scene, and the scene earns its cost.** Every rule below is written so a reviewer can say pass or fail. The scene's colours (clear colour, fog, lights' tint) come from the project's `DESIGN.md` tokens (`design-direction.md`), and its reduced-motion path is `motion.md`'s.

## Before the first mesh: the scene's job

Write one sentence: what does the 3D show that a still picture or a 3-second video can't (turn the product, explore a structure, react to the reader)? If the answer is "it looks cool", ship a rendered image or a looping video and stop here: they cost nothing at runtime and never black-screen.

- Pass: the brief or the PR names the job, and the scene responds to something (input, scroll, data, time) a picture can't.
- Fail: the scene autoplays one fixed motion forever. That is a video; encode it as one.

## Composition

One subject, one camera, one idea. Compose like a photographer, then lock it so no viewport and no drag can ruin it.

1. **One subject wins the squint test.** Downscale a screenshot to 64 px wide (or blur it 8 px): the subject is still the highest-contrast, most saturated region. Backgrounds, particles and floors lose that test on purpose.
2. **Choose the lens on purpose.** Vertical field of view 20–35° for an object you look at (product, logo, sculpture: long lens, little distortion); 45–65° for a space you are inside (room, landscape). Above 75° only as a deliberate effect. The defaults (50° for a bare three.js `PerspectiveCamera`, 75° for React Three Fiber's default camera) are placeholders, not choices.
3. **Fit the subject from its bounds, not by eye.** Distance = r / sin(fov/2) for a bounding sphere of radius r, using the smaller of the vertical FOV and the horizontal FOV (2·atan(tan(vfov/2)·aspect)). Recompute on every resize. Pass: the whole subject is in frame at 360×640 portrait and at 1920×1080.
4. **Fill 40–70% of the frame's short side.** Smaller reads as lost, bigger crowds the copy. When text sits beside the scene, offset the subject to the third away from the text (shift the camera's view offset or the subject, never squash the canvas) so empty space faces the words.
5. **Look slightly down.** A 5–15° downward camera tilt grounds an object; dead-level reads as a technical drawing, and below the subject reads as heroic, which a product rarely wants. Keep the horizon off the exact middle.
6. **Ground it.** A floating object needs a contact shadow, a soft blob under it or a reflection. Pass: nothing that should rest on something hovers with no darkening beneath it.
7. **No seam with the page.** The canvas edges match the page background: a transparent canvas (alpha) or a clear color and fog equal to the page color. Pass: a canvas corner pixel equals the page background (or alpha is 0).
8. **Clip planes as tight as the scene allows.** far/near ≤ 10,000; raise near before you lower far. A near of 0.001 is the usual cause of flickering, interleaved surfaces.
9. **Clamp every control.** Orbit limits on polar angle and distance, damping on, pan off unless the job needs it. Pass: drag and zoom to every limit; the subject is still framed and the camera never goes inside or under it.
10. **The scroll belongs to the page.** On a scrolling page, wheel-zoom is off (or only after the user clicks into the scene), and a full-width canvas never swallows vertical swipes on touch: allow `touch-action: pan-y` and rotate horizontally only, or activate on tap. Pass: wheel and swipe over the canvas scroll the page.

## Light and material

Get the color pipeline right before touching a single light, or every later tweak compensates for a bug.

**The pipeline, once:** color textures (albedo, emissive) are sRGB; data textures (normal, roughness, metalness, AO) are linear; output is sRGB; one tone mapper (ACES, AgX or Neutral) chosen and kept, exposure tuned against it. Washed-out grey means a double conversion; muddy and over-saturated means a missing one. Colors that must match CSS go through the same conversion (three.js `Color` converts for you; raw WebGL needs you to linearize the hex).

**Recipes** (pick one, then adjust; don't mix two):

| Look | Environment | Direct lights | Materials | Post |
|---|---|---|---|---|
| Studio product | soft studio HDR at 0.6–1.0 intensity, background hidden | one key at ~45° above and to the side, casting the only shadow; optional rim from behind | PBR from the real object; metals need the environment to look like metal | none, or subtle SMAA |
| Soft clay / abstract | low-contrast HDR or a hemisphere light (sky warm, ground cool) | one soft directional, large shadow radius | roughness 0.6–0.9, metalness 0, one or two pastel hues | ambient occlusion if the shapes nest |
| Night / neon | near-black environment | few or none: emissive surfaces do the lighting | emissive values above 1.0 on what should glow, dark rough everything else | bloom with a threshold of ~1.0, so only the glowing parts bloom |
| Diagram / data | none | none or one flat light | unlit, matcap or toon ramp; color encodes meaning | none; outlines if parts touch |

**Checkable rules:**

- At most one shadow-casting light, at most three direct lights in total; the environment does the rest. Static lighting is baked into textures or vertex colors.
- The shadow camera hugs the subject: its box is within ~1.5× the subject's bounds (turn on the camera helper to check). Shadow map 1024–2048; a bigger map hides a frustum that is too big.
- Metalness is 0 or 1 except in masked transitions; roughness is never exactly 0; albedo stays inside sRGB 30–240 (nothing real is pure black or pure white).
- The subject's silhouette separates from the background by luminance, not only by hue: a rim light, a darker backdrop or a lighter one. Pass: the greyscale squint test still finds the outline.

## Shader looks

Signature looks that are cheap when built right. Each one has an intensity uniform where 0 means plain, so it can be measured, tuned and turned off by the quality ladder.

- **Fresnel rim:** `rim = pow(1.0 - max(dot(N, V), 0.0), 3.0)` added to emissive; the cheapest way to separate a silhouette. Exponent 2–5; a lower exponent turns it into a halo.
- **Toon ramp:** quantize `dot(N, L)` through a tiny ramp texture (4–8 texels, nearest filtering) rather than branches; the ramp is the art direction and can change without a shader edit.
- **Gradient map:** compute luminance, then look up a 256×1 gradient texture. One texture gives a whole scene a brand palette.
- **Dissolve / reveal:** a noise texture against a threshold uniform, with a thin emissive edge band. Keep `discard` materials small and off large opaque surfaces: a shader that can discard loses early depth rejection for everything it covers.
- **Dither every gradient:** add ±0.5/255 of screen-space noise before output. Dark smooth gradients band in 8 bits on every display; this removes it for one hash.
- **Fog that is the page:** fog color equals the page background (after the color conversion above), so distance fades into the page instead of into grey.

Two traps that only show up later:

- **Time loses precision.** A `uTime` uniform that grows forever stutters: in `mediump` (half floats, common on phones) the step between representable values passes 1/60 s after about 32 seconds, and in `highp` it still grows with every hour. Wrap time on the CPU (JavaScript numbers are doubles) with a period that is a multiple of every loop in the shader, and declare the uniform `highp` where the device supports it. Pass: the scene left open for an hour animates as smoothly as at second one (fake it by starting the clock at 3,600).
- **NaN spreads.** `normalize(vec3(0))`, `pow` of a negative base, or a divide by zero makes a NaN pixel; bloom and blur smear it into a black or white blot. Guard the denominators; probe with `if (any(isnan(c))) c = vec3(1, 0, 1);` (WebGL2 / GLSL ES 3.00 only, and some drivers fold `isnan` away under fast math: if the probe never fires, test the suspect denominators directly).

Post-processing: at most three passes, merged where the library allows (the `postprocessing` library combines several effects in one pass). Bloom, vignette and grain together is the budget's ceiling, not its floor.

## Budget

Target device: **a mid laptop** (integrated graphics, 1920×1080 panel, devicePixelRatio 1.5, on battery, browser fullscreen) and **a mid phone** for anything above the fold on mobile. Measure there, not on the workstation that built it.

| Measure | Laptop | Phone | How to read it |
|---|---|---|---|
| Frame time, p95 over 10 s of interaction | ≤ 16.7 ms (60 fps) | ≤ 33 ms (30 fps floor, 60 preferred) | `requestAnimationFrame` deltas, or the browser's performance panel |
| GPU time per frame | ≤ 10 ms (the page needs the rest) | ≤ 16 ms | timer query extension where the browser exposes it; otherwise frame time with the CPU idle |
| Draw calls | ≤ 100 | ≤ 50 | three.js `renderer.info.render.calls`; Spector.js for raw WebGL |
| Triangles drawn | ≤ 500 k | ≤ 150 k | `renderer.info.render.triangles` |
| Texture memory | ≤ 64 MB | ≤ 32 MB | sum of width × height × bytes per texel × 1.33 for mips |
| Device pixel ratio | min(dpr, 2) | min(dpr, 1.5) | read `renderer.getPixelRatio()` |
| Scene download | ≤ 2 MB compressed before the first frame | ≤ 1 MB | network panel, filtered to the scene's chunk and assets |
| Hitch after reveal | none > 50 ms | none > 100 ms | performance panel; shaders compiled before reveal |
| Idle cost | 0 frames when nothing moves, offscreen or hidden | same | performance panel for 5 s idle: no GPU tasks |

Arithmetic worth remembering:

- Fragment work scales with DPR squared: DPR 2 shades 4× the pixels of DPR 1. The DPR cap is the biggest single lever.
- One uncompressed 4096² RGBA texture with mips is ≈ 85 MB: over the whole laptop budget on its own. Use 2048² at most for a hero texture, and GPU-compressed formats (KTX2/Basis, 4–8× smaller in memory) for everything.
- Instancing turns a thousand copies into one draw call; merging static meshes that share a material does the same for scenery.

Loading: the 3D code and assets load after the page's main content has painted (dynamic import, triggered when the scene's container nears the viewport). Geometry compressed (Draco or meshopt), textures KTX2. Shaders are compiled before the canvas fades in (three.js `renderer.compile` or `compileAsync`).

**Quality ladder.** When p95 frame time stays over budget for ~2 s, step down in this order and never up again in the same session (oscillating is worse than either level; with drei's `PerformanceMonitor` use `onDecline` only and ignore `onIncline`, and treat `AdaptiveDpr` as a drop during interaction, not a step on this ladder): DPR → post-processing → shadow map size → shadows off → particle and instance counts → the poster. Never drop the subject's own geometry first; it is the reason the scene exists. React Three Fiber users get most of this from drei's performance monitor and adaptive DPR helpers.

## Survival contract

The scene is an enhancement. Each clause below has a probe; a scene that fails one doesn't ship. A raw WebGL2 starting point that already passes all nine, in one file with no dependencies: `references/ui/templates/scene.html`. For three.js, describe the scene once as plain data (camera, lights, materials, meshes, animations) and `fm scene compile scene.json --out scene.js` emits a module with the same clauses built in; the page keeps the poster and the text twin (`fm scene --help` holds the schema). `--to component` adds `<fm-scene label="...">`, a custom element holding the poster as its `slot="poster"` child and the twin after it; give it its box before it is defined, `fm-scene:not(:defined){display:block;position:relative;aspect-ratio:16/10}` and `fm-scene:not(:defined)>[slot=poster]{width:100%;height:100%;object-fit:cover}`, then set the ratio with `fm-scene::part(stage)`. A second scene on one page takes its own tag, `customElements.define("fm-scene-2", FmScene)`, and its markup uses `<fm-scene-2>` too.

1. **No WebGL, no problem.** When `getContext("webgl2")` (and the WebGL1 fallback, if you have one) returns null, the poster and the text twin show and nothing throws. Check before constructing the renderer: three.js's `WebGLRenderer` and an R3F `Canvas` throw when there is no context, so test `getContext` first, or wrap the construction in try/catch (an error boundary for R3F). Decorative scenes also pass `failIfMajorPerformanceCaveat: true`, so a software renderer gets the poster instead of a 5 fps slideshow. Probe: an init script that replaces `HTMLCanvasElement.prototype.getContext` with one returning null; the page has no console errors and shows the poster.
2. **The poster is there first.** A still image rendered from the same scene, same framing, same aspect ratio, sits where the canvas will be from the first paint; the canvas fades in over it only after its first frame has drawn. Pass: layout shift from the scene is 0, and with JavaScript disabled the poster shows.
3. **Context loss is survived.** On `webglcontextlost`: call `preventDefault()` (without it the browser never restores the context), stop the loop, show the poster. On `webglcontextrestored`: rebuild every GPU resource you created yourself, resume the loop, hide the poster. three.js resets its own state on restore; buffers, textures and programs you made through raw `gl` calls are yours to rebuild. Probe: `gl.getExtension("WEBGL_lose_context").loseContext()`, then `restoreContext()` a second later: the poster covers the gap, the scene returns, no console errors.
4. **One context per page.** Browsers cap live WebGL contexts (Chrome keeps about 16 on desktop, fewer on phones; the exact numbers vary by browser and version) and lose the oldest, with a console warning and a `webglcontextlost` event on it. Several views share one renderer through viewports and scissor rectangles; a route change disposes its renderer and releases its context (raw three.js: `renderer.dispose()` then `renderer.forceContextLoss()`; R3F does both on unmount). Pass: navigating through every route twice never logs a lost context.
5. **Reduced motion is honored.** Under `prefers-reduced-motion: reduce`: no auto-rotate, no camera drift, no scroll-driven flight, no parallax; render one still frame and then only on user input. Probe: emulate the media feature, take two screenshots a second apart: they are identical.
6. **It has a name and a text twin.** A non-interactive canvas has `role="img"` and an `aria-label` naming what it depicts. Whatever the scene communicates (product colors, the data in a sculpture, a step in a process) also exists as DOM text: a caption, a list, a table. Pass: remove the canvas from the page and no information is lost.
7. **Interaction is keyboard-reachable.** An interactive scene is focusable, shows a visible focus ring, rotates or steps with arrow keys, says so in its label, and never traps focus. Pass: tab in, operate it, tab out, without a pointer.
8. **Failure is contained.** A shader that fails to compile, an asset that 404s or a loader that throws ends at the poster, logged once, never at a blank or black box. Pass: block the model's URL in the network panel and reload.
9. **It sleeps.** Offscreen (an intersection observer) or in a hidden tab, the loop stops; a scene with nothing moving renders on demand (React Three Fiber: `frameloop="demand"` with `invalidate()`). On unmount, the loop is cancelled, listeners removed, and geometries, materials, textures and the renderer disposed, and the context released (`renderer.forceContextLoss()` in raw three.js). Pass: `renderer.info.memory` returns to its starting counts after ten mount/unmount cycles.

## Black screen triage

Run the first probe first: it halves the search.

**Probe zero: set the clear color to magenta.** Magenta canvas → the context, size and loop work; the problem is the scene (camera, lights, materials, shaders). No magenta → the problem is the canvas or the loop.

| Symptom | Likely cause | Probe |
|---|---|---|
| No magenta, canvas has no visible area | the container has 0 height (canvas sized by CSS from a parent that has none) | `canvas.clientHeight` and `canvas.width`; give the container a height or aspect ratio |
| No magenta, canvas sized | the loop never runs, the context failed, or something is painted over it | log in the frame callback; check the context is non-null; inspect stacking order |
| Magenta, subject missing | camera inside or behind the subject, the subject outside near/far, or wrong units (a model in centimeters is 100× too big) | log the scene's bounding box size and center; add axes and box helpers; refit the camera with the formula from Composition |
| Subject is a black silhouette | no lights, metals without an environment map, or missing or inverted normals | swap in a normal-visualizing material: colored means lighting or material, still black means geometry or normals |
| Black only on some devices | an unchecked shader compile error, `highp` unsupported in fragment shaders, float render targets unsupported | read the shader info log (three.js reports it to the console when shader error checking is on); run the page under a software renderer |
| Black after a while, a tab switch or route changes | context lost from leaked GPU memory or too many contexts | log `webglcontextlost`; watch `renderer.info.memory` across navigations |
| Black only with post-processing on | the composer isn't resized with the canvas, an unsupported render-target type, or tone mapping applied twice | disable passes one at a time; compare composer size with canvas size |
| Black or white blots that grow with bloom | NaN pixels from the shader | the magenta NaN probe from Shader looks |
| Black for one frame on resize | setting `canvas.width` clears the buffer and the redraw waits a frame | render right after resizing, in the same callback |
| Black only in screenshot tests | headless browser without a GPU, or the capture runs before the first frame or after the buffer was cleared | run headless with a software GL backend; wait for a "first frame drawn" flag; capture with `preserveDrawingBuffer` in tests only |
| Washed out or too dark, not black | color space mismatch | check output color space and each texture's color space against the pipeline in Light and material |

## Done when

- [ ] The scene's job is one sentence, and a still image couldn't do it.
- [ ] Squint test, fit at 360×640 and 1920×1080, clamped controls and page scroll all pass.
- [ ] The budget table's numbers were measured on the target devices and recorded in the task's evidence.
- [ ] All nine survival clauses have their probe run, ideally as browser tests (null context, lose and restore, reduced motion, blocked asset, mount/unmount memory).
- [ ] The poster is rendered from the current scene, not a stale one.
