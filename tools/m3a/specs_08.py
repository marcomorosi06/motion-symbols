# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 957-1004 (crib .. data_check).

from lib import *  # noqa: F401,F403


@spec('crib')
def _(b):
    c = b.part('crib', b.I(0), pivot=(12.0, 22.0))
    rock(c, 0, 4, 3, 170, SPATIAL_SLOW)
    return "The crib rocks gently from side to side and comes to rest."


@spec('crisis_alert')
def _(b):
    outer = b.part('outer', b.I(0), pivot=(12.0, 12.6))
    inner = b.part('inner', b.I(1), pivot=(12.0, 12.6))
    dot = b.part('dot', b.I(3))
    mark = b.part('alert', b.I(2), pivot='b')
    pop(dot, 0, 0.2)
    press(inner, 50, 0.85, hold=60)
    press(outer, 110, 0.92, hold=60)
    mark.rot.kick(60, 600.0, BOUNCY)
    return "The target pulses outward from its center and the alert mark above it shakes."


def _ratio(b, sx, sy, label):
    f = b.part('frame', b.I(0))
    pressxy(f, 0, sx, sy, hold=110, spec_out=BOUNCY)
    return "The crop frame squeezes and snaps back out to its %s shape." % label


@spec('crop_16_9')
def _(b):
    return _ratio(b, 0.8, 1, '16:9')


@spec('crop_21_9')
def _(b):
    return _ratio(b, 0.8, 1, '21:9')


@spec('crop_3_2')
def _(b):
    return _ratio(b, 0.82, 1, '3:2')


@spec('crop_5_4')
def _(b):
    return _ratio(b, 0.85, 1, '5:4')


@spec('crop_7_5')
def _(b):
    return _ratio(b, 0.84, 1, '7:5')


@spec('crop_landscape')
def _(b):
    return _ratio(b, 0.82, 1, 'landscape')


@spec('crop_2_3')
def _(b):
    return _ratio(b, 1, 0.82, '2:3')


@spec('crop_9_16')
def _(b):
    return _ratio(b, 1, 0.8, '9:16')


@spec('crop_portrait')
def _(b):
    return _ratio(b, 1, 0.82, 'portrait')


@spec('crop_square')
def _(b):
    return _ratio(b, 0.85, 0.85, 'square')


@spec('crop_free')
def _(b):
    dirs = {0: (0.8, -0.8), 1: (-0.8, -0.8), 2: (0.8, 0.8), 3: (-0.8, 0.8)}
    for k, (i, (dx, dy)) in enumerate(sorted(dirs.items())):
        n = b.part('corner%d' % i, b.I(i))
        shift(n, k * 40, dx=dx, dy=dy, hold=100, spec_out=SPATIAL_FAST)
    return "The four corners close in one after another and spring back out: a free crop."


@spec('crop_rotate')
def _(b):
    big = b.part('frame_big', b.I(1))
    small = b.part('frame_small', b.I(2))
    a0 = b.part('a0', b.I(0))
    a1 = b.part('a1', b.I(3))
    arrows = b.group('arrows', [a0, a1], pivot=(12.0, 12.0))
    spin(arrows, 0, 180, SPATIAL)
    press(arrows, 0, 0.9, hold=200, spec_out=SPATIAL)
    shift(big, 60, dx=-0.5, dy=0.5, hold=110)
    shift(small, 60, dx=0.5, dy=-0.5, hold=110)
    return "The arrows swing a half turn around the crop, whose corners slide together and back."


@spec('crossword')
def _(b):
    g = b.part('grid', b.I(0))
    order = [4, 1, 2, 3, 0]
    cells = [b.hole('cell%d' % k, g, b.isl[0], i) for k, i in enumerate(order)]
    for k, c in enumerate(cells):
        pop(c, k * 60, 0.0, dt=80, spec_out=SPATIAL_FAST)
    return "The empty squares fill in one after another and clear again, like answers being tried."


@spec('crowdsource')
def _(b):
    body = b.part('body', b.I(4), pivot='b')
    lh = b.part('hand_l', b.I(5), pivot='br')
    rh = b.part('hand_r', b.I(6), pivot='bl')
    dots = [b.part('d%d' % k, b.I(i)) for k, i in enumerate([1, 3, 0, 2])]
    nod(lh, 0, 10, hold=110)
    nod(rh, 0, -10, hold=110)
    squash(body, 0, 0.05)
    stagger(dots, 60, 50, pop, low=0.2)
    return "The hands open upward and the ideas pop above them one after another."


@spec('crown')
def _(b):
    c = b.part('crown', b.I(1), pivot='b')
    base = b.part('base', b.I(0), pivot='b')
    hop(c, 0, 0.9, stretch=1.03)
    squash(base, 300, 0.25)
    return "The crown hops and lands back on its band with a squash."


@spec('css')
def _(b):
    ls = [b.part('l%d' % k, b.I(i), pivot='b') for k, i in enumerate([2, 0, 1])]
    stagger(ls, 0, 80, hop, h=0.9, stretch=1.03)
    return "The letters hop one after another, like reading C-S-S."


@spec('csv')
def _(b):
    f = b.part('frame', b.I(3))
    ls = [b.part('l%d' % k, b.I(i), pivot='b', parent=f) for k, i in enumerate([0, 1, 2])]
    press(f, 0, 0.97)
    stagger(ls, 40, 80, hop, h=0.8, stretch=1.03)
    return "The file gives and its letters hop one after another, like reading C-S-V."


def coin(n, t=0, lift_=True):
    n.sx.to(t, -1.0, SPATIAL)
    n.sx.to(t + 200, 1.0, SPATIAL)
    if lift_:
        n.ty.to(t, -0.6, SPATIAL)
        n.ty.back(t + 200, BOUNCY)
    return t + 600


