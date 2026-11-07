# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 909-956 (content_paste_go .. credit_score).

from lib import *  # noqa: F401,F403


@spec('content_paste_go')
def _(b):
    c = b.part('clipboard', b.I(1), pivot='b')
    a = b.part('arrow', b.I(0))
    squash(c, 0, 0.05)
    dart(a, 40, 1.0, 0)
    return "The clipboard settles and the arrow darts on to paste."


@spec('content_paste_off')
def _(b):
    c = b.part('clipboard', b.all())
    off, on, t = off_icon(b, 'content_paste')
    press(c, t, 0.95)
    return "The slash retracts, showing the clipboard whole for a moment, and cuts across again; then it flinches."


@spec('content_paste_search')
def _(b):
    c = b.part('clipboard', b.I(1), pivot='b')
    lens = b.part('lens', b.I(0))
    squash(c, 0, 0.04)
    for k, (x, y) in enumerate([(-0.8, -0.6), (0.3, -0.9), (0.2, 0.2)]):
        lens.tx.to(k * 110, x, SPATIAL)
        lens.ty.to(k * 110, y, SPATIAL)
    lens.tx.back(330, BOUNCY)
    lens.ty.back(330, BOUNCY)
    return "The magnifier circles over the clipboard, searching."


@spec('contextual_token')
def _(b):
    f = b.part('frame', b.I(3))
    toks = [b.part('t%d' % k, b.I(i), parent=f) for k, i in enumerate([2, 0, 1])]
    press(f, 0, 0.97)
    stagger(toks, 40, 70, pop, low=0.3)
    return "The frame gives and the tokens inside pop one after another."


@spec('contextual_token_add')
def _(b):
    f = b.part('frame', b.I(0))
    toks = [b.part('t%d' % k, b.I(i), parent=f) for k, i in enumerate([2, 1, 3])]
    p = b.part('plus', b.I(4))
    press(f, 0, 0.97)
    stagger(toks, 40, 70, pop, low=0.3)
    plus_badge(p, 220)
    return "The tokens pop one after another and the plus contracts and springs back."


@spec('contract')
def _(b):
    pg = b.part('scroll', b.I(0))
    press(pg, 0, 0.97)
    for k, i in enumerate([1, 2]):
        redraw(b, b.part('line%d' % k, b.I(i)), 40 + k * 80, 0)
    return "The contract settles and its lines are written again one after the other."


@spec('contract_delete')
def _(b):
    pg = b.part('scroll', b.I(1))
    press(pg, 0, 0.97)
    for k, i in enumerate([2, 3]):
        redraw(b, b.part('line%d' % k, b.I(i)), 40 + k * 80, 0)
    x = b.part('x', b.I(0))
    rock(x, 160, 14, 3, 90)
    return "The lines are written again and the x beside them shakes its head."


@spec('contract_edit')
def _(b):
    pg = b.part('scroll', b.I(2))
    press(pg, 0, 0.97)
    for k, i in enumerate([0, 1]):
        redraw(b, b.part('line%d' % k, b.I(i)), 40 + k * 80, 0)
    pen = b.part('pen', b.I(3), pivot='bl')
    for k, (x, y) in enumerate([(-0.6, 0.3), (0.3, -0.2), (-0.4, 0.2)]):
        pen.tx.to(40 + k * 90, x, SPATIAL_FAST)
        pen.ty.to(40 + k * 90, y, SPATIAL_FAST)
    pen.tx.back(310, BOUNCY)
    pen.ty.back(310, BOUNCY)
    return "The pen scribbles while the lines of the contract are written again."


def _contrast_pm(b):
    shape = b.part('shape', b.I(0))
    plus = b.hole('plus', shape, b.isl[0], 1)
    minus = b.part('minus', b.I(1))
    plus_badge(plus, 0, 0.6)
    pressxy(minus, 120, 0.5, 1, hold=80, spec_out=BOUNCY)


@spec('contrast_circle')
def _(b):
    _contrast_pm(b)
    return "The plus contracts and springs back, then the minus shrinks and stretches back."


@spec('contrast_square')
def _(b):
    _contrast_pm(b)
    return "The plus contracts and springs back, then the minus shrinks and stretches back."


@spec('contrast_rtl_off')
def _(b):
    c = b.part('contrast', b.all())
    off, on, t = off_icon(b, 'contrast')
    press(c, t, 0.95)
    return "The slash retracts, showing the contrast circle whole for a moment, and cuts across again; then it flinches."


