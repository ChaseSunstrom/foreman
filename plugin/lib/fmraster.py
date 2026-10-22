"""fmraster (T-1631): an integer software rasteriser, the deterministic frame source for tests and terminal previews.

The camera sits at the origin looking along +z, x right and y up; callers move and turn their scene into that space
first (cube()'s turn and at do it for the cube), in integers. From a right-handed view space (three.js: looking
down -z, front faces counter-clockwise) negate z, the light's too, and swap two vertices of every triangle: the
mirror leaves the screen winding as it was, so three's front faces would otherwise be culled. Triangles are cut at the near plane z = NEAR, go
through a perspective divide to 1/16-pixel fixed point, fill by edge functions, depth-test on an interpolated 1/z
and take one flat shade from a directional light. No float is ever made, so a frame's bytes are the same on every
run, machine and Python (its PNG's too wherever zlib is the same build: zlib-ng deflates the same pixels to other
bytes). Front faces are clockwise as the camera sees them (Direct3D's rule); back faces are culled.
ponytail: pixels on a shared edge go to the first triangle drawn (equal depths tie to it; rounding can decide
near-ties: no top-left rule); no textures, smooth shading or anti-aliasing. Each triangle costs its on-screen box
in pure Python (about a second a megapixel), so a render past WORK pixel tests is refused before it draws.
"""
from math import isqrt

import fmimg

SUB = 16  # sub-pixel steps per pixel
ONE = 1 << 32  # 1/z's fixed-point scale in the z-buffer
NEAR = 1
AMBIENT = 64  # of 256: a face turned from the light keeps a quarter of its colour
LIGHT = (1, 2, -3)  # toward the light: from above, right and behind the camera
MAX_PIXELS = 1 << 22
WORK = MAX_PIXELS * 16  # pixel tests a render may make: 16 full frames at the cap, a minute or so


def _rgb(c):
    b = bytes(tuple(c))  # ValueError past 0..255, TypeError for a float or a bare int (bytes(3) is three zeros)
    if len(b) != 3:
        raise ValueError(f"{c!r} isn't an (r, g, b) colour")
    return b


def _point(p):
    if len(p) != 3 or not all(isinstance(q, int) for q in p):
        raise TypeError(f"{p!r} isn't an (x, y, z) of integers")
    return p


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


def _clip(pts):
    """The triangle cut to z >= NEAR (Sutherland-Hodgman on one plane): 0, 1 or 2 triangles, winding kept. Each cut
    is measured from the edge's near end, so two triangles sharing an edge cut it at the same point."""
    poly = []
    for a, b in zip(pts, pts[1:] + pts[:1]):
        if a[2] >= NEAR:
            poly.append(a)
        if (a[2] >= NEAR) != (b[2] >= NEAR):
            p, q = (a, b) if a[2] >= NEAR else (b, a)
            t, d = p[2] - NEAR, p[2] - q[2]
            poly.append((p[0] + (q[0] - p[0]) * t // d, p[1] + (q[1] - p[1]) * t // d, NEAR))
    return [(poly[0], poly[i], poly[i + 1]) for i in range(1, len(poly) - 1)]


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
    focal = width if focal is None else focal
    if not all(isinstance(v, int) for v in (width, height)) or width <= 0 or height <= 0 \
            or width * height > MAX_PIXELS:
        raise ValueError(f"{width}x{height} isn't a frame of 1 to {MAX_PIXELS} pixels")
    if not isinstance(focal, int) or focal <= 0:
        raise ValueError(f"focal {focal!r} isn't a positive whole number of pixels")
    if not isinstance(ambient, int) or not 0 <= ambient <= 256:
        raise ValueError(f"ambient {ambient!r} isn't a whole number from 0 to 256")
    bg, ll = _rgb(background), _dot(_point(light), light)
    f, cx, cy = focal * SUB, width * SUB // 2, height * SUB // 2
    work, todo = 0, []
    for *pts, colour in tris:
        rgb = _rgb(colour)
        if len(pts) != 3:
            raise TypeError(f"{pts!r} isn't three points")
        n = _cross(_sub(_point(pts[1]), _point(pts[0])), _sub(_point(pts[2]), pts[0]))
        lam = min(256, max(0, _dot(n, light)) * 256 // (isqrt(_dot(n, n) * ll) or 1))
        shade = ambient + (256 - ambient) * lam // 256
        rgb = bytes(c * shade >> 8 for c in rgb)
        for tri in _clip(pts):
            X = [cx + f * x // z for x, _, z in tri]
            Y = [cy - f * y // z for _, y, z in tri]
            area = (X[1] - X[0]) * (Y[2] - Y[0]) - (Y[1] - Y[0]) * (X[2] - X[0])
            if area <= 0:  # a back face, or edge-on: every edge function 0 would divide the depth by zero
                continue
            x0, x1 = max(0, min(X) // SUB), min(width - 1, max(X) // SUB)
            y0, y1 = max(0, min(Y) // SUB), min(height - 1, max(Y) // SUB)
            if x0 > x1 or y0 > y1:
                continue
            work += (x1 - x0 + 1) * (y1 - y0 + 1)
            if work > WORK:
                raise ValueError(f"over the budget of {WORK} pixel tests (16 frames of {MAX_PIXELS}): "
                                 "fewer or smaller triangles, or a smaller frame")
            todo.append((X, Y, area, [ONE // p[2] for p in tri], x0, x1, y0, y1, rgb))
    out = bytearray(bg * (width * height))
    depth = [0] * (width * height)  # 1/z scaled by ONE: bigger is nearer, 0 is nothing drawn yet
    for X, Y, area, iz, x0, x1, y0, y1, rgb in todo:
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
