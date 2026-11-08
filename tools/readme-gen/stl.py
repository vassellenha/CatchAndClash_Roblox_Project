"""Builds an ASCII STL of the procedural FishingRod from RodTool.lua (same sizes, tilts and offsets)."""
import math
from common import OUT

SCALE = 10


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def T(x, y, z):
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def RX(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def RZ(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def apply(m, p):
    x, y, z = p
    return tuple(m[i][0] * x + m[i][1] * y + m[i][2] * z + m[i][3] for i in range(3))


tris = []


def add(m, a, b, c):
    tris.append((apply(m, a), apply(m, b), apply(m, c)))


def block(m, sx, sy, sz):
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz), (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (2, 3, 7), (2, 7, 6), (1, 2, 6), (1, 6, 5), (0, 4, 7), (0, 7, 3)]
    for a, b, c in faces:
        add(m, v[a], v[b], v[c])


def cylinder_x(m, length, radius, n=16):
    """Roblox cylinders run along the part's X axis."""
    h = length / 2
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p0 = (0, radius * math.cos(a0), radius * math.sin(a0))
        p1 = (0, radius * math.cos(a1), radius * math.sin(a1))
        A, B = (-h, p0[1], p0[2]), (-h, p1[1], p1[2])
        C, D = (h, p0[1], p0[2]), (h, p1[1], p1[2])
        add(m, A, D, B); add(m, A, C, D)
        add(m, (-h, 0, 0), B, A); add(m, (h, 0, 0), C, D)


def sphere(m, r, nu=10, nv=7):
    for i in range(nv):
        t0, t1 = math.pi * i / nv, math.pi * (i + 1) / nv
        for j in range(nu):
            p0, p1 = 2 * math.pi * j / nu, 2 * math.pi * (j + 1) / nu
            def P(t, p):
                return (r * math.sin(t) * math.cos(p), r * math.cos(t), r * math.sin(t) * math.sin(p))
            a, b, c, d = P(t0, p0), P(t0, p1), P(t1, p0), P(t1, p1)
            if i > 0:
                add(m, a, b, c)
            if i < nv - 1:
                add(m, b, d, c)


S = [[SCALE, 0, 0, 0], [0, SCALE, 0, 0], [0, 0, SCALE, 0], [0, 0, 0, 1]]
handle = mat_mul(S, T(0, 0, 0))
block(handle, 0.22, 1.0, 0.22)
cylinder_x(mat_mul(handle, T(0, -0.25, 0.28)), 0.4, 0.2)
# reel crank
block(mat_mul(handle, T(0.24, -0.25, 0.28)), 0.04, 0.3, 0.05)
segs = [((0.17, 1.3, 0.17), 3), ((0.13, 1.3, 0.13), 5), ((0.09, 1.2, 0.09), 6), ((0.05, 1.0, 0.05), 7)]
top = mat_mul(handle, T(0, 0.5, 0))
for size, tilt in segs:
    top = mat_mul(top, RX(tilt))
    seg = mat_mul(top, T(0, size[1] / 2, 0))
    block(seg, *size)
    top = mat_mul(seg, T(0, size[1] / 2, 0))
    # line guide ring at each joint
    cylinder_x(mat_mul(top, RZ(90)), 0.02, 0.05, 8)
tip = top
hook = mat_mul(tip, T(0.35, -1.3, 0.25))
sphere(hook, 0.07)
# fishing line as a thin box from tip to hook
tp = apply(tip, (0, 0, 0)); hp = apply(hook, (0, 0, 0))
dx, dy, dz = (hp[i] - tp[i] for i in range(3))
L = math.sqrt(dx * dx + dy * dy + dz * dz) / SCALE
# build basis with Y along the line
ux, uy, uz = dx / (L * SCALE), dy / (L * SCALE), dz / (L * SCALE)
ax = (1, 0, 0) if abs(ux) < 0.9 else (0, 0, 1)
xv = (uy * ax[2] - uz * ax[1], uz * ax[0] - ux * ax[2], ux * ax[1] - uy * ax[0])
n = math.sqrt(sum(c * c for c in xv)); xv = tuple(c / n for c in xv)
zv = (xv[1] * uz - xv[2] * uy, xv[2] * ux - xv[0] * uz, xv[0] * uy - xv[1] * ux)
mid = tuple((tp[i] + hp[i]) / 2 / SCALE for i in range(3))
M = [[xv[0], ux, zv[0], mid[0]], [xv[1], uy, zv[1], mid[1]], [xv[2], uz, zv[2], mid[2]], [0, 0, 0, 1]]
block(mat_mul(S, M), 0.025, L, 0.025)


def normal(a, b, c):
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
    nx, ny, nz = u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
    return nx / l, ny / l, nz / l


lines = ["solid FishingRod"]
for a, b, c in tris:
    n = normal(a, b, c)
    lines.append(f"facet normal {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}")
    lines.append("outer loop")
    for p in (a, b, c):
        lines.append(f"vertex {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}")
    lines.append("endloop")
    lines.append("endfacet")
lines.append("endsolid FishingRod")
txt = "\n".join(lines)
open(f"{OUT}/fishing-rod.stl", "w").write(txt + "\n")
print("triangles", len(tris), "lines", len(lines))
