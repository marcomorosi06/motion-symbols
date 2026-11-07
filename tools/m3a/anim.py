# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Motion model: spring tracks (Compose SpringSpec physics, M3 Expressive
# motion scheme tokens), a tree of animated parts, clip and morph drivers,
# sampling and keyframe reduction. Emitters live in emit.py.

import math

# M3 Expressive motion scheme (Compose MotionScheme.expressive()).
# (stiffness, damping ratio). Spatial: may overshoot. Effects: never overshoot.
SPATIAL_FAST = (800.0, 0.6)
SPATIAL = (380.0, 0.8)
SPATIAL_SLOW = (200.0, 0.8)
EFFECTS_FAST = (3800.0, 1.0)
EFFECTS = (1600.0, 1.0)
EFFECTS_SLOW = (800.0, 1.0)
# Extra bouncy spring for playful landings (still a Compose-style spring).
BOUNCY = (500.0, 0.45)
SOFT = (120.0, 0.75)

STEP_MS = 2.0          # sampling grid
HOLD_MS = 900          # pause appended for the loop variant

# visibility thresholds per channel kind
THRESH = {'t': 0.004, 'r': 0.05, 's': 0.0006, 'a': 0.003, 'p': 0.0008}


def spring_eval(u0, v0, k, z, t):
    """Displacement and velocity of a unit-mass spring after t seconds."""
    w0 = math.sqrt(k)
    if t <= 0:
        return u0, v0
    if z < 1.0:
        wd = w0 * math.sqrt(1 - z * z)
        a = u0
        b = (v0 + z * w0 * u0) / wd
        e = math.exp(-z * w0 * t)
        c, s = math.cos(wd * t), math.sin(wd * t)
        u = e * (a * c + b * s)
        v = e * ((-z * w0) * (a * c + b * s) + (-a * wd * s + b * wd * c))
        return u, v
    if abs(z - 1.0) < 1e-9:
        b = v0 + w0 * u0
        e = math.exp(-w0 * t)
        u = (u0 + b * t) * e
        v = (b - w0 * (u0 + b * t)) * e
        return u, v
    r = w0 * math.sqrt(z * z - 1)
    r1 = -z * w0 + r
    r2 = -z * w0 - r
    c2 = (v0 - r1 * u0) / (r2 - r1)
    c1 = u0 - c2
    u = c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t)
    v = c1 * r1 * math.exp(r1 * t) + c2 * r2 * math.exp(r2 * t)
    return u, v


def ease_emph(x):
    # cubic bezier approximation of M3 standard easing (0.2, 0, 0, 1)
    return 1 - (1 - x) ** 3 if x < 1 else 1.0


class Track:
    """Scalar animatable. Events: ('to', t_ms, target, spec),
    ('snap', t_ms, value), ('kick', t_ms, dv_per_s), ('tween', t_ms, target, dur_ms, ease)."""

    def __init__(self, rest, kind):
        self.rest = rest
        self.kind = kind
        self.ev = []
        self._cache = None
        self.end = None

    def to(self, t, target, spec=SPATIAL):
        self.ev.append(('to', float(t), float(target), spec))
        self._cache = None
        return self

    def back(self, t, spec=SPATIAL_FAST):
        return self.to(t, self.rest, spec)

    def snap(self, t, value):
        t = 2.0 * round(t / 2.0)
        self.ev.append(('snap', float(t), float(value), None))
        self._cache = None
        return self

    def kick(self, t, dv, spec=SPATIAL_FAST):
        """Add velocity (units per second) and keep springing to the
        current target (or to rest when idle)."""
        self.ev.append(('kick', float(t), float(dv), spec))
        self._cache = None
        return self

    def tween(self, t, target, dur, ease='emph'):
        self.ev.append(('tween', float(t), float(target), (float(dur), ease)))
        self._cache = None
        return self

    @property
    def animated(self):
        return bool(self.ev)

    def snap_times(self):
        return [e[1] for e in self.ev if e[0] == 'snap']

    def _segments(self):
        if self._cache is not None:
            return self._cache
        evs = sorted(self.ev, key=lambda e: e[1])
        segs = []   # (t_start, x0, v0, mode, params)
        x, v = self.rest, 0.0
        tgt, spec = self.rest, SPATIAL_FAST
        t0 = 0.0
        mode = ('spring', tgt, spec)
        for e in evs:
            kind, te = e[0], e[1]
            # state at te under current mode
            x, v = self._advance(t0, x, v, mode, te)
            t0 = te
            if kind == 'to':
                mode = ('spring', e[2], e[3])
            elif kind == 'snap':
                x, v = e[2], 0.0
                mode = ('spring', e[2], SPATIAL_FAST)
            elif kind == 'kick':
                v += e[2]
                if mode[0] == 'tween':
                    mode = ('spring', mode[1], e[3])
                else:
                    mode = ('spring', mode[1], e[3])
            elif kind == 'tween':
                mode = ('tween', x, e[2], te, e[3][0], e[3][1])
            segs.append((t0, x, v, mode))
        self._cache = ([(0.0, self.rest, 0.0, ('spring', self.rest, SPATIAL_FAST))] + segs)
        return self._cache

    @staticmethod
    def _advance(t0, x, v, mode, t):
        if mode[0] == 'spring':
            tgt, (k, z) = mode[1], mode[2]
            u, vv = spring_eval(x - tgt, v, k, z, (t - t0) / 1000.0)
            return tgt + u, vv
        _, a, b, ts, dur, ease = mode
        f = min(1.0, max(0.0, (t - ts) / dur))
        g = ease_emph(f) if ease == 'emph' else f
        if f >= 1.0:
            return b, 0.0
        # numeric velocity
        f2 = min(1.0, (t + 0.5 - ts) / dur)
        g2 = ease_emph(f2) if ease == 'emph' else f2
        return a + (b - a) * g, (b - a) * (g2 - g) / 0.0005

    def value(self, t):
        if self.end is not None and t >= self.end:
            return self.rest
        segs = self._segments()
        lo = 0
        for i, s in enumerate(segs):
            if s[0] <= t:
                lo = i
            else:
                break
        t0, x, v, mode = segs[lo]
        return self._advance(t0, x, v, mode, t)[0]

    def final_target(self):
        segs = self._segments()
        m = segs[-1][3]
        return m[1] if m[0] == 'spring' else m[2]

    def settle_time(self):
        if not self.ev:
            return 0.0
        segs = self._segments()
        tlast = segs[-1][0]
        thr = THRESH[self.kind]
        t = tlast
        # walk forward until within threshold for 40 ms
        ok_since = None
        while t < tlast + 8000:
            x, v = self._advance(segs[-1][0], segs[-1][1], segs[-1][2], segs[-1][3], t)
            if abs(x - self.rest) < thr and abs(v) * 0.02 < thr:
                if ok_since is None:
                    ok_since = t
                if t - ok_since >= 40:
                    return ok_since
            else:
                ok_since = None
            t += STEP_MS
        raise RuntimeError('track does not settle')


