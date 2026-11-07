# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Structural validation of the generated files: well-formed XML, the fixed
# SVG rules (viewBox, currentColor, reduced-motion fallback, unique ids per
# icon and variant), and for AnimatedVectorDrawables: unique names, every
# target exists, keyframe fractions from 0 to 1 in increasing order, and
# path morphs with compatible commands in every keyframe.
# Usage: python3 validate.py NAME...

import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
A = '{http://schemas.android.com/apk/res/android}'


def sig(d):
    return re.sub(r'[-+0-9.eE ]+', ',', d)


def check_svg(path, name, variant):
    errs = []
    s = open(path).read()
    try:
        root = ET.fromstring(s)
    except ET.ParseError as e:
        return ['xml: %s' % e]
    if root.get('viewBox') != '0 0 24 24' or root.get('fill') != 'currentColor':
        errs.append('root attributes')
    if 'prefers-reduced-motion' not in s or 'm3a-static' not in s:
        errs.append('no reduced motion fallback')
    if not s.isascii():
        errs.append('non ascii')
    if re.search(r'<(?:path|g)[^>]* (?:fill|stroke|color)="', s):
        errs.append('color on a path')
    ids = re.findall(r' id="([^"]+)"', s)
    for i in ids:
        if not i.startswith('m3a-%s-%s-' % (name, variant)):
            errs.append('bad id ' + i)
    if len(ids) != len(set(ids)):
        errs.append('duplicate ids')
    for ref in re.findall(r'url\(#([^)]+)\)', s):
        if ref not in ids:
            errs.append('dangling ref ' + ref)
    for m in re.finditer(r'<animate attributeName="d"[^>]*values="([^"]+)"', s):
        vals = m.group(1).split(';')
        if len(set(sig(v) for v in vals)) != 1:
            errs.append('incompatible d morph')
    for m in re.finditer(r'keyTimes="([^"]+)"[^>]*values="([^"]+)"', s):
        kt = [float(x) for x in m.group(1).split(';')]
        if kt[0] != 0 or kt[-1] != 1 or any(b <= a for a, b in zip(kt, kt[1:])):
            errs.append('keyTimes order')
        if len(kt) != len(m.group(2).split(';')):
            errs.append('keyTimes/values count')
    return errs


def check_avd(path, loop):
    errs = []
    s = open(path).read()
    try:
        root = ET.fromstring(s)
    except ET.ParseError as e:
        return ['xml: %s' % e]
    if not s.isascii():
        errs.append('non ascii')
    names = {}
    for el in root.iter():
        n = el.get(A + 'name')
        if n and el.tag in ('group', 'path', 'clip-path'):
            if n in names:
                errs.append('duplicate name ' + n)
            names[n] = el
    vec = root.find('.//vector')
    if vec.get(A + 'tint') != '?attr/colorControlNormal':
        errs.append('tint')
    for p in root.iter('path'):
        if p.get(A + 'fillColor') != '@android:color/white':
            errs.append('fill color')
    for t in root.iter('target'):
        n = t.get(A + 'name')
        if n not in names:
            errs.append('target without element ' + n)
            continue
        el = names[n]
        for oa in t.iter('objectAnimator'):
            if oa.get(A + 'repeatCount') != ('-1' if loop else '0'):
                errs.append('repeatCount')
            for pvh in oa.iter('propertyValuesHolder'):
                prop = pvh.get(A + 'propertyName')
                ok = {'group': {'translateX', 'translateY', 'rotation', 'scaleX', 'scaleY'},
                      'path': {'fillAlpha', 'pathData'}, 'clip-path': {'pathData'}}[el.tag]
                if prop not in ok:
                    errs.append('property %s on %s' % (prop, el.tag))
                fr = [float(k.get(A + 'fraction')) for k in pvh.iter('keyframe')]
                if fr[0] != 0 or fr[-1] != 1 or any(b <= a for a, b in zip(fr, fr[1:])):
                    errs.append('fractions')
                if prop == 'pathData':
                    vals = [k.get(A + 'value') for k in pvh.iter('keyframe')] + [el.get(A + 'pathData')]
                    if len(set(sig(v) for v in vals)) != 1:
                        errs.append('incompatible pathData morph on ' + n)
    return errs


def main(names):
    bad = 0
    for n in names:
        errs = []
        for variant, d in (('loop', 'loop'), ('once', 'oneshot')):
            errs += ['svg %s: %s' % (d, e) for e in check_svg(os.path.join(ROOT, 'web', d, n + '.svg'), n, variant)]
            errs += ['avd %s: %s' % (d, e) for e in check_avd(
                os.path.join(ROOT, 'android', 'drawable', 'avd_%s_%s.xml' % (n, d)), d == 'loop')]
        if errs:
            bad += 1
            print(n, sorted(set(errs))[:6])
    print('validated', len(names), 'bad', bad)


if __name__ == '__main__':
    main(sys.argv[1:])
