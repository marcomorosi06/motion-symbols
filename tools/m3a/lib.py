# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Icon builder and motion vocabulary used by the per-icon specs.

import math
import os

import geom
import raster
from anim import (Track, Node, Clip, Icon, SPATIAL, SPATIAL_FAST, SPATIAL_SLOW,
                  EFFECTS, EFFECTS_FAST, EFFECTS_SLOW, BOUNCY, SOFT)

# Folder symbols/web of google/material-design-icons at the commit in
# manifest.json (source_commit).
SRC = os.environ.get('M3A_SRC', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                                             'material-design-icons', 'symbols', 'web'))


def source_text(name):
    with open(os.path.join(SRC, name, 'materialsymbolsrounded', name + '_24px.svg')) as f:
        return f.read()


def source_exists(name):
    return os.path.exists(os.path.join(SRC, name, 'materialsymbolsrounded', name + '_24px.svg'))


def load(name):
    subs = geom.load_source(source_text(name))
    isl = geom.islands(subs)
    return subs, isl


# ------------------------------------------------------------- clip shapes

def _orient(pts, ccw):
    a = geom.area(pts)
    if (a > 0) != ccw:
        pts = pts[::-1]
    return pts


def R(x0, y0, x1, y1):
    """Axis aligned rectangle polygon."""
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _grow(poly, d):
    """Offset a convex polygon outward by d."""
    if not d:
        return list(poly)
    pts = _orient(list(poly), True)
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            return (dy / L, -dx / L)
        n0, n1 = nrm(p0, p1), nrm(p1, p2)
        bx, by = n0[0] + n1[0], n0[1] + n1[1]
        L = math.hypot(bx, by) or 1.0
        cosh = (bx * n0[0] + by * n0[1]) / L
        k = d / max(cosh, 0.3)
        out.append((p1[0] + bx / L * k, p1[1] + by / L * k))
    # make sure the growth went outward
    if abs(geom.area(out)) < abs(geom.area(pts)):
        return _grow([p for p in reversed(poly)], -d) if d > 0 else out
    return out


def band_pts(box, angle, lo, hi, margin=1.0):
    """Quad covering the part of box between fractions lo..hi along the
    direction angle (degrees, 0 = to the right, 90 = down)."""
    lo = max(0.0, min(1.0, lo))
    hi = max(0.0, min(1.0, hi))
    if hi < lo:
        hi = lo
    x0, y0, x1, y1 = box[0] - margin, box[1] - margin, box[2] + margin, box[3] + margin
    a = math.radians(angle)
    d = (math.cos(a), math.sin(a))
    n = (-d[1], d[0])
    cs = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    pr = [c[0] * d[0] + c[1] * d[1] for c in cs]
    qr = [c[0] * n[0] + c[1] * n[1] for c in cs]
    smin, smax = min(pr), max(pr)
    qmin, qmax = min(qr), max(qr)
    s0 = smin + (smax - smin) * lo
    s1 = smin + (smax - smin) * hi

    def P(s, q):
        return (d[0] * s + n[0] * q, d[1] * s + n[1] * q)
    return [P(s0, qmin), P(s1, qmin), P(s1, qmax), P(s0, qmax)]


def clip_band(box, angle, margin=1.0):
    """Clip visible between drivers lo and hi (rest lo=0, hi=1)."""
    lo = Track(0.0, 'p')
    hi = Track(1.0, 'p')

    def fn(v):
        return geom.poly_d(_orient(band_pts(box, angle, v[0], v[1], margin), True))
    return Clip(fn, [lo, hi]), lo, hi