@spec('control_camera')
def _(b):
    dot = b.part('center', b.I(0))
    up = b.part('up', b.I(3))
    right = b.part('right', b.I(4))
    down = b.part('down', b.I(1))
    left = b.part('left', b.I(2))
    press(dot, 0, 0.7)
    for k, (n, dx, dy) in enumerate([(up, 0, -0.7), (right, 0.7, 0), (down, 0, 0.7), (left, -0.7, 0)]):
        shift(n, 40 + k * 60, dx=dx, dy=dy, hold=80)
    return "The center presses and the four arrows push outward in turn, going around."


@spec('control_point_duplicate')
def _(b):
    ring_ = b.part('ring', b.I(1), pivot='r')
    p = b.part('plus', b.I(2), parent=ring_)
    back = b.part('back', b.I(0))
    press(ring_, 0, 0.95)
    plus_badge(p, 40)
    shift(back, 60, dx=0.5, hold=90, spec_out=SPATIAL)
    return "The circle gives, its plus contracts and springs back, and the copy behind it shifts."


@spec('controller_gen')
def _(b):
    outer = b.part('outer', b.I(2))
    inner = b.part('inner', b.I(0), parent=outer)
    stick = b.part('stick', b.I(1), parent=inner)
    press(outer, 0, 0.96)
    press(inner, 40, 0.85)
    shift(stick, 80, dx=0.6, dy=-0.6, hold=90)
    return "The controller is pressed and its stick flicks and springs back."


@spec('conversation')
def _(b):
    l = b.part('left', b.I(2), pivot='b')
    r = b.part('right', b.I(3), pivot='b')
    b.part('eye_l', b.I(0), parent=l)
    b.part('eye_r', b.I(1), parent=r)
    nod(l, 0, 6, hold=90)
    nod(r, 200, -6, hold=90)
    return "The two faces take turns: one leans in to speak, then the other answers."


@spec('conversion_path')
def _(b):
    p = b.part('path', b.I(0))
    redraw(b, p, 0, 40, erase_ms=100, spec_draw=SPATIAL_SLOW)
    return "The path is drawn again from its start to its goal."


@spec('conversion_path_off')
def _(b):
    c = b.part('path', b.all())
    off, on, t = off_icon(b, 'conversion_path')
    press(c, t, 0.95)
    return "The slash retracts, showing the path whole for a moment, and cuts across again; then it flinches."


@spec('convert_to_text')
def _(b):
    f = b.part('frame', b.I(0))
    arrow = b.part('arrow', b.I(1), pivot=(8.0, 11.0))
    press(f, 0, 0.98)
    nod(arrow, 0, -14, hold=100)
    for k, i in enumerate([4, 3, 2]):
        redraw(b, b.part('line%d' % k, b.I(i)), 80 + k * 70, 0)
    return "The arrow swings around and the text is written in line by line."


@spec('conveyor_belt')
def _(b):
    belt = b.part('belt', b.I(0))
    box = b.part('box', b.I(1), pivot='b')
    b.part('tape', b.I(3), parent=box)
    l0 = b.part('speed_top', b.I(4))
    l1 = b.part('speed_bottom', b.I(2))
    box.tx.to(0, 1.2, SPATIAL)
    box.rot.to(0, -4, SPATIAL_FAST)
    box.rot.back(90, BOUNCY)
    box.tx.back(180, BOUNCY)
    blink(l0, 0, 0.1)
    blink(l1, 50, 0.1)
    press(belt, 0, 0.98)
    return "The box rides along the belt and slides back, with the speed lines flickering."


@spec('cookie')
def _(b):
    c = b.part('cookie', b.I(0))
    chips = [b.part('chip%d' % k, b.I(i), parent=c) for k, i in enumerate([1, 2, 3])]
    nod(c, 0, -10, hold=100)
    stagger(chips, 60, 60, pop, low=0.2)
    return "The cookie wobbles and its chips pop one after another."


@spec('cookie_off')
def _(b):
    c = b.part('cookie', b.all())
    off, on, t = off_icon(b, 'cookie')
    press(c, t, 0.95)
    return "The slash retracts, showing the cookie whole for a moment, and cuts across again; then it flinches."


@spec('cooking')
def _(b):
    lid = b.part('lid', b.I(3), pivot='b')
    pot = b.part('pot', b.I(2), pivot='b')
    h0 = b.part('leg_l', b.I(0))
    h1 = b.part('leg_r', b.I(1))
    for k in range(2):
        lid.ty.to(k * 160, -0.9, SPATIAL_FAST)
        lid.rot.to(k * 160, (-5, 5)[k], SPATIAL_FAST)
        lid.ty.to(k * 160 + 80, 0.0, SPATIAL_FAST)
        lid.rot.to(k * 160 + 80, 0.0, SPATIAL_FAST)
    lid.ty.back(320, BOUNCY)
    lid.rot.back(320, BOUNCY)
    squash(pot, 80, 0.04)
    return "The lid rattles twice on the boiling pot and settles."


