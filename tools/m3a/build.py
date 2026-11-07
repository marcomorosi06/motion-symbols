# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Builds icons from their specs, checks them and writes the four output
# files per icon plus the manifest entry.
#
#   python3 build.py check NAME...         checks only
#   python3 build.py strip OUT NAME...     filmstrip PNG of the motion model
#   python3 build.py write FIRST LAST      build manifest indexes FIRST..LAST
#
# Checks: every frame inside the 24 box, first and last frame equal to the
# untouched icon (raster comparison), unique part names.

import datetime
import glob
import importlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)

import geom    # noqa: E402
import lib     # noqa: E402
import render  # noqa: E402
from emit import Emitter  # noqa: E402

GENERATOR = '0.12.0'

for f in sorted(glob.glob(os.path.join(HERE, 'specs_*.py'))):
    importlib.import_module(os.path.basename(f)[:-3])


def _png(svg_doc, px=96):
    p = subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px)], input=svg_doc.encode(), capture_output=True,
                       check=True)
    from PIL import Image
    import numpy as np
    im = Image.open(io.BytesIO(p.stdout)).convert('RGBA')
    return np.asarray(im)[:, :, 3].astype(int)


def _doc(body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">%s</svg>' % body


def check_rest(ic):
    G = ic.gesture_ms()
    ref = _png(_doc('<path d="%s"/>' % geom.to_d(ic.static_subs)))
    errs = []
    for t in (0.0, float(G)):
        img = _png(_doc(render.frame_svg_body(ic, t, 'r')))
        diff = abs(img - ref)
        if diff.max() > 40 or diff.mean() > 0.05:
            errs.append('rest frame differs at t=%d (max %d, mean %.3f)' % (t, diff.max(), diff.mean()))
    return errs


def _chain_bbox(ic, t):
    """World bbox of each drawn node at time t, restricted by its clips.
    Plain clips intersect the bbox; complement clips (a big rectangle with
    holes) drop the outline points that fall inside their holes."""
    out = []

    def clip_info(n, m):
        d = n.clip.fn([dr.value(t) for dr in n.clip.drivers])
        subs = geom.parse(d, rescale=False)
        polys = [[geom.apply_pt(m, p) for p in geom.flatten(sp)] for sp in subs]
        if not polys or len(polys[0]) < 3 or abs(geom.area(polys[0])) < 1e-9:
            return ('empty', None)
        bb = geom.bbox(polys[0])
        if bb[2] - bb[0] > 60:
            holes = [p for p in polys[1:] if len(p) >= 3 and abs(geom.area(p)) > 1e-9]
            return ('holes', holes)
        return ('box', bb)

    def walk(n, m_parent, cb, holes):
        if n.clip and n.clip.space == 'outer':
            kind, v = clip_info(n, m_parent)
            if kind == 'empty':
                return
            if kind == 'box':
                cb = _isect(cb, v)
            else:
                holes = holes + v
        m = geom.mat_mul(m_parent, n.matrix(t))
        if n.clip and n.clip.space == 'inner':
            kind, v = clip_info(n, m)
            if kind == 'empty':
                return
            if kind == 'box':
                cb = _isect(cb, v)
            else:
                holes = holes + v
        subs = n.path_subs(t)
        if subs and n.alpha.value(t) > 0.001:
            pts = [geom.apply_pt(m, p) for sp in subs for p in geom.flatten(sp, 4)]
            if holes:
                pts = [p for p in pts if not any(geom.pip(p, h) for h in holes)]
            if pts:
                bb = _isect(geom.bbox(pts), cb)
                if bb:
                    out.append((n.name, bb))
        for c in n.children:
            walk(c, m, cb, holes)

    walk(ic.root, geom.IDENT, (-1e9, -1e9, 1e9, 1e9), [])
    return out


def _isect(a, b):
    if a is None or b is None:
        return None
    r = (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))
    if r[0] >= r[2] or r[1] >= r[3]:
        return None
    return r


def check_bounds(ic, eps=0.02):
    G = ic.gesture_ms()
    errs = []
    t = 0.0
    worst = {}
    while t <= G:
        for name, bb in _chain_bbox(ic, t):
            over = max(-bb[0], -bb[1], bb[2] - 24, bb[3] - 24)
            if over > eps and over > worst.get(name, (0,))[0]:
                worst[name] = (over, t)
        t += 4.0
    for name, (over, t) in worst.items():
        errs.append('part %s leaves the box by %.3f at %dms' % (name, over, t))
    return errs


def check(ic):
    errs = check_bounds(ic) + check_rest(ic)
    G = ic.gesture_ms()
    if G > 1600:
        errs.append('gesture too long: %d' % G)
    return errs


def main():
    cmd = sys.argv[1]
    if cmd == 'check':
        bad = 0
        for n in sys.argv[2:]:
            try:
                ic = lib.build_icon(n)
                e = check(ic)
            except Exception as ex:
                e = ['ERROR %r' % ex]
            if e:
                bad += 1
                print(n, e)
        print('checked', len(sys.argv) - 2, 'bad', bad)
    elif cmd == 'strip':
        out = sys.argv[2]
        render.filmstrip([lib.build_icon(n) for n in sys.argv[3:]], out)
    elif cmd == 'write':
        first, last = int(sys.argv[2]), int(sys.argv[3])
        mpath = os.path.join(ROOT, 'manifest.json')
        with open(mpath) as f:
            m = json.load(f)
        today = os.environ.get('M3A_DATE', datetime.date.today().isoformat())
        bad = []
        for e in m['icons']:
            if not (first <= e['index'] <= last):
                continue
            ic = lib.build_icon(e['name'])
            errs = check(ic)
            if errs:
                bad.append((e['name'], errs))
                continue
            em = Emitter(ic)
            files = {
                'web_loop': 'web/loop/%s.svg' % ic.name,
                'web_oneshot': 'web/oneshot/%s.svg' % ic.name,
                'android_loop': 'android/drawable/avd_%s_loop.xml' % ic.name,
                'android_oneshot': 'android/drawable/avd_%s_oneshot.xml' % ic.name,
            }
            outs = {'web_loop': em.svg(True), 'web_oneshot': em.svg(False),
                    'android_loop': em.avd(True), 'android_oneshot': em.avd(False)}
            for k, rel in files.items():
                with open(os.path.join(ROOT, rel), 'w') as f:
                    f.write(outs[k])
            idx = e['index']
            e.clear()
            e.update({
                'name': ic.name,
                'index': idx,
                'status': 'done',
                'chunk': 11 + (idx - 621) // 100,
                'concept': ic.concept,
                'parts': ic.parts,
                'loop_ms': em.L,
                'gesture_ms': em.G,
                'files': files,
                'generator': GENERATOR,
                'date': today,
            })
            print('wrote', idx, ic.name, em.G)
        m['completed'] = sum(1 for e in m['icons'] if e['status'] == 'done')
        with open(mpath, 'w') as f:
            json.dump(m, f, indent=1, ensure_ascii=True)
            f.write('\n')
        for n, errs in bad:
            print('FAILED', n, errs)
        print('completed', m['completed'])


if __name__ == '__main__':
    main()
