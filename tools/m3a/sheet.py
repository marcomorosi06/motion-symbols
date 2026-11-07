# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Development aid: contact sheets of source icons with their islands
# numbered, rendered to PNG with rsvg-convert.
# Usage: python3 sheet.py OUT_PREFIX NAME [NAME ...]

import subprocess
import sys

import geom
import lib

COLORS = ['#d32f2f', '#1976d2', '#388e3c', '#f57c00', '#7b1fa2', '#0097a7', '#c2185b', '#5d4037',
          '#455a64', '#afb42b', '#512da8', '#00796b']


def cell(name, x, y, size):
    subs, isl = lib.load(name)
    k = size / 24.0
    out = ['<g transform="translate(%g %g) scale(%g)">' % (x, y, k),
           '<rect x="0" y="0" width="24" height="24" fill="#fff" stroke="#ccc" stroke-width="0.05"/>']
    for I in isl:
        d = geom.to_d([subs[s] for s in I.sub_ids])
        out.append('<path d="%s" fill="%s" fill-opacity="0.85"/>' % (d, COLORS[I.idx % len(COLORS)]))
    for I in isl:
        cx, cy = I.center
        out.append('<text x="%g" y="%g" font-size="1.6" font-family="sans-serif" fill="#000" stroke="#fff" '
                   'stroke-width="0.25" paint-order="stroke" text-anchor="middle">%d%s</text>'
                   % (cx, cy + 0.5, I.idx, ('h%d' % len(I.holes)) if I.holes else ''))
    out.append('</g>')
    out.append('<text x="%g" y="%g" font-size="11" font-family="sans-serif" text-anchor="middle">%s</text>'
               % (x + size / 2, y + size + 13, name[:24]))
    return ''.join(out)


def sheet(prefix, names, cols=8, size=150):
    rows = (len(names) + cols - 1) // cols
    W = cols * (size + 20)
    H = rows * (size + 30)
    body = [cell(n, 10 + (i % cols) * (size + 20), 5 + (i // cols) * (size + 30), size) for i, n in enumerate(names)]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><rect width="100%%" height="100%%" fill="#eee"/>%s</svg>'
           % (W, H, ''.join(body)))
    with open(prefix + '.svg', 'w') as f:
        f.write(svg)
    subprocess.check_call(['rsvg-convert', prefix + '.svg', '-o', prefix + '.png'])


if __name__ == '__main__':
    sheet(sys.argv[1], sys.argv[2:])