@spec('cool_to_dry')
def _(b):
    drop = b.part('drop', b.I(0))
    press(drop, 0, 0.85, hold=120)
    for k, i in enumerate([1, 2, 3]):
        redraw(b, b.part('wave%d' % k, b.I(i)), 60 + k * 70, 0)
    return "The drop shrinks as the drying waves flow by one after another."


@spec('copyright')
def _(b):
    ring_ = b.part('ring', b.I(0))
    c = b.part('c', b.I(1), parent=ring_)
    press(ring_, 0, 0.95)
    spin(c, 0, 360, SPATIAL)
    return "The C turns a full circle inside the ring and lands back in place."


@spec('coronavirus')
def _(b):
    v = b.part('virus', b.I(0))
    dots = [b.part('d%d' % k, b.I(i), parent=v) for k, i in enumerate([6, 7, 5, 2, 1, 3, 4])]
    spin(v, 0, 45, SPATIAL)
    stagger(dots, 60, 40, pop, low=0.2)
    return "The virus turns an eighth and lands on its spikes while its dots pop in turn."


@spec('corporate_fare')
def _(b):
    bld = b.part('building', b.I(0), pivot='b')
    l0 = b.part('light_top', b.I(1), parent=bld)
    l1 = b.part('light_bottom', b.I(2), parent=bld)
    squash(bld, 0, 0.05)
    blink(l0, 80, 0.0)
    blink(l1, 160, 0.0)
    return "The building settles and its windows light up one after the other."


@spec('cottage')
def _(b):
    h = b.part('cottage', b.I(0), pivot='b')
    s = b.part('smoke', b.I(1), pivot='b')
    squash(h, 0, 0.06)
    s.ty.to(0, -0.9, SPATIAL_SLOW)
    s.alpha.to(0, 0.0, EFFECTS_SLOW)
    s.ty.snap(280, 0.7)
    s.ty.to(282, 0.0, SPATIAL_SLOW)
    s.alpha.to(282, 1.0, EFFECTS_SLOW)
    return "A puff of smoke rises from the chimney and a new one follows, while the cottage settles."


def _counter(b, ring_i, digit_i):
    ring_ = b.part('ring', b.I(ring_i))
    d = b.part('digit', b.I(digit_i), parent=ring_)
    press(ring_, 0, 0.95)
    roll(b, d, 20, up=True)


for _n in range(10):
    def _mk(n):
        @spec('counter_%d' % n)
        def _(b):
            if n == 7:
                _counter(b, 1, 0)
            else:
                _counter(b, 0, 1)
            return "The ring gives and the number rolls up like a counter and lands in place."
    _mk(_n)


@spec('create_new_folder')
def _(b):
    f = b.part('folder', b.I(0), pivot='b')
    p = b.part('plus', b.I(1), parent=f)
    squash(f, 0, 0.06)
    plus_badge(p, 60)
    return "The folder settles and the plus on it contracts and springs back."


def _card(b, card_i):
    c = b.part('card', b.I(card_i))
    dart(c, 0, 0.8, 0)
    return c


@spec('credit_card_clock')
def _(b):
    _card(b, 1)
    clk = b.part('clock', b.I(0))
    hands = b.hole('hands', clk, b.isl[0], 0, pivot=(18.0, 17.0))
    press(clk, 60, 0.9)
    spin(hands, 100, 360, SPATIAL_SLOW)
    return "The card swipes and the clock hands sweep a full turn."


@spec('credit_card_gear')
def _(b):
    _card(b, 1)
    g = b.part('gear', b.I(0), pivot=(17.9, 17.0))
    spin(g, 60, 60, SPATIAL)
    return "The card swipes and the gear turns a sixth, landing on its teeth."


@spec('credit_card_heart')
def _(b):
    _card(b, 1)
    h = b.part('heart', b.I(0))
    press(h, 60, 0.82, hold=70)
    press(h, 240, 0.86, hold=70)
    return "The card swipes and the heart beats twice."


@spec('credit_card_off')
def _(b):
    c = b.part('card', b.all())
    off, on, t = off_icon(b, 'credit_card')
    press(c, t, 0.95)
    return "The slash retracts, showing the card whole for a moment, and cuts across again; then it flinches."


@spec('credit_card_spark')
def _(b):
    _card(b, 0)
    s = b.part('spark', b.I(1), pivot=(18.5, 17.5))
    spin(s, 60, 90, SPATIAL)
    pop(s, 60, 0.3)
    return "The card swipes and the sparkle pops and twinkles a quarter turn."


@spec('credit_score')
def _(b):
    _card(b, 0)
    k = b.part('check', b.I(1))
    check_draw(b, k, 80, pop_s=1.12)
    return "The card swipes and the check is drawn again, popping at the end."
