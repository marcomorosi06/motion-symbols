# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Emitters: animated SVG (SMIL) and Android AnimatedVectorDrawable, both in
# a loop and a one-shot variant, from the same sampled motion model.

import geom
from anim import STEP_MS, HOLD_MS, rdp
from geom import fmt

TOL = {'t': 0.003, 'r': 0.04, 's': 0.0005, 'a': 0.004, 'p': 0.0008}

STYLE = ('<style>.m3a-static{display:none}@media (prefers-reduced-motion: reduce)'
         '{.m3a-anim{display:none}.m3a-static{display:inline}}</style>')


def attribution(icon):
    s = (icon.name + ': Derived from Material Symbols (Rounded) by Google, Apache License 2.0. '
         'Modified: geometry rescaled to 24x24 and split into animated parts.')
    if icon.fixes_note:
        s += ' ' + icon.fixes_note
    return s


class Sampler:
    def __init__(self, icon):
        self.icon = icon
        self.G = icon.gesture_ms()
        ts = set()
        t = 0.0
        while t < self.G:
            ts.add(round(t, 3))
            t += STEP_MS
        ts.add(float(self.G))
        self.snaps = set()
        for tr in icon.root.all_tracks():
            for s in tr.snap_times():
                if 0 < s < self.G:
                    ts.add(s - 1.0)
                    ts.add(s)
                    self.snaps.add(s - 1.0)
                    self.snaps.add(s)
        self.times = sorted(ts)

    def series(self, tracks, value_fn=None):
        """Reduce a group of tracks to keyframes. Returns list of (t, row)."""
        times = self.times
        rows = []
        for i, t in enumerate(times):
            if i == len(times) - 1:
                rows.append(tuple(tr.rest for tr in tracks))
            else:
                rows.append(tuple(tr.value(t) for tr in tracks))
        tol = [TOL[tr.kind] for tr in tracks]
        keep = {i for i, t in enumerate(times) if t in self.snaps}
        idx = rdp(times, rows, tol, keep)
        return [(times[i], rows[i]) for i in idx]


def _frac(t, dur):
    return fmt(t / dur, 4)


def _keytimes(kf, dur, loop):
    ks = [_frac(t, dur) for t, _ in kf]
    if loop:
        ks.append('1')
    # guard against equal rounded neighbours
    out = []
    for k in ks:
        if out and float(k) <= float(out[-1]):
            raise RuntimeError('keyTimes collide')
        out.append(k)
    return ';'.join(out)


