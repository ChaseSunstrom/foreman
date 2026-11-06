# WebGL live-context cap, measured

Probe 2026-10-23: a page creating 40 canvases with getContext('webgl'), then counting those with !isContextLost() after 500 ms.

- HeadlessChrome/153.0.0.0 (Playwright chromium-1243, Linux x86_64, --headless=new, SwiftShader through ANGLE): made=40, live=16.
- Safari, Firefox and Android Chrome weren't available on this machine: their caps are unverified.

The probe page: a loop of document.createElement('canvas').getContext('webgl'), then made.filter(gl => !gl.isContextLost()).length.
