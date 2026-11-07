# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Renders still frames of the motion model (not of the emitted files) to
# static SVG, used for filmstrips, rest-frame checks and bounds checks.

import subprocess

import geom
from geom import fmt


def frame_svg_body(icon, t, uid='f'):
    defs = []
    cnt = [0]

    def clip(n, vals_t):
        c = n.clip
        d = c.fn([dr.value(vals_t) for dr in c.drivers])
        cid = '%s-c%d' % (uid, cnt[0])
        cnt[0] += 1
        defs.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d))
        return cid

    def node(n, alpha):
        a = alpha * max(0.0, min(1.0, n.alpha.value(t)))
        parts = []
        subs = n.path_subs(t)
        if subs:
            parts.append('<path d="%s" opacity="%s"/>' % (geom.to_d(subs), fmt(a)))
        for c in n.children:
            parts.append(node(c, a))
        body = ''.join(parts)
        if n.clip and n.clip.space == 'inner':
            body = '<g clip-path="url(#%s)">%s</g>' % (clip(n, t), body)
        m = n.matrix(t)
        body = '<g transform="matrix(%s)">%s</g>' % (' '.join(fmt(v, 5) for v in m), body)
        if n.clip and n.clip.space == 'outer':
            body = '<g clip-path="url(#%s)">%s</g>' % (clip(n, t), body)
        return body

    b = node(icon.root, 1.0)
    return '<defs>%s</defs>%s' % (''.join(defs), b)


def strip_svg(rows, size=48, label_w=170):
    """rows: list of (label, [svg bodies]) -> one SVG document."""
    ncol = max(len(r[1]) for r in rows)
    W = label_w + ncol * (size + 6)
    H = len(rows) * (size + 8)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><rect width="100%%" height="100%%" fill="#fff"/>' % (W, H)]
    for r, (label, bodies) in enumerate(rows):
        y = r * (size + 8) + 4
        out.append('<text x="4" y="%d" font-size="11" font-family="sans-serif">%s</text>' % (y + size // 2 + 4, label))
        for k, body in enumerate(bodies):
            x = label_w + k * (size + 6)
            out.append('<g transform="translate(%d %d) scale(%g)"><rect width="24" height="24" fill="#f3f3f3"/>'
                       '<g fill="#222">%s</g></g>' % (x, y, size / 24.0, body))
    out.append('</svg>')
    return ''.join(out)


def filmstrip(icons, path, n=14, size=48):
    rows = []
    for ic in icons:
        G = ic.gesture_ms()
        ts = [G * k / (n - 1) for k in range(n)]
        rows.append(('%s %dms' % (ic.name, G), [frame_svg_body(ic, t, '%s%d' % (ic.name, i)) for i, t in enumerate(ts)]))
    svg = strip_svg(rows, size)
    with open(path + '.svg', 'w') as f:
        f.write(svg)
    subprocess.check_call(['rsvg-convert', path + '.svg', '-o', path + '.png'])