def circle_pts(cx, cy, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def clip_radial(cx, cy, rmax, n=24):
    """Visible inside a circle of radius p*rmax (rest p=1)."""
    p = Track(1.0, 'p')

    def fn(v):
        r = max(0.0, v[0]) * rmax
        return geom.poly_d(_orient(circle_pts(cx, cy, r, n), True))
    return Clip(fn, [p]), p


def clip_sweep(cx, cy, R, a0, span, n=36):
    """Pie from angle a0 (deg, 0 = 12 o'clock, clockwise) spanning p*span."""
    p = Track(1.0, 'p')

    def fn(v):
        f = max(0.0, min(1.0, v[0]))
        pts = [(cx, cy)]
        for k in range(n + 1):
            a = math.radians(a0 + span * f * k / n - 90)
            pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
        return geom.poly_d(_orient(pts, True))
    return Clip(fn, [p]), p


BIG = [(-30.0, -30.0), (54.0, -30.0), (54.0, 54.0), (-30.0, 54.0)]


def complement_d(inner_pts):
    outer = _orient(list(BIG), True)
    inner = _orient(list(inner_pts), False)
    if abs(geom.area(inner_pts)) < 1e-9:
        inner = list(inner_pts)
    return geom.poly_d(outer) + geom.poly_d(inner)


# ------------------------------------------------------------- builder

class B:
    """Per-icon builder. Islands are indexed in source order (see sheets)."""

    def __init__(self, name):
        self.name = name
        self.subs, self.isl = load(name)
        self.used = set()
        self.nodes = {}
        self.root = Node('all', [], (12.0, 12.0))
        self.nodes['all'] = self.root
        self.fixes_note = None
        self.static_subs = [self.subs[k] for I in self.isl for k in I.sub_ids]
        self.static_subs = [self.subs[k] for k in sorted(k for I in self.isl for k in I.sub_ids)]
        self.splits = []

    # selection ----------------------------------------------------------
    def I(self, *ids):
        return [self.isl[i] for i in ids]

    def where(self, f):
        return [I for I in self.isl if f(I)]

    def box(self, x0, y0, x1, y1):
        return self.where(lambda I: x0 <= I.center[0] <= x1 and y0 <= I.center[1] <= y1)

    def rest(self):
        return [I for I in self.isl if I.idx not in self.used]

    def all(self):
        return list(self.isl)

    def bbox_of(self, isls):
        return geom.bbox_union([I.bbox for I in isls])

    # parts --------------------------------------------------------------
    def part(self, name, isls, pivot='c', parent=None, drop_holes=()):
        if isinstance(isls, geom.Island):
            isls = [isls]
        isls = list(isls)
        for I in isls:
            if I.idx in self.used:
                raise ValueError('%s: island %d used twice' % (self.name, I.idx))
            self.used.add(I.idx)
        ids = []
        for I in isls:
            ids += [k for k in I.sub_ids if k not in drop_holes]
        subs = [self.subs[k] for k in sorted(ids)]
        bb = self.bbox_of(isls) if isls else (12, 12, 12, 12)
        n = Node(name, subs, self.pivot(pivot, bb))
        n.bb = bb
        n.isl = isls
        self._attach(n, parent)
        return n

    def geo_part(self, name, subs, pivot='c', parent=None):
        pts = [p for sp in subs for p in geom.flatten(sp)]
        bb = geom.bbox(pts) if pts else (12.0, 12.0, 12.0, 12.0)
        n = Node(name, list(subs), self.pivot(pivot, bb))
        n.bb = bb
        n.isl = []
        self._attach(n, parent)
        return n

    def bake(self, name, host, isls, pivot='c'):
        """Move whole islands into host's path (animated by path morphing),
        so that shapes that touch at rest share one path and show no
        antialiasing seam."""
        if isinstance(isls, geom.Island):
            isls = [isls]
        ids = []
        for I in isls:
            if I.idx in self.used:
                raise ValueError('%s: island %d used twice' % (self.name, I.idx))
            self.used.add(I.idx)
            ids += I.sub_ids
        subs = [self.subs[k] for k in sorted(ids)]
        bb = self.bbox_of(isls)
        n = Node(name, subs, self.pivot(pivot, bb))
        n.bb = bb
        host.baked.append(n)
        return n

    def hole(self, name, host, island, k, pivot='c'):
        """Bake hole k of island (already inside host) into host's path."""
        sid = island.holes[k]
        sub = self.subs[sid]
        host.subs = [s for s in host.subs if s is not sub]
        bb = geom.bbox(geom.flatten(sub))
        n = Node(name, [sub], self.pivot(pivot, bb))
        n.bb = bb
        host.baked.append(n)
        return n

    def group(self, name, children, pivot='c', parent=None):
        bb = geom.bbox_union([c.bb for c in children])
        n = Node(name, [], self.pivot(pivot, bb))
        n.bb = bb
        n.isl = []
        for c in children:
            self._detach(c)
            n.children.append(c)
        self._attach(n, parent)
        return n

    def _detach(self, c):
        for m in self.nodes.values():
            if c in m.children:
                m.children.remove(c)

    def _attach(self, n, parent):
        if n.name in self.nodes:
            raise ValueError('duplicate node ' + n.name)
        self.nodes[n.name] = n
        (parent or self.root).children.append(n)

    @staticmethod
    def pivot(p, bb):
        x0, y0, x1, y1 = bb
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if isinstance(p, tuple):
            return p
        return {'c': (cx, cy), 'b': (cx, y1), 't': (cx, y0), 'l': (x0, cy), 'r': (x1, cy),
                'bl': (x0, y1), 'br': (x1, y1), 'tl': (x0, y0), 'tr': (x1, y0),
                'icon': (12.0, 12.0)}[p]

    def split(self, name, isls, pieces, parent=None, grow=0.35, rest=True):
        """Cut islands into pieces with clips, like the head and the shaft
        of an arrow. pieces: list of (piece_name, polygon, pivot); a polygon
        is a list of points in the 24 box. A last piece named name + '_rest'
        gets everything outside the polygons. The untouched source path is
        drawn at rest; the pieces only while something moves (switched at the
        first and the last frame of the motion), so rest frames stay exact.
        Returns (group, {piece_name: node})."""
        if isinstance(isls, geom.Island):
            isls = [isls]
        isls = list(isls)
        src = self.part(name + '_src', isls)
        subs = list(src.subs)
        grp = self.group(name, [src], pivot='c', parent=parent)
        nodes = {}
        polys = []
        for pname, poly, pivot in pieces:
            n = self.geo_part(pname, subs, pivot=pivot, parent=grp)
            gp = _grow(poly, grow)
            n.clip = Clip((lambda d: (lambda v: d))(geom.poly_d(_orient(gp, True))), [], space='inner')
            n.bb = geom.bbox(poly)
            nodes[pname] = n
            polys.append(poly)
        if rest:
            # the excluded polygons must not overlap (nonzero winding)
            rn = self.geo_part(name + '_rest', subs, pivot='c', parent=grp)
            outer = _orient(list(BIG), True)
            d = geom.poly_d(outer) + ''.join(geom.poly_d(_orient(list(p), False)) for p in polys)
            rn.clip = Clip((lambda d: (lambda v: d))(d), [], space='inner')
            nodes[name + '_rest'] = rn
        self.splits.append((grp, src, list(nodes.values())))
        return grp, nodes

    def _finish_splits(self):
        for grp, src, pieces in self.splits:
            skip = {id(src.alpha)} | {id(p.alpha) for p in pieces}
            # every motion inside the split group (pieces, wrappers, clips);
            # the group's own transform is shared by source and pieces
            trs = [x for x in grp.all_tracks() if id(x) not in skip]
            t_end = max([tr.settle_time() for tr in trs if tr.animated] + [0.0])
            t_end = 2.0 * math.ceil((t_end + 4.0) / 2.0)
            src.alpha.snap(2, 0.0)
            src.alpha.snap(t_end, 1.0)
            for p in pieces:
                p.alpha = Track(0.0, 'a')
                p.alpha.snap(2, 1.0)
                p.alpha.snap(t_end, 0.0)

    def finish(self, concept):
        left = self.rest()
        if left:
            raise ValueError('%s: islands not assigned: %s' % (self.name, [I.idx for I in left]))
        self._finish_splits()
        if self.splits:
            note = 'While moving, parts of the path are drawn as clipped pieces; at rest the original path is drawn.'
            self.fixes_note = (self.fixes_note + ' ' + note) if self.fixes_note else note
        # internal helper nodes (source copies, clip wrappers) are not parts
        parts = [n for n in self.nodes if n != 'all' and not n.endswith(('_src', '_w'))]
        return Icon(self.name, self.root, concept, parts, self.static_subs,
                    self.fixes_note)


# ------------------------------------------------------------- vocabulary
# Every helper takes a start time t (ms) and returns the time at which the
# gesture can be considered visually done, so that helpers can be chained.

def press(n, t, s=0.85, hold=110, spec_in=SPATIAL, spec_out=SPATIAL_FAST):
    """Squeeze uniformly and spring back with overshoot."""
    n.sx.to(t, s, spec_in)
    n.sy.to(t, s, spec_in)
    n.sx.back(t + hold, spec_out)
    n.sy.back(t + hold, spec_out)
    return t + hold + 250


def swell(n, t, s=1.12, hold=120, spec_out=SPATIAL_FAST):
    return press(n, t, s, hold, SPATIAL, spec_out)


def pressxy(n, t, sx=0.9, sy=0.9, hold=110, spec_out=SPATIAL_FAST):
    if sx != 1:
        n.sx.to(t, sx, SPATIAL)
        n.sx.back(t + hold, spec_out)
    if sy != 1:
        n.sy.to(t, sy, SPATIAL)
        n.sy.back(t + hold, spec_out)
    return t + hold + 250


def squash(n, t, amt=0.14, hold=100, spec_out=BOUNCY):
    """Squash on its pivot (use a bottom pivot): wider and lower."""
    n.sy.to(t, 1 - amt, SPATIAL)
    n.sx.to(t, 1 + amt * 0.6, SPATIAL)
    n.sy.back(t + hold, spec_out)
    n.sx.back(t + hold, spec_out)
    return t + hold + 300


def hop(n, t, h=2.0, ant=70, air=170, land=True, stretch=1.06):
    """Anticipation squash, jump up, fall and land with a squash.
    The node pivot should be at its bottom."""
    n.sy.to(t, 0.9, SPATIAL_FAST)
    n.sx.to(t, 1.06, SPATIAL_FAST)
    t1 = t + ant
    n.sy.to(t1, stretch, SPATIAL_FAST)
    n.sx.to(t1, 1.0 - (stretch - 1.0) * 0.67, SPATIAL_FAST)
    n.ty.to(t1, -h, SPATIAL)
    t2 = t1 + air
    n.ty.to(t2, 0.0, (700.0, 0.9))
    n.sy.to(t2, 1.0, SPATIAL)
    n.sx.to(t2, 1.0, SPATIAL)
    t3 = t2 + 95
    if land:
        n.sy.to(t3, 0.9, SPATIAL_FAST)
        n.sx.to(t3, 1.07, SPATIAL_FAST)
        n.sy.back(t3 + 70, BOUNCY)
        n.sx.back(t3 + 70, BOUNCY)
    return t3 + 300


def lift(n, t, dy=-1.5, hold=150, spec_out=BOUNCY):
    n.ty.to(t, dy, SPATIAL)
    n.ty.back(t + hold, spec_out)
    return t + hold + 300


def shift(n, t, dx=0.0, dy=0.0, hold=150, spec_in=SPATIAL, spec_out=BOUNCY):
    if dx:
        n.tx.to(t, dx, spec_in)
        n.tx.back(t + hold, spec_out)
    if dy:
        n.ty.to(t, dy, spec_in)
        n.ty.back(t + hold, spec_out)
    return t + hold + 300


def nod(n, t, deg=12, hold=120, spec_out=BOUNCY):
    n.rot.to(t, deg, SPATIAL)
    n.rot.back(t + hold, spec_out)
    return t + hold + 300


def rock(n, t, deg=10, n_half=2, dt=150, spec=SPATIAL):
    """Rock side to side n_half times then settle."""
    s = 1
    for i in range(n_half):
        n.rot.to(t + i * dt, deg * s, spec)
        s = -s
    n.rot.back(t + n_half * dt, BOUNCY)
    return t + n_half * dt + 300


def wobble(n, t, v=500.0, ch='rot', spec=BOUNCY):
    """Velocity kick: a damped wobble around rest."""
    getattr(n, ch).kick(t, v, spec)
    return t + 400


def jolt(n, t, dx=0.0, dy=0.0, v=60.0):
    if dx:
        n.tx.kick(t, v * dx, BOUNCY)
    if dy:
        n.ty.kick(t, v * dy, BOUNCY)
    return t + 350


def spin(n, t, deg, spec=SPATIAL):
    """Rotate by a symmetric amount and land on itself; the rest value is
    restored with an invisible snap once settled."""
    n.rot.to(t, deg, spec)
    te = t + settle_ms(spec, deg, 'r')
    n.rot.snap(te, 0.0)
    return te


def settle_ms(spec, dist, kind):
    tr = Track(0.0, kind)
    tr.to(0, dist, spec)
    tr2 = Track(dist, kind)
    tr2.ev = [('snap', 0.0, 0.0, None), ('to', 0.0, dist, spec)]
    # settle of tr2 around its rest = dist
    t = 0.0
    from anim import THRESH
    thr = THRESH[kind] * 0.5
    ok = None
    while t < 5000:
        x = tr2.value(t)
        if abs(x - dist) < thr:
            if ok is None:
                ok = t
            if t - ok > 30:
                return 2.0 * math.ceil(ok / 2.0)
        else:
            ok = None
        t += 2.0
    return 5000


def pop(n, t, low=0.0, dt=90, spec_in=EFFECTS_FAST, spec_out=BOUNCY):
    """Shrink away fast, then pop back in with a bounce."""
    n.sx.to(t, low, spec_in)
    n.sy.to(t, low, spec_in)
    n.sx.back(t + dt, spec_out)
    n.sy.back(t + dt, spec_out)
    return t + dt + 350


def blink(n, t, low=0.25, hold=90, spec=EFFECTS):
    n.alpha.to(t, low, spec)
    n.alpha.back(t + hold, spec)
    return t + hold + 150


def fade_out_in(n, t, hold=100):
    n.alpha.to(t, 0.0, EFFECTS_FAST)
    n.alpha.back(t + hold, EFFECTS)
    return t + hold + 150


def stagger(nodes, t, dt, fn, **kw):
    end = t
    for i, n in enumerate(nodes):
        end = max(end, fn(n, t + i * dt, **kw))
    return end


def redraw(b, n, t, angle=0.0, erase_ms=110, spec_in=EFFECTS_FAST, spec_draw=SPATIAL, margin=0.6, space='outer'):
    """Erase along angle, then draw in again along the same direction."""
    clip, lo, hi = clip_band(n.bb, angle, margin)
    clip.space = space
    n.clip = clip
    lo.to(t, 1.0, spec_in)
    t1 = t + erase_ms
    lo.snap(t1, 0.0)
    hi.snap(t1, 0.0)
    hi.to(t1 + 2, 1.0, spec_draw)
    return t1 + 260


def reveal(b, n, t, angle=0.0, hide_ms=70, spec=SPATIAL, margin=0.6):
    """Hide quickly (from the far side) and draw in along angle."""
    clip, lo, hi = clip_band(n.bb, angle, margin)
    n.clip = clip
    hi.to(t, 0.0, EFFECTS_FAST)
    hi.to(t + hide_ms, 1.0, spec)
    return t + hide_ms + 260


def wipe_out_in(b, n, t, angle=0.0, spec_out=EFFECTS, spec_in=SPATIAL, hold=40, margin=0.6):
    """Retract toward the start (hi -> 0), then extend again (hi -> 1)."""
    clip, lo, hi = clip_band(n.bb, angle, margin)
    n.clip = clip
    hi.to(t, 0.0, spec_out)
    hi.to(t + 150 + hold, 1.0, spec_in)
    return t + 150 + hold + 260


def roll(b, n, t, dy=None, up=True, spec_out=SPATIAL, spec_in=SPATIAL_FAST, gap=100, window=None):
    """Odometer: the part rolls out of its own window and back in from
    the other side."""
    bb = window or n.bb
    h = (bb[3] - bb[1]) + 0.6 if dy is None else dy
    s = -1 if up else 1
    clip, lo, hi = clip_band((bb[0] - 0.3, bb[1] - 0.15, bb[2] + 0.3, bb[3] + 0.15), 0, margin=0.0)
    n.clip = clip
    n.ty.to(t, s * h, spec_out)
    t1 = t + gap
    # once outside the window, jump to the other side
    n.ty.snap(t1, -s * h)
    n.ty.to(t1 + 2, 0.0, spec_in)
    return t1 + 300


def slide_through(b, n, t, dx=0.0, dy=0.0, window=None, gap=110, spec_out=SPATIAL, spec_in=SPATIAL_FAST, margin=0.3):
    """Leave the window in (dx, dy) and come back in from the other side."""
    bb = window or n.bb
    clip, lo, hi = clip_band((bb[0] - margin, bb[1] - margin, bb[2] + margin, bb[3] + margin), 0, margin=0.0)
    n.clip = clip
    if dx:
        n.tx.to(t, dx, spec_out)
        n.tx.snap(t + gap, -dx)
        n.tx.to(t + gap + 2, 0.0, spec_in)
    if dy:
        n.ty.to(t, dy, spec_out)
        n.ty.snap(t + gap, -dy)
        n.ty.to(t + gap + 2, 0.0, spec_in)
    return t + gap + 300


def window_clip(n, box):
    clip, lo, hi = clip_band(box, 0, margin=0.0)
    n.clip = clip
    return clip


def level(b, n, t, angle=-90, low=0.0, spec_down=SPATIAL, spec_up=SPATIAL_SLOW, hold=60, margin=0.4):
    """A fill that drains (toward the start of angle) and fills again.
    Default angle -90 = fills upward (from bottom to top)."""
    clip, lo, hi = clip_band(n.bb, angle, margin)
    n.clip = clip
    hi.to(t, low, spec_down)
    hi.to(t + 160 + hold, 1.0, spec_up)
    return t + 160 + hold + 380


def sweep(b, n, t, cx, cy, R, a0=0, span=360, low=0.0, spec_down=EFFECTS, spec_up=SPATIAL_SLOW, hold=60):
    clip, p = clip_sweep(cx, cy, R, a0, span)
    n.clip = clip
    p.to(t, low, spec_down)
    p.to(t + 140 + hold, 1.0, spec_up)
    return t + 140 + hold + 400


def radial_pop(b, n, t, low=0.0, spec_in=EFFECTS_FAST, spec_out=SPATIAL):
    bb = n.bb
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    r = math.hypot(bb[2] - bb[0], bb[3] - bb[1]) / 2 + 0.4
    clip, p = clip_radial(cx, cy, r)
    n.clip = clip
    p.to(t, low, spec_in)
    p.to(t + 90, 1.0, spec_out)
    return t + 90 + 350


# ------------------------------------------------------------- _off icons

def slash_geometry(off_name, on_name, on_subs=None):
    """Find the slash line and the corridor half width from rasters of the
    off and on icons. Returns (A, B, hw, mismatch) where A is the start (the
    upper end) and mismatch the fraction of differing pixels outside the
    corridor."""
    off = raster.rasterize(geom.load_source(source_text(off_name)))
    on = raster.rasterize(on_subs if on_subs is not None else geom.load_source(source_text(on_name)))
    return raster.slash_fit(off, on)


def off_icon(b, on_name, start='top', parts=None, retract_ms=170, spec_back=SPATIAL, t=0, on_subs=None,
             on_note=None):
    """Standard _off gesture. The off geometry (b's islands, or the parts
    given) goes in a wrapper clipped to the complement of the retracted part
    of the corridor; the on icon is drawn only inside it.
    Returns (wrapper_off, on_node, t_end, (A, B, hw))."""
    A, B, hw, mism = slash_geometry(b.name, on_name, on_subs)
    if start == 'bottom':
        A, B = B, A
    if on_subs is None:
        on_subs = geom.load_source(source_text(on_name))
    on_isl = geom.islands(on_subs)
    on_keep = [on_subs[k] for k in sorted(k for I in on_isl for k in I.sub_ids)]
    p = Track(1.0, 'p')
    ax, ay = A
    bx, by = B
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    ext = hw + 0.4

    def region(v, grow=0.0):
        f = max(0.0, min(1.0, v[0]))
        # retracted part of the corridor: from A + f (B - A) to past B; when
        # fully retracted it also covers the cap before A
        if f >= 1.0:
            s0 = s1 = L
            g = 0.0
        else:
            s0 = f * L - (1.0 - f) * ext - grow
            s1 = L + ext + grow
            g = grow
        w = hw + g
        return [(ax + ux * s0 - nx * w, ay + uy * s0 - ny * w), (ax + ux * s1 - nx * w, ay + uy * s1 - ny * w),
                (ax + ux * s1 + nx * w, ay + uy * s1 + ny * w), (ax + ux * s0 + nx * w, ay + uy * s0 + ny * w)]

    def f_off(v):
        return complement_d(region(v))

    def f_on(v):
        # slightly larger than the hole in the off layer: no antialiasing seam
        pts = region(v, 0.2)
        return geom.poly_d(_orient(pts, True)) if abs(geom.area(pts)) > 1e-9 else geom.poly_d(pts)

    off_wrap = Node('off', [], (12.0, 12.0))
    off_wrap.bb = (0, 0, 24, 24)
    off_wrap.isl = []
    off_wrap.clip = Clip(f_off, [p])
    on = Node('on_layer', on_keep, (12.0, 12.0))
    on.bb = (0, 0, 24, 24)
    on.isl = []
    on.clip = Clip(f_on, [p])
    b.nodes['off'] = off_wrap
    b.nodes['on_layer'] = on
    # move existing root children into the off wrapper
    for c in list(b.root.children):
        b.root.children.remove(c)
        off_wrap.children.append(c)
    b.root.children += [off_wrap, on]
    # gesture: retract, hold, cut across again
    p.to(t, 0.0, EFFECTS)
    p.to(t + retract_ms + 160, 1.0, spec_back)
    b.off_meta = (A, B, hw, mism)
    b.fixes_note = on_note or ("While moving, the slash is retracted over the '%s' icon of the same set." % on_name)
    return off_wrap, on, t + retract_ms + 160 + 230


# ------------------------------------------------------------- registry

SPECS = {}


def spec(*names):
    """Register a spec function for one or more icons. The function gets a
    builder B and returns the concept sentence."""
    def deco(fn):
        for n in names:
            if n in SPECS:
                raise ValueError('spec defined twice: ' + n)
            SPECS[n] = fn
        return fn
    return deco


def build_icon(name):
    b = B(name)
    concept = SPECS[name](b)
    ic = b.finish(concept)
    ic.builder = b
    return ic


# ------------------------------------------------------------- more vocabulary

def dart(n, t, dx, dy, wind=0.35, go=90, hold=110):
    """Wind back against (dx, dy), dart along it and spring home."""
    if dx:
        n.tx.to(t, -dx * wind, SPATIAL)
        n.tx.to(t + go, dx, SPATIAL_FAST)
        n.tx.back(t + go + hold, BOUNCY)
    if dy:
        n.ty.to(t, -dy * wind, SPATIAL)
        n.ty.to(t + go, dy, SPATIAL_FAST)
        n.ty.back(t + go + hold, BOUNCY)
    return t + go + hold + 300


def plus_badge(n, t, s=0.6):
    """The plus contracts and springs back (it never rotates)."""
    return press(n, t, s, hold=90, spec_in=SPATIAL_FAST, spec_out=BOUNCY)


def alert_badge(n, t, deg=14):
    """The alert badge pops and shakes."""
    pop(n, t, 0.3, dt=80)
    n.rot.kick(t + 160, 900.0 * deg / 14.0, BOUNCY)
    return t + 600


def ring(n, t, deg=16):
    """A ringing shake: fast damped wobble."""
    n.rot.kick(t, 1300.0 * deg / 16.0, (900.0, 0.18))
    return t + 700


def flicker(n, t, s=0.12):
    """Flame-like flicker on a bottom pivot."""
    n.sy.to(t, 1 + s, SPATIAL_FAST)
    n.sx.to(t, 1 - s * 0.6, SPATIAL_FAST)
    n.sy.to(t + 80, 1 - s * 0.6, SPATIAL_FAST)
    n.sx.to(t + 80, 1 + s * 0.4, SPATIAL_FAST)
    n.sy.back(t + 160, BOUNCY)
    n.sx.back(t + 160, BOUNCY)
    n.rot.kick(t + 40, 260.0, BOUNCY)
    return t + 500


def check_draw(b, n, t, angle=0.0, pop_s=1.18):
    """The check is erased and drawn again, popping at the end."""
    e = redraw(b, n, t, angle, erase_ms=100, spec_draw=SPATIAL)
    n.sx.to(e - 60, pop_s, SPATIAL)
    n.sy.to(e - 60, pop_s, SPATIAL)
    n.sx.back(e + 40, BOUNCY)
    n.sy.back(e + 40, BOUNCY)
    return e + 300


def symmetry_error(subs, angle, center):
    """Fraction of differing pixels between a shape and itself rotated by
    angle about center (used to pick spins that land on themselves)."""
    m = geom.mat_trs(0, 0, angle, 1, 1, center[0], center[1])
    a = raster.rasterize(subs)
    b2 = raster.rasterize(geom.transform_subs(subs, m))
    return float((a ^ b2).sum()) / float(max(1, a.sum()))


def best_center(subs, angle, guess, span=2.0, step=0.1):
    """Search the rotation center that makes a shape land on itself."""
    best = (9.0, guess)
    for coarse in (True, False):
        g = best[1]
        s = span if coarse else step * 3
        st = step * 3 if coarse else step / 3
        k = int(round(s / st))
        for i in range(-k, k + 1):
            for j in range(-k, k + 1):
                c = (g[0] + i * st, g[1] + j * st)
                e = symmetry_error(subs, angle, c)
                if e < best[0]:
                    best = (e, c)
    return best


def rounded_path(pts, r):
    """Closed polygon with rounded corners (quadratic), as subpaths."""
    n = len(pts)
    d = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def toward(a, b, k):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            k = min(k, L / 2)
            return (a[0] + dx / L * k, a[1] + dy / L * k)
        a = toward(p1, p0, r)
        c = toward(p1, p2, r)
        d.append(('L' if d else 'M') + '%r %r' % a)
        d.append('Q%r %r %r %r' % (p1[0], p1[1], c[0], c[1]))
    return geom.parse(''.join(d) + 'Z', rescale=False)


def circle_path(cx, cy, r, n=8):
    """Circle made of n quadratic segments."""
    rc = r / math.cos(math.pi / n)
    d = 'M%r %r' % (cx + r, cy)
    for k in range(n):
        a1 = 2 * math.pi * (k + 0.5) / n
        a2 = 2 * math.pi * (k + 1) / n
        d += 'Q%r %r %r %r' % (cx + rc * math.cos(a1), cy + rc * math.sin(a1), cx + r * math.cos(a2), cy + r * math.sin(a2))
    return geom.parse(d + 'Z', rescale=False)


# ------------------------------------------------------------- arrows (old set style)

def _u(angle):
    a = math.radians(angle)
    return math.cos(a), math.sin(a)


def shoot(n, t, angle, dist=1.6, wind=0.55, sq=0.82, st=1.12, go=95, hold=110, spec_back=BOUNCY):
    """Arrow move of the old set: winds back against its direction squashing
    along it, darts forward stretching, and springs home. angle: direction
    in degrees (0 right, 90 down). Sets the node axis to the direction."""
    n.axis = float(angle)
    ux, uy = _u(angle)
    t1 = t + go
    for tr, u in ((n.tx, ux), (n.ty, uy)):
        if abs(u) > 1e-6:
            tr.to(t, -u * wind, SPATIAL)
            tr.to(t1, u * dist, SPATIAL_FAST)
            tr.back(t1 + hold, spec_back)
    n.sx.to(t, sq, SPATIAL)
    n.sy.to(t, 1 + (1 - sq) * 0.45, SPATIAL)
    n.sx.to(t1, st, SPATIAL_FAST)
    n.sy.to(t1, 1 - (st - 1) * 0.5, SPATIAL_FAST)
    n.sx.back(t1 + 70, SPATIAL_FAST)
    n.sy.back(t1 + 70, SPATIAL_FAST)
    return t1 + hold + 320


def elastic(head, shaft, t, angle, L, dist=1.6, wind=0.5, go=95, hold=110, spec_back=BOUNCY):
    """The head darts along angle while the shaft, anchored at its tail
    (shaft pivot), stretches to stay attached, like a rubber band. L is the
    shaft length from the tail to the cut."""
    ux, uy = _u(angle)
    shaft.axis = float(angle)
    t1 = t + go
    for d, spec_, tt in ((-wind, SPATIAL, t), (dist, SPATIAL_FAST, t1)):
        for tr, u in ((head.tx, ux), (head.ty, uy)):
            if abs(u) > 1e-6:
                tr.to(tt, u * d, spec_)
        shaft.sx.to(tt, 1 + d / L, spec_)
    for tr, u in ((head.tx, ux), (head.ty, uy)):
        if abs(u) > 1e-6:
            tr.back(t1 + hold, spec_back)
    shaft.sx.back(t1 + hold, spec_back)
    return t1 + hold + 320


def through(n, t, dx, dy, window=(0.0, 0.0, 24.0, 24.0), gap=120, spec_out=SPATIAL, spec_in=SPATIAL_FAST):
    """Leave the window along (dx, dy) and come back in from the other side
    (old arrow_circle style). The clip moves with nothing: it is the window."""
    clip, lo, hi = clip_band(window, 0, margin=0.0)
    n.clip = clip
    for tr, d in ((n.tx, dx), (n.ty, dy)):
        if d:
            tr.to(t, d, spec_out)
            tr.snap(t + gap, -d)
            tr.to(t + gap + 2, 0.0, spec_in)
    return t + gap + 320
