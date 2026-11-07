# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Geometry helpers: parse Material Symbols path data, rescale it from the
# viewBox "0 -960 960 960" to "0 0 24 24", split it into subpaths and islands
# (outline plus its holes), flatten curves, apply affine transforms and
# format path data. Only M L H V Q T C Z (absolute and relative) are handled,
# which covers the whole Material Symbols Rounded set.

import math
import re

_TOK = re.compile(r'[MmLlHhVvQqTtCcSsZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')


def fmt(v, nd=4):
    """Format a number like the existing outputs: at most nd decimals, no
    trailing zeros, no negative zero."""
    r = round(v, nd)
    if r == 0:
        r = 0.0
    s = ('%.' + str(nd) + 'f') % r
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    if s == '-0':
        s = '0'
    return s


class Seg:
    """One absolute command. cmd in M L Q T C Z. pts: list of (x, y)."""
    __slots__ = ('cmd', 'pts')

    def __init__(self, cmd, pts):
        self.cmd = cmd
        self.pts = pts

    def copy(self):
        return Seg(self.cmd, list(self.pts))


def load_source(svg_text):
    """Return subpaths (24 box) of a Material Symbols source file, honoring
    its viewBox (0 -960 960 960, legacy 0 96 960 960, or none = 24 box)."""
    m = re.search(r'viewBox="([^"]+)"', svg_text)
    vb = [float(v) for v in m.group(1).split()] if m else [0.0, 0.0, 24.0, 24.0]
    d = ''.join(re.findall(r' d="([^"]+)"', svg_text))
    subs = parse(d, rescale=False)
    k = 24.0 / vb[2]
    return [[Seg(s.cmd, [((px - vb[0]) * k, (py - vb[1]) * k) for px, py in s.pts]) for s in sp] for sp in subs]


