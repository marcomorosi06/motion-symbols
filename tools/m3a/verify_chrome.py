# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Development aid: renders the emitted SVG files in headless Chrome (real
# SMIL playback, seeked with setCurrentTime) and compares each frame with
# the motion model rendered by rsvg-convert. Needs Node, puppeteer and a
# Chrome binary (see shot.js).
# Usage: python3 verify_chrome.py NAME...

import io
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib     # noqa: E402
import render  # noqa: E402
import build   # noqa: E402,F401  (loads the specs)
from emit import Emitter  # noqa: E402

PX = 96
SHOT = os.path.join(HERE, 'shot.js')


def times_for(G, L):
    ts = [G * k / 8.0 for k in range(9)]
    loop_ts = [G * 0.33, G * 0.66, G + 300.0, L - 1.0]
    return ts, loop_ts


def run(names, tmp='/tmp/m3a_verify'):
    os.makedirs(tmp, exist_ok=True)
    cells = []
    for n in names:
        ic = lib.build_icon(n)
        em = Emitter(ic)
        G, L = em.G, em.L
        ts, lts = times_for(G, L)
        for variant, svg, tlist in (('once', em.svg(False), ts), ('loop', em.svg(True), lts)):
            for k, t in enumerate(tlist):
                uid = '%s-%s-%d' % (n, variant, k)
                s = svg.replace('m3a-%s-' % n, 'v-%s-' % uid)
                s = s.replace('<svg ', '<svg data-t="%s" ' % repr(t), 1)
                s = re.sub(r'width="24" height="24"', 'width="%d" height="%d"' % (PX, PX), s, count=1)
                tm = t if t <= G else G
                cells.append((n, variant, t, s, render.frame_svg_body(ic, tm, 'm' + uid.replace('_', ''))))
    cols = 10
    rows = (len(cells) + cols - 1) // cols
    html = ['<!doctype html><html><body style="margin:0;background:#fff">'
            '<div style="display:grid;grid-template-columns:repeat(%d,%dpx);gap:0">' % (cols, PX)]
    for c in cells:
        html.append('<div style="width:%dpx;height:%dpx;color:#000;line-height:0">%s</div>' % (PX, PX, c[3]))
    html.append('</div></body></html>')
    hp = os.path.join(tmp, 'page.html')
    with open(hp, 'w') as f:
        f.write(''.join(html))
    out = os.path.join(tmp, 'shot.png')
    subprocess.check_call(['node', SHOT, hp, out, str(cols * PX), str(rows * PX)])
    shot = np.asarray(Image.open(out).convert('L')).astype(int)
    bad = []
    worst = 0
    for i, c in enumerate(cells):
        r, q = divmod(i, cols)
        got = 255 - shot[r * PX:(r + 1) * PX, q * PX:(q + 1) * PX]
        doc = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 24 24">%s</svg>' % (PX, PX, c[4])
        p = subprocess.run(['rsvg-convert'], input=doc.encode(), capture_output=True, check=True)
        ref = np.asarray(Image.open(io.BytesIO(p.stdout)).convert('RGBA'))[:, :, 3].astype(int)
        d = np.abs(got - ref)
        score = d.mean()
        worst = max(worst, score)
        if score > 2.5:
            bad.append((c[0], c[1], round(c[2]), round(score, 2)))
    return bad, worst, len(cells)


if __name__ == '__main__':
    bad, worst, n = run(sys.argv[1:])
    for b in bad:
        print('MISMATCH', b)
    print('frames', n, 'mismatches', len(bad), 'worst mean diff %.2f' % worst)
