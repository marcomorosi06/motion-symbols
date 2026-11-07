# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 1005-1020 (data_exploration .. deblur).

from lib import *  # noqa: F401,F403


@spec('data_info_alert')
def _(b):
    for k, i in enumerate([2, 3, 0]):
        redraw(b, b.part('row%d' % k, b.I(i)), k * 70, 0)
    badge = b.part('badge', b.I(1))
    pop(badge, 160, 0.3)
    lift(badge, 280, -0.6, hold=90)
    return "The rows are written again one after another and the info badge pops in and nods."


@spec('data_loss_prevention')
def _(b):
    lens = b.part('lens', b.I(2), pivot=(11.0, 10.0))
    head = b.part('head', b.I(0), pivot='b', parent=lens)
    body = b.part('body', b.I(1), pivot='b', parent=lens)
    press(lens, 0, 0.94)
    nod(lens, 0, -8, hold=120)
    hop(head, 80, 0.5, stretch=1.03)
    squash(body, 80, 0.06)
    return "The magnifier tilts over the person it protects, who stands firm."


@spec('data_object')
def _(b):
    r = b.part('right', b.I(0))
    l = b.part('left', b.I(1))
    dart(l, 0, -0.9, 0)
    dart(r, 0, 0.9, 0)
    return "The curly braces wind in and push outward, then spring back."


def _arc_redraw(b, arc, t=0):
    clip, p = clip_sweep(12.0, 12.2, 12.0, 1.0, 117.0, n=40)
    arc.clip = clip
    p.to(t, 0.0, EFFECTS)
    p.to(t + 170, 1.0, SPATIAL_SLOW)


@spec('data_usage')
def _(b):
    big = b.part('arc_big', b.I(0))
    small = b.part('arc_used', b.I(1))
    press(big, 0, 0.96)
    _arc_redraw(b, small, 0)
    return "The used arc empties and is drawn again clockwise, as the usage refills."


@spec('data_saver_on')
def _(b):
    big = b.part('arc_big', b.I(0))
    small = b.part('arc_used', b.I(1))
    p = b.part('plus', b.I(2))
    press(big, 0, 0.96)
    _arc_redraw(b, small, 0)
    plus_badge(p, 120)
    return "The used arc is drawn again clockwise and the plus in the middle contracts and springs back."


@spec('data_table')
def _(b):
    t = b.part('table', b.I(0))
    dots = [b.part('d%d' % k, b.I(i), parent=t) for k, i in enumerate([1, 2, 3])]
    press(t, 0, 0.96)
    stagger(dots, 40, 70, pop, low=0.0)
    return "The table gives and its row markers pop in one after another."


@spec('dataset')
def _(b):
    f = b.part('frame', b.I(4))
    cells = [b.part('c%d' % k, b.I(i), parent=f) for k, i in enumerate([2, 3, 0, 1])]
    press(f, 0, 0.97)
    stagger(cells, 40, 60, pop, low=0.3)
    return "The frame gives and the four data cells pop one after another."


@spec('dataset_linked')
def _(b):
    f = b.part('frame', b.I(0))
    cells = [b.part('c%d' % k, b.I(i)) for k, i in enumerate([2, 4, 1])]
    l = b.part('link_l', b.I(3))
    m = b.part('link_mid', b.I(5))
    r = b.part('link_r', b.I(6))
    press(f, 0, 0.98)
    stagger(cells, 0, 60, pop, low=0.3)
    shift(l, 120, dx=0.4, hold=80)
    shift(r, 120, dx=-0.4, hold=80, spec_out=SPATIAL)
    pressxy(m, 120, 0.7, 1, hold=80)
    return "The data cells pop in turn and the chain links tug together and snap back."


@spec('date_range')
def _(b):
    c = b.part('calendar', b.I(3), pivot='t')
    dots = [b.part('d%d' % k, b.I(i), parent=c) for k, i in enumerate([0, 1, 2])]
    c.sy.to(0, 0.86, SPATIAL)
    c.sx.to(0, 1.03, SPATIAL)
    c.sy.back(110, BOUNCY)
    c.sx.back(110, BOUNCY)
    stagger(dots, 100, 60, pop, low=0.2)
    return "The calendar page flips and the days of the range pop in one after another."


@spec('deblur')
def _(b):
    half = b.part('half', b.I(12))
    cols = [[3, 5], [4, 2, 0, 1], [7, 8, 10, 9, 11, 6]]
    k = 0
    for c, ids in enumerate(cols):
        for i in ids:
            n = b.part('dot%d' % k, b.I(i))
            pop(n, c * 70, 0.0, dt=70)
            k += 1
    press(half, 230, 0.93)
    return "The blur dots pop into focus column by column, toward the sharp half."