def rdp(times, rows, tol, keep):
    """Ramer-Douglas-Peucker on a multi-dimensional series sampled at
    times. rows[i] is a tuple of values. tol per dimension. keep: set of
    indices that must be kept."""
    n = len(times)
    if n <= 2:
        return list(range(n))
    mark = [False] * n
    mark[0] = mark[-1] = True
    for k in keep:
        mark[k] = True
    anchors = [i for i in range(n) if mark[i]]
    stack = [(anchors[i], anchors[i + 1]) for i in range(len(anchors) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        ta, tb = times[a], times[b]
        worst, wi = 0.0, -1
        for i in range(a + 1, b):
            f = (times[i] - ta) / (tb - ta)
            err = 0.0
            for d in range(len(rows[i])):
                pred = rows[a][d] + (rows[b][d] - rows[a][d]) * f
                e = abs(rows[i][d] - pred) / tol[d]
                if e > err:
                    err = e
            if err > worst:
                worst, wi = err, i
        if worst > 1.0:
            mark[wi] = True
            stack.append((a, wi))
            stack.append((wi, b))
    return [i for i in range(n) if mark[i]]


class Clip:
    """Animated clip region. fn(vals) -> path data string in the 24 box,
    with a structure that never changes. drivers: list of Track ('p' kind).
    space: 'outer' = parent space (outside the part transform),
    'inner' = part local space (moves with the part)."""

    def __init__(self, fn, drivers, space='outer'):
        self.fn = fn
        self.drivers = drivers
        self.space = space


class Node:
    def __init__(self, name, subs=None, pivot=(12.0, 12.0)):
        self.name = name
        self.subs = subs or []
        self.pivot = pivot
        self.tx = Track(0.0, 't')
        self.ty = Track(0.0, 't')
        self.rot = Track(0.0, 'r')
        self.sx = Track(1.0, 's')
        self.sy = Track(1.0, 's')
        self.alpha = Track(1.0, 'a')
        self.children = []
        self.baked = []        # nodes whose subpaths live in this node's path
        self.clip = None
        self.gen = None        # procedural geometry: (fn(vals)->subs, drivers)
        self.hidden_rest = False
        # static axis (degrees) of the rotation/scale frame: scaleX/scaleY act
        # along this direction, so a diagonal arrow can squash and stretch
        # along its own length
        self.axis = 0.0

    # convenience -------------------------------------------------------
    def tracks(self):
        return [self.tx, self.ty, self.rot, self.sx, self.sy, self.alpha]

    def scale(self, t, s, spec=SPATIAL):
        self.sx.to(t, s, spec)
        self.sy.to(t, s, spec)
        return self

    def all_nodes(self):
        out = [self]
        for c in self.children:
            out += c.all_nodes()
        return out

    def all_tracks(self):
        tr = list(self.tracks())
        for b in self.baked:
            tr += b.tracks()
        if self.clip:
            tr += self.clip.drivers
        if self.gen:
            tr += self.gen[1]
        for c in self.children:
            tr += c.all_tracks()
        return tr

    def matrix(self, t):
        import geom
        return geom.mat_trs(self.tx.value(t), self.ty.value(t), self.rot.value(t),
                            self.sx.value(t), self.sy.value(t), self.pivot[0], self.pivot[1], self.axis)

    def path_subs(self, t):
        """Geometry of this node's own path at time t (local space)."""
        import geom
        if self.gen:
            fn, drv = self.gen
            return fn([d.value(t) for d in drv])
        subs = list(self.subs)
        for b in self.baked:
            subs += geom.transform_subs(b.subs, b.matrix(t))
        return subs

    def path_animated(self):
        return bool(self.gen) or any(any(tr.animated for tr in b.tracks()) for b in self.baked)

    def path_drivers(self):
        if self.gen:
            return self.gen[1]
        tr = []
        for b in self.baked:
            tr += [x for x in b.tracks() if x.animated]
        return tr


class Icon:
    def __init__(self, name, root, concept, parts, static_subs, fixes_note=None):
        self.name = name
        self.root = root
        self.concept = concept
        self.parts = parts
        self.static_subs = static_subs
        self.fixes_note = fixes_note

    def gesture_ms(self):
        if getattr(self, '_g', None) is None:
            trs = self.root.all_tracks()
            st = max([tr.settle_time() for tr in trs] + [0.0])
            self._g = int(math.ceil((st + 20) / 10.0) * 10)
            # the emitted files hold the exact rest value from the end on
            for tr in trs:
                tr.end = float(self._g)
        return self._g