class Emitter:
    def __init__(self, icon):
        self.icon = icon
        self.S = Sampler(icon)
        self.G = self.S.G
        self.L = self.G + HOLD_MS
        self._kf = {}

    # ---------------------------------------------------------- helpers
    def kf(self, key, tracks):
        if key not in self._kf:
            self._kf[key] = self.S.series(tracks)
        return self._kf[key]

    def eff_alpha_tracks(self, chain):
        return [n.alpha for n in chain if n.alpha.animated]

    # ---------------------------------------------------------- SVG
    def svg(self, loop):
        ic = self.icon
        dur = self.L if loop else self.G
        rep = 'repeatCount="indefinite"' if loop else 'repeatCount="1" fill="freeze"'
        self._svg_defs = []
        self._svg_clip_n = 0
        variant = 'loop' if loop else 'once'

        def at(attr, typ, kf, fmtrow):
            vals = [fmtrow(r) for _, r in kf]
            if loop:
                vals.append(vals[0])
            t = ' type="%s"' % typ if typ else ''
            tag = 'animateTransform' if typ else 'animate'
            return ('<%s attributeName="%s"%s dur="%dms" %s calcMode="linear" keyTimes="%s" values="%s"/>'
                    % (tag, attr, t, dur, rep, _keytimes(kf, dur, loop), ';'.join(vals)))

        def clip_el(node):
            c = node.clip
            kf = self.kf(('clip', node.name), c.drivers)
            cid = 'm3a-%s-%s-c%d' % (ic.name, variant, self._svg_clip_n)
            self._svg_clip_n += 1
            d0 = c.fn([d.rest for d in c.drivers])
            if any(d.animated for d in c.drivers):
                vals = [c.fn(list(r)) for _, r in kf]
                if loop:
                    vals.append(vals[0])
                a = ('<animate attributeName="d" dur="%dms" %s calcMode="linear" keyTimes="%s" values="%s"/>'
                     % (dur, rep, _keytimes(kf, dur, loop), ';'.join(vals)))
                self._svg_defs.append('<clipPath id="%s"><path d="%s">%s</path></clipPath>' % (cid, d0, a))
            else:
                self._svg_defs.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d0))
            return cid

        def node_svg(n, chain):
            chain = chain + [n]
            inner = []
            # own path
            if n.subs or n.baked or n.gen:
                d0 = geom.to_d(n.path_subs(0.0)) if n.gen else geom.to_d(n.subs + [s for b in n.baked for s in b.subs])
                anims = []
                if n.path_animated():
                    drv = n.path_drivers()
                    kf = self.kf(('path', n.name), drv)
                    vals = [geom.to_d(n.path_subs(t)) for t, _ in kf]
                    vals[-1] = d0 if not n.gen else geom.to_d(n.path_subs(self.G + 10000))
                    if loop:
                        vals.append(vals[0])
                    anims.append('<animate attributeName="d" dur="%dms" %s calcMode="linear" keyTimes="%s" values="%s"/>'
                                 % (dur, rep, _keytimes(kf, dur, loop), ';'.join(vals)))
                al = self.eff_alpha_tracks(chain)
                op = ''
                if al:
                    kf = self.kf(('alpha', n.name), al)
                    prod = lambda r: fmt(max(0.0, min(1.0, _prod(r))), 4)
                    anims.append(at('opacity', None, kf, prod))
                    r0 = _prod([a.rest for a in al])
                    if r0 < 1:
                        op = ' opacity="%s"' % fmt(r0)
                if anims:
                    inner.append('<path d="%s"%s>%s</path>' % (d0, op, ''.join(anims)))
                else:
                    inner.append('<path d="%s"%s/>' % (d0, op))
            for c in n.children:
                inner.append(node_svg(c, chain))
            body = ''.join(inner)
            if n.clip and n.clip.space == 'inner':
                body = '<g clip-path="url(#%s)">%s</g>' % (clip_el(n), body)
            px, py = n.pivot
            rs = n.rot.animated or n.sx.animated or n.sy.animated
            if rs:
                body = '<g transform="translate(%s %s)">%s</g>' % (fmt(-px), fmt(-py), body)
                if n.axis:
                    body = '<g transform="rotate(%s)">%s</g>' % (fmt(-n.axis), body)
                if n.sy.animated and not _same(n.sx, n.sy):
                    kf = self.kf(('sy', n.name), [n.sy])
                    body = '<g>%s%s</g>' % (at('transform', 'scale', kf, lambda r: '1 ' + fmt(r[0])), body)
                if n.sx.animated:
                    if _same(n.sx, n.sy):
                        kf = self.kf(('sx', n.name), [n.sx])
                        body = '<g>%s%s</g>' % (at('transform', 'scale', kf, lambda r: fmt(r[0]) + ' ' + fmt(r[0])), body)
                    else:
                        kf = self.kf(('sx', n.name), [n.sx])
                        body = '<g>%s%s</g>' % (at('transform', 'scale', kf, lambda r: fmt(r[0]) + ' 1'), body)
                if n.rot.animated:
                    kf = self.kf(('rot', n.name), [n.rot])
                    body = '<g>%s%s</g>' % (at('transform', 'rotate', kf, lambda r: fmt(r[0])), body)
                if n.axis:
                    body = '<g transform="rotate(%s)">%s</g>' % (fmt(n.axis), body)
                body = '<g transform="translate(%s %s)">%s</g>' % (fmt(px), fmt(py), body)
            if n.tx.animated or n.ty.animated:
                kf = self.kf(('tr', n.name), [n.tx, n.ty])
                body = '<g>%s%s</g>' % (at('transform', 'translate', kf, lambda r: fmt(r[0]) + ' ' + fmt(r[1])), body)
            if n.clip and n.clip.space == 'outer':
                body = '<g clip-path="url(#%s)">%s</g>' % (clip_el(n), body)
            return body

        body = node_svg(ic.root, [])
        defs = '<defs>%s</defs>' % ''.join(self._svg_defs) if self._svg_defs else ''
        static = '<path d="%s"/>' % geom.to_d(ic.static_subs)
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">'
                '<!-- %s -->%s<g class="m3a-anim">%s%s</g><g class="m3a-static">%s</g></svg>\n'
                % (attribution(ic), STYLE, defs, body, static))

    # ---------------------------------------------------------- Android
    def avd(self, loop):
        ic = self.icon
        dur = self.L if loop else self.G
        targets = []

        def frac(t):
            return fmt(t / dur, 4)

        def pvh(prop, kf, fmtv, vtype='floatType', restv=None):
            ks = []
            last = -1
            for t, r in kf:
                f = frac(t)
                if float(f) <= last:
                    raise RuntimeError('fraction collide')
                last = float(f)
                ks.append('<keyframe android:fraction="%s" android:value="%s"/>' % (f, fmtv(r)))
            if loop:
                ks.append('<keyframe android:fraction="1" android:value="%s"/>' % fmtv(kf[0][1]))
            return ('<propertyValuesHolder android:propertyName="%s" android:valueType="%s">%s</propertyValuesHolder>'
                    % (prop, vtype, ''.join(ks)))

        def target(name, holders):
            targets.append('<target android:name="%s"><aapt:attr name="android:animation"><objectAnimator '
                           'android:duration="%d" android:repeatCount="%s" android:interpolator="@android:anim/linear_interpolator">'
                           '%s</objectAnimator></aapt:attr></target>' % (name, dur, '-1' if loop else '0', ''.join(holders)))

        f1 = lambda r: fmt(r[0])

        def clip_xml(n):
            c = n.clip
            d0 = c.fn([d.rest for d in c.drivers])
            if any(d.animated for d in c.drivers):
                kf = self.kf(('clip', n.name), c.drivers)
                vals = [c.fn(list(r)) for _, r in kf]
                kf2 = [(t, v) for (t, _), v in zip(kf, vals)]
                target('c_' + n.name, [pvh('pathData', kf2, lambda v: v, 'pathType')])
            return '<clip-path android:name="c_%s" android:pathData="%s"/>' % (n.name, d0)

        def node_xml(n, chain):
            chain = chain + [n]
            inner = []
            if n.clip and n.clip.space == 'inner':
                inner.append(clip_xml(n))
            if n.subs or n.baked or n.gen:
                d0 = geom.to_d(n.path_subs(0.0)) if n.gen else geom.to_d(n.subs + [s for b in n.baked for s in b.subs])
                holders = []
                al = self.eff_alpha_tracks(chain)
                fa = ''
                if al:
                    kf = self.kf(('alpha', n.name), al)
                    holders.append(pvh('fillAlpha', kf, lambda r: fmt(max(0.0, min(1.0, _prod(r))))))
                    r0 = _prod([a.rest for a in al])
                    if r0 < 1:
                        fa = ' android:fillAlpha="%s"' % fmt(r0)
                if n.path_animated():
                    kf = self.kf(('path', n.name), n.path_drivers())
                    vals = [geom.to_d(n.path_subs(t)) for t, _ in kf]
                    vals[-1] = d0 if not n.gen else geom.to_d(n.path_subs(self.G + 10000))
                    kf2 = [(t, v) for (t, _), v in zip(kf, vals)]
                    holders.append(pvh('pathData', kf2, lambda v: v, 'pathType'))
                if holders:
                    target('p_' + n.name, holders)
                inner.append('<path android:name="p_%s" android:fillColor="@android:color/white"%s android:pathData="%s"/>'
                             % (n.name, fa, d0))
            for c in n.children:
                inner.append(node_xml(c, chain))
            th = []
            if n.tx.animated:
                th.append(pvh('translateX', self.kf(('tx1', n.name), [n.tx]), f1))
            if n.ty.animated:
                th.append(pvh('translateY', self.kf(('ty1', n.name), [n.ty]), f1))
            rh = []
            if n.rot.animated:
                rh.append(pvh('rotation', self.kf(('rot', n.name), [n.rot]), f1))
            if n.sx.animated:
                rh.append(pvh('scaleX', self.kf(('sx', n.name), [n.sx]), f1))
            if n.sy.animated:
                rh.append(pvh('scaleY', self.kf(('sy1', n.name), [n.sy]), f1))
            pv = (fmt(n.pivot[0]), fmt(n.pivot[1]))
            if n.axis and rh:
                # outer: translation and the axis; middle: animated rotation
                # and scale; inner: back from the axis
                if th:
                    target('g_' + n.name, th)
                target('s_' + n.name, rh)
                g = ('<group android:name="g_%s" android:pivotX="%s" android:pivotY="%s" android:rotation="%s">'
                     '<group android:name="s_%s" android:pivotX="%s" android:pivotY="%s">'
                     '<group android:name="a_%s" android:pivotX="%s" android:pivotY="%s" android:rotation="%s">'
                     '%s</group></group></group>'
                     % (n.name, pv[0], pv[1], fmt(n.axis), n.name, pv[0], pv[1], n.name, pv[0], pv[1],
                        fmt(-n.axis), ''.join(inner)))
            else:
                if th + rh:
                    target('g_' + n.name, th + rh)
                g = ('<group android:name="g_%s" android:pivotX="%s" android:pivotY="%s">%s</group>'
                     % (n.name, pv[0], pv[1], ''.join(inner)))
            if n.clip and n.clip.space == 'outer':
                g = '<group android:name="w_%s">%s%s</group>' % (n.name, clip_xml(n), g)
            return g

        body = node_xml(ic.root, [])
        return ('<?xml version="1.0" encoding="utf-8"?>\n<!-- %s -->\n'
                '<animated-vector xmlns:android="http://schemas.android.com/apk/res/android" '
                'xmlns:aapt="http://schemas.android.com/aapt"><aapt:attr name="android:drawable">'
                '<vector android:width="24dp" android:height="24dp" android:viewportWidth="24" '
                'android:viewportHeight="24" android:tint="?attr/colorControlNormal">%s</vector></aapt:attr>%s'
                '</animated-vector>\n' % (attribution(ic), body, ''.join(targets)))


def _prod(r):
    p = 1.0
    for v in r:
        p *= v
    return p


def _same(a, b):
    return a.ev == b.ev and a.rest == b.rest