for _n in ['currency_bitcoin', 'currency_lira', 'currency_pound', 'currency_ruble',
           'currency_rupee', 'currency_yen', 'currency_yuan']:
    def _mk(name):
        @spec(name)
        def _(b):
            c = b.part('symbol', b.I(0))
            coin(c)
            return "The symbol flips around like a tossed coin and lands back face up."
    _mk(_n)


@spec('currency_rupee_circle')
def _(b):
    ring_ = b.part('ring', b.I(1))
    c = b.part('symbol', b.I(0), parent=ring_)
    press(ring_, 0, 0.95)
    coin(c, 0, False)
    return "The ring gives and the symbol inside flips around like a coin."


@spec('currency_exchange')
def _(b):
    bot = b.part('arrow_bottom', b.I(1))
    top = b.part('arrow_top', b.I(2))
    arrows = b.group('arrows', [bot, top], pivot=(12.0, 12.0))
    sym = b.part('symbol', b.I(0))
    press(arrows, 0, 0.7, hold=260, spec_in=SPATIAL_FAST, spec_out=SPATIAL)
    spin(arrows, 60, 180, SPATIAL)
    coin(sym, 40, False)
    return "The arrows swing a half turn around the money, which flips like a coin: exchanged."


@spec('curtains')
def _(b):
    c = b.part('curtains', b.I(0), pivot='t')
    rock(c, 0, 2, 3, 140, SPATIAL_SLOW)
    pressxy(c, 0, 1.0, 0.97, hold=160, spec_out=SPATIAL)
    return "The curtains sway on their rod in a draught and settle."


@spec('cycle')
def _(b):
    arrows = [b.part('a%d' % k, b.I(i)) for k, i in enumerate([0, 1, 2])]
    g = b.group('cycle', arrows, pivot=(12.0, 12.0))
    spin(g, 0, 360, SPATIAL_SLOW)
    press(g, 0, 0.88, hold=280, spec_out=SPATIAL)
    return "The three arrows chase each other around a full turn."


@spec('cyclone')
def _(b):
    eye = b.part('eye', b.I(0))
    arms = b.part('arms', b.I(1))
    spin(arms, 0, 360, SPATIAL_SLOW)
    press(arms, 0, 0.9, hold=280, spec_out=SPATIAL)
    press(eye, 60, 0.8)
    return "The cyclone whirls a full turn around its eye."


@spec('dangerous')
def _(b):
    o = b.part('octagon', b.I(0))
    x = b.part('x', b.I(1))
    spin(o, 0, 45, SPATIAL)
    rock(x, 120, 14, 3, 90)
    return "The sign turns an eighth and lands on itself, and the x inside shakes its head."


@spec('dark_mode')
def _(b):
    m = b.part('moon', b.I(0))
    rock(m, 0, 10, 3, 170, SPATIAL_SLOW)
    return "The moon rocks gently, like a cradle."


def _tiles(b, order, t0=0, dt=60):
    ns = [b.part('tile%d' % k, b.I(i)) for k, i in enumerate(order)]
    stagger(ns, t0, dt, pop, low=0.4)
    return ns


@spec('dashboard')
def _(b):
    _tiles(b, [1, 0, 3, 2])
    return "The dashboard tiles pop in one after another."


@spec('dashboard_2')
def _(b):
    _tiles(b, [3, 1, 2, 0])
    return "The dashboard tiles pop in one after another."


@spec('dashboard_2_add')
def _(b):
    _tiles(b, [1, 0, 2])
    badge = b.part('badge', b.I(3))
    plus_badge(badge, 200, 0.75)
    return "The dashboard tiles pop in one after another and the add badge contracts and springs back."


@spec('dashboard_2_edit')
def _(b):
    _tiles(b, [3, 1, 2])
    pen = b.part('pen', b.I(0), pivot='bl')
    for k, (x, y) in enumerate([(-0.6, 0.3), (0.3, -0.2), (-0.4, 0.2)]):
        pen.tx.to(150 + k * 90, x, SPATIAL_FAST)
        pen.ty.to(150 + k * 90, y, SPATIAL_FAST)
    pen.tx.back(420, BOUNCY)
    pen.ty.back(420, BOUNCY)
    return "The dashboard tiles pop in one after another and the pen scribbles an edit."


@spec('dashboard_2_gear')
def _(b):
    _tiles(b, [2, 0, 1])
    g = b.part('gear', b.I(3), pivot=(18.0, 17.0))
    spin(g, 150, 60, SPATIAL)
    return "The dashboard tiles pop in one after another and the gear turns a sixth."


@spec('dashboard_customize')
def _(b):
    _tiles(b, [0, 1, 2])
    p = b.part('plus', b.I(3))
    plus_badge(p, 200)
    return "The tiles pop in one after another and the plus in the last slot contracts and springs back."


def _data_rows(b, ids, t0=0):
    for k, i in enumerate(ids):
        redraw(b, b.part('row%d' % k, b.I(i)), t0 + k * 70, 0)


@spec('data_alert')
def _(b):
    _data_rows(b, [2, 3, 0])
    alert_badge(b.part('badge', b.I(1)), 160)
    return "The rows are written again one after another and the alert badge pops and shakes."


@spec('data_check')
def _(b):
    _data_rows(b, [2, 3, 0])
    badge = b.part('badge', b.I(1))
    pop(badge, 160, 0.3)
    nod(badge, 280, -10, hold=80)
    return "The rows are written again one after another and the check badge pops in with a nod."


@spec('data_array')
def _(b):
    r = b.part('right', b.I(0))
    l = b.part('left', b.I(1))
    dart(l, 0, -0.9, 0)
    dart(r, 0, 0.9, 0)
    return "The square brackets wind in and push outward, then spring back."
