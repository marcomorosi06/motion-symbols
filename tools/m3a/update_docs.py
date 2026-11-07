# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Rebuilds the icon grid and the embedded icon store of preview.html and the
# progress lines of preview.html and README.md from manifest.json and the
# files in web/. Run after build.py write.

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


def main():
    with open(os.path.join(ROOT, 'manifest.json')) as f:
        m = json.load(f)
    done = sorted((e for e in m['icons'] if e['status'] == 'done'), key=lambda e: e['index'])
    total = m['total']
    n = len(done)
    pct = '%.1f' % (100.0 * n / total)

    cards = []
    store = []
    for e in done:
        cards.append(
            '<div class="card" data-name="{n}" data-index="{i}" tabindex="0" role="button" '
            'aria-label="Icon {i}, {n}, replay animation"><div class="icons" aria-hidden="true">'
            '<span class="slot loop"></span><span class="slot once"></span></div>'
            '<div class="name"><span class="num">{i}</span>{n}</div>'
            '<div class="timing">{g} ms / loop {l} ms</div></div>'.format(n=e['name'], i=e['index'],
                                                                          g=e['gesture_ms'], l=e['loop_ms']))
        with open(os.path.join(ROOT, e['files']['web_loop'])) as f:
            lp = f.read().strip()
        with open(os.path.join(ROOT, e['files']['web_oneshot'])) as f:
            on = f.read().strip()
        store.append('<template data-for="%s">%s%s</template>' % (e['name'], lp, on))

    path = os.path.join(ROOT, 'preview.html')
    with open(path) as f:
        s = f.read()
    a = s.index('<div class="grid" id="grid">\n') + len('<div class="grid" id="grid">\n')
    b = s.index('\n</div>\n<div class="empty-state"', a)
    s = s[:a] + '\n'.join(cards) + s[b:]
    a = s.index('<div id="store" hidden>\n') + len('<div id="store" hidden>\n')
    b = s.index('\n</div>\n\n<script>', a)
    s = s[:a] + '\n'.join(store) + s[b:]
    s = re.sub(r'<span id="count">[^<]*</span>',
               '<span id="count">%d / %s (%s%%)</span>' % (n, '{:,}'.format(total), pct), s, count=1)
    s = re.sub(r'id="progress-fill" style="width:[^"]*"', 'id="progress-fill" style="width:%s%%"' % pct, s, count=1)
    with open(path, 'w') as f:
        f.write(s)

    rpath = os.path.join(ROOT, 'README.md')
    with open(rpath) as f:
        r = f.read()
    r = re.sub(r'\*\*\d+ / [\d,]+ icons completed\*\* \xb7 [\d.]+%',
               '**%d / %s icons completed** \xb7 %s%%' % (n, '{:,}'.format(total), pct), r, count=1)
    with open(rpath, 'w') as f:
        f.write(r)
    print('preview and README updated:', n, total, pct)


if __name__ == '__main__':
    main()