def parse(d, rescale=True):
    """Parse path data into a list of subpaths (lists of Seg), absolute.
    H/V become L. Coordinates are rescaled to the 24 box when rescale."""
    toks = _TOK.findall(d)
    i = 0
    subs = []
    cur = None
    x = y = 0.0
    sx = sy = 0.0
    cmd = None

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    while i < len(toks):
        t = toks[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t
            i += 1
            if cmd in 'Zz':
                if cur is not None:
                    cur.append(Seg('Z', []))
                x, y = sx, sy
                continue
        elif cmd is None:
            raise ValueError('path data starts with a number')
        rel = cmd.islower()
        c = cmd.upper()
        if c == 'M':
            nx, ny = num(), num()
            if rel:
                nx += x
                ny += y
            cur = [Seg('M', [(nx, ny)])]
            subs.append(cur)
            x, y = sx, sy = nx, ny
            cmd = 'l' if rel else 'L'
        elif c == 'L':
            nx, ny = num(), num()
            if rel:
                nx += x
                ny += y
            cur.append(Seg('L', [(nx, ny)]))
            x, y = nx, ny
        elif c == 'H':
            nx = num()
            if rel:
                nx += x
            cur.append(Seg('L', [(nx, y)]))
            x = nx
        elif c == 'V':
            ny = num()
            if rel:
                ny += y
            cur.append(Seg('L', [(x, ny)]))
            y = ny
        elif c == 'Q':
            a, b, nx, ny = num(), num(), num(), num()
            if rel:
                a += x; b += y; nx += x; ny += y
            cur.append(Seg('Q', [(a, b), (nx, ny)]))
            x, y = nx, ny
        elif c == 'T':
            nx, ny = num(), num()
            if rel:
                nx += x
                ny += y
            cur.append(Seg('T', [(nx, ny)]))
            x, y = nx, ny
        elif c == 'C':
            a, b, e, f, nx, ny = [num() for _ in range(6)]
            if rel:
                a += x; b += y; e += x; f += y; nx += x; ny += y
            cur.append(Seg('C', [(a, b), (e, f), (nx, ny)]))
            x, y = nx, ny
        else:
            raise ValueError('unsupported command ' + cmd)
    if rescale:
        subs = [[Seg(s.cmd, [(px / 40.0, (py + 960.0) / 40.0) for px, py in s.pts]) for s in sp] for sp in subs]
    return subs


def to_d(subs, nd=4):
    out = []
    for sp in subs:
        for s in sp:
            if s.cmd == 'Z':
                out.append('Z')
            else:
                out.append(s.cmd + ' '.join(fmt(p[0], nd) + ' ' + fmt(p[1], nd) for p in s.pts))
    return ''.join(out)


def flatten(sp, steps=8):
    """Polyline of one subpath (closed implicitly)."""
    pts = []
    x = y = 0.0
    lastq = None
    for s in sp:
        if s.cmd == 'M':
            x, y = s.pts[0]
            pts.append((x, y))
            lastq = None
        elif s.cmd == 'L':
            x, y = s.pts[0]
            pts.append((x, y))
            lastq = None
        elif s.cmd in 'QT':
            if s.cmd == 'Q':
                (cx, cy), (nx, ny) = s.pts
            else:
                nx, ny = s.pts[0]
                if lastq is None:
                    cx, cy = x, y
                else:
                    cx, cy = 2 * x - lastq[0], 2 * y - lastq[1]
            for k in range(1, steps + 1):
                t = k / steps
                a = (1 - t) ** 2
                b = 2 * (1 - t) * t
                c = t * t
                pts.append((a * x + b * cx + c * nx, a * y + b * cy + c * ny))
            lastq = (cx, cy)
            x, y = nx, ny
        elif s.cmd == 'C':
            (c1x, c1y), (c2x, c2y), (nx, ny) = s.pts
            for k in range(1, steps + 1):
                t = k / steps
                mt = 1 - t
                pts.append((mt ** 3 * x + 3 * mt * mt * t * c1x + 3 * mt * t * t * c2x + t ** 3 * nx,
                            mt ** 3 * y + 3 * mt * mt * t * c1y + 3 * mt * t * t * c2y + t ** 3 * ny))
            lastq = None
            x, y = nx, ny
        elif s.cmd == 'Z':
            lastq = None
    return pts


def area(poly):
    a = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def bbox_union(bs):
    bs = [b for b in bs if b]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def pip(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            xx = xi + (y - yi) * (xj - xi) / (yj - yi)
            if x < xx:
                inside = not inside
        j = i
    return inside


def winding(pt, polys):
    """Nonzero winding number of pt against a list of closed polylines."""
    x, y = pt
    w = 0
    for poly in polys:
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if y1 <= y < y2 or y2 <= y < y1:
                xx = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if xx > x:
                    w += 1 if y2 > y1 else -1
    return w


class Island:
    def __init__(self, idx, outer, holes, subs):
        self.idx = idx
        self.outer = outer          # index into subs
        self.holes = holes          # indices into subs
        self.subs = subs            # reference to all subpaths
        self.poly = flatten(subs[outer])
        self.bbox = bbox(self.poly)
        self.area = abs(area(self.poly)) - sum(abs(area(flatten(subs[h]))) for h in holes)

    @property
    def sub_ids(self):
        return [self.outer] + list(self.holes)

    @property
    def center(self):
        b = self.bbox
        return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def islands(subs):
    """Group subpaths: each even-depth subpath is an island outline, odd-depth
    subpaths directly inside it are its holes. Zero-area subpaths dropped."""
    polys = [flatten(s) for s in subs]
    keep = [i for i, p in enumerate(polys) if len(p) >= 3 and abs(area(p)) > 1e-6]
    parent = {}
    depth = {}
    # containment by testing a few vertices of the candidate
    for i in keep:
        cands = []
        for j in keep:
            if i == j:
                continue
            if abs(area(polys[j])) <= abs(area(polys[i])):
                continue
            pts = polys[i]
            probe = [pts[k] for k in range(0, len(pts), max(1, len(pts) // 5))][:5]
            hits = sum(1 for p in probe if pip(p, polys[j]))
            if hits > len(probe) / 2:
                cands.append(j)
        # direct parent = smallest container
        if cands:
            parent[i] = min(cands, key=lambda j: abs(area(polys[j])))
    for i in keep:
        dd = 0
        k = i
        while k in parent:
            dd += 1
            k = parent[k]
        depth[i] = dd
    out = []
    for i in keep:
        if depth[i] % 2 == 0:
            holes = [h for h in keep if parent.get(h) == i and depth[h] % 2 == 1]
            out.append(Island(len(out), i, holes, subs))
    return out


# ---------------------------------------------------------------- transforms

def mat_mul(a, b):
    # 2x3 affine matrices (a, b, c, d, e, f) meaning x' = a x + c y + e, y' = b x + d y + f
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


IDENT = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _rot(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (c, s, -s, c, 0.0, 0.0)


def mat_trs(tx, ty, rot_deg, sx, sy, px, py, axis=0.0):
    """translate(tx,ty) translate(p) rotate(axis) rotate scale rotate(-axis)
    translate(-p): the same composition used in both the SVG and the
    Android groups."""
    m = (1.0, 0.0, 0.0, 1.0, -px, -py)
    if axis:
        m = mat_mul(_rot(-axis), m)
    m = mat_mul((sx, 0.0, 0.0, sy, 0.0, 0.0), m)
    m = mat_mul(_rot(rot_deg), m)
    if axis:
        m = mat_mul(_rot(axis), m)
    m = mat_mul((1.0, 0.0, 0.0, 1.0, px + tx, py + ty), m)
    return m


def apply_pt(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def transform_subs(subs, m):
    return [[Seg(s.cmd, [apply_pt(m, p) for p in s.pts]) for s in sp] for sp in subs]


def reverse_poly_d(pts, nd=4):
    return 'M' + 'L'.join(fmt(x, nd) + ' ' + fmt(y, nd) for x, y in pts) + 'Z'


def poly_d(pts, nd=4):
    return 'M' + 'L'.join(fmt(x, nd) + ' ' + fmt(y, nd) for x, y in pts) + 'Z'
