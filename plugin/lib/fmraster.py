"""fmraster (T-1631): an integer software rasteriser, the deterministic frame source for tests and terminal previews.

Triangles in camera space (x right, y up, z ahead, the camera at the origin; integers only) go through a perspective
divide to 1/16-pixel fixed point, fill by edge functions, depth-test on an interpolated 1/z and take one flat shade
from a directional light. No float is ever made, so a frame's bytes are the same on every run, machine and Python
(its PNG's too wherever zlib is the same build: zlib-ng deflates the same pixels to other bytes).
Front faces are clockwise as the camera sees them (Direct3D's rule); back faces are culled.
ponytail: a triangle with a vertex nearer than z=1 is dropped, not clipped, and pixels on a shared edge go to the
first triangle drawn (no top-left rule); no textures, smooth shading or anti-aliasing. Each triangle costs its
on-screen box in pure Python (about a second a megapixel), so keep frames small.
"""
from math import isqrt

import fmimg

SUB = 16  # sub-pixel steps per pixel
ONE = 1 << 32  # 1/z's fixed-point scale in the z-buffer
NEAR = 1
AMBIENT = 64  # of 256: a face turned from the light keeps a quarter of its colour
LIGHT = (1, 2, -3)  # toward the light: from above, right and behind the camera
MAX_PIXELS = 1 << 22


def _rgb(c):
    b = bytes(c)  # ValueError past 0..255, TypeError for a float
    if len(b) != 3:
        raise ValueError(f"{c!r} isn't an (r, g, b) colour")
    return b


def _sub(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def _cross(u, v):
    return u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _turn(p, c, s, d):
    """p turned about y, then about x, by the angle whose cosine is c/d and sine s/d (3-4-5 is exact in integers)."""
    x, y, z = p
    x, z = (x * c + z * s) // d, (z * c - x * s) // d
    y, z = (y * c + z * s) // d, (z * c - y * s) // d
    return x, y, z


def cube(half=100, at=(0, 0, 450), colour=(200, 120, 60), turn=(4, 3, 5)):
    """A cube's 12 triangles, turned so its front, right and top faces show, centred at `at`."""
    tris = []
    for axis in range(3):
        u, v = (a for a in range(3) if a != axis)
        for side in (-half, half):
            quad = []
            for du, dv in ((-1, -1), (-1, 1), (1, 1), (1, -1)):
                p = [0, 0, 0]
                p[axis], p[u], p[v] = side, du * half, dv * half
                quad.append(tuple(p))
            for a, b, c in ((quad[0], quad[1], quad[2]), (quad[0], quad[2], quad[3])):
                if _dot(_cross(_sub(b, a), _sub(c, a)), a) < 0:  # the normal must point out of the cube
                    b, c = c, b
                tris.append((*(tuple(q + o for q, o in zip(_turn(p, *turn), at)) for p in (a, b, c)), colour))
    return tris


def render(tris, width=64, height=64, focal=None, light=LIGHT, ambient=AMBIENT, background=(0, 0, 0)):
    """Triangles [(p0, p1, p2, (r, g, b)), …] → width * height * 3 RGB bytes, rows top to bottom. focal is the
    camera's focal length in pixels (default the width: a 53° horizontal field of view)."""
    if width <= 0 or height <= 0 or width * height > MAX_PIXELS:
        raise ValueError(f"{width}x{height} isn't a frame of 1 to {MAX_PIXELS} pixels")
    f = (focal or width) * SUB
    cx, cy = width * SUB // 2, height * SUB // 2
    out = bytearray(_rgb(background) * (width * height))
    depth = [0] * (width * height)  # 1/z scaled by ONE: bigger is nearer, 0 is nothing drawn yet
    ll = _dot(light, light)
    for *pts, colour in tris:
        rgb = _rgb(colour)
        if len(pts) != 3 or not all(len(p) == 3 and all(isinstance(q, int) for q in p) for p in pts):
            raise TypeError(f"{pts!r} isn't three (x, y, z) integer points")
        if min(p[2] for p in pts) < NEAR:
            continue
        X = [cx + f * x // z for x, _, z in pts]
        Y = [cy - f * y // z for _, y, z in pts]
        area = (X[1] - X[0]) * (Y[2] - Y[0]) - (Y[1] - Y[0]) * (X[2] - X[0])
        if area <= 0:  # a back face, or edge-on
            continue
        n = _cross(_sub(pts[1], pts[0]), _sub(pts[2], pts[0]))
        lam = min(256, max(0, _dot(n, light)) * 256 // (isqrt(_dot(n, n) * ll) or 1))
        shade = ambient + (256 - ambient) * lam // 256
        rgb = bytes(c * shade >> 8 for c in rgb)
        iz = [ONE // p[2] for p in pts]
        x0, x1 = max(0, min(X) // SUB), min(width - 1, max(X) // SUB)
        y0, y1 = max(0, min(Y) // SUB), min(height - 1, max(Y) // SUB)
        # w0, w1, w2: the edge functions of edges 1→2, 2→0 and 0→1; all ≥ 0 inside, their sum is area
        dx = [(Y[2] - Y[1]) * SUB, (Y[0] - Y[2]) * SUB, (Y[1] - Y[0]) * SUB]
        for y in range(y0, y1 + 1):
            px, py = x0 * SUB + SUB // 2, y * SUB + SUB // 2
            w0 = (X[2] - X[1]) * (py - Y[1]) - (Y[2] - Y[1]) * (px - X[1])
            w1 = (X[0] - X[2]) * (py - Y[2]) - (Y[0] - Y[2]) * (px - X[2])
            w2 = (X[1] - X[0]) * (py - Y[0]) - (Y[1] - Y[0]) * (px - X[0])
            i = y * width + x0
            for _ in range(x0, x1 + 1):
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    d = (w0 * iz[0] + w1 * iz[1] + w2 * iz[2]) // area
                    if d > depth[i]:
                        depth[i] = d
                        out[3 * i:3 * i + 3] = rgb
                w0 -= dx[0]
                w1 -= dx[1]
                w2 -= dx[2]
                i += 1
    return bytes(out)


def save(path, tris, width=64, height=64, **kw):
    """render() written to a PNG through fmimg (atomic, 0600)."""
    fmimg.save(path, width, height, render(tris, width, height, **kw), "rgb")
