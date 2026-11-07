# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 765-812 (check_alert .. circle_circle).

from lib import *  # noqa: F401,F403


@spec('check_alert')
def _(b):
    k = b.part('check', b.I(0))
    badge = b.part('badge', b.I(1))
    check_draw(b, k, 0)
    alert_badge(badge, 260)
    return "The check is drawn again, then the alert badge pops and shakes."


@spec('check_box')
def _(b):
    box = b.part('box', b.I(1))
    k = b.part('check', b.I(0), parent=box)
    press(box, 0, 0.92)
    check_draw(b, k, 60, pop_s=1.12)
    return "The box is pressed and the check is drawn again, popping at the end."


@spec('check_box_outline_blank')
def _(b):
    box = b.part('box', b.I(0))
    press(box, 0, 0.88, hold=90)
    return "The empty box gives under a tap and springs back."


@spec('check_circle')
def _(b):
    c = b.part('circle', b.I(1))
    k = b.part('check', b.I(0), parent=c)
    press(c, 0, 0.93)
    check_draw(b, k, 60, pop_s=1.12)
    return "The circle is pressed and the check is drawn again, popping at the end."


@spec('check_circle_unread')
def _(b):
    c = b.part('circle', b.I(1))
    k = b.part('check', b.I(2), parent=c)
    dot = b.part('dot', b.I(0))
    press(c, 0, 0.94)
    check_draw(b, k, 60, pop_s=1.12)
    pop(dot, 200, 0.2)
    return "The check is drawn again inside the circle and the unread dot pops back in."


@spec('check_in_out')
def _(b):
    i = b.part('i', b.I(1), pivot='b')
    n = b.part('n', b.I(2), pivot='b')
    o = b.part('o', b.I(0), pivot='b')
    u = b.part('u', b.I(3), pivot='b')
    t = b.part('t', b.I(4), pivot='b')
    stagger([i, n], 0, 70, hop, h=0.8)
    stagger([o, u, t], 200, 70, hop, h=0.8)
    return "The letters hop in reading order: first IN, then OUT."


@spec('check_indeterminate_small')
def _(b):
    d = b.part('dash', b.I(0))
    pressxy(d, 0, 0.35, 1.0, hold=90, spec_out=BOUNCY)
    return "The dash shrinks toward its center and stretches back with a bounce."


@spec('check_small')
def _(b):
    k = b.part('check', b.I(0))
    check_draw(b, k, 0)
    return "The check is erased and drawn again from left to right, popping at the end."


@spec('checkbook')
def _(b):
    book = b.part('book', b.I(2))
    l1 = b.part('line_top', b.I(1))
    l0 = b.part('line_bottom', b.I(0))
    tip = b.part('tip', b.I(3))
    body = b.part('pen_body', b.I(4))
    pen = b.group('pen', [tip, body], pivot=(14.0, 20.0))
    press(book, 0, 0.98)
    redraw(b, l1, 40, 0)
    redraw(b, l0, 140, 0)
    for k, (x, y) in enumerate([(-0.6, 0.3), (0.3, -0.2), (-0.4, 0.2)]):
        pen.tx.to(40 + k * 90, x, SPATIAL_FAST)
        pen.ty.to(40 + k * 90, y, SPATIAL_FAST)
    pen.tx.back(310, BOUNCY)
    pen.ty.back(310, BOUNCY)
    return "The pen scribbles and the lines of the check are written again one after the other."


@spec('checked_bag')
def _(b):
    belt = b.part('belt', b.I(0), pivot='b')
    bag = b.part('bag', b.I(1), pivot='b')
    bag.ty.to(0, -1.0, SPATIAL)
    bag.ty.to(160, 0.0, (700.0, 0.9))
    squash(bag, 240, 0.08)
    squash(belt, 240, 0.3)
    return "The bag is lifted and dropped onto the belt, which gives under its weight."


@spec('checked_bag_question')
def _(b):
    belt = b.part('belt', b.I(0), pivot='b')
    bag = b.part('bag', b.I(1), pivot='b')
    badge = b.part('badge', b.I(2))
    squash(bag, 0, 0.06)
    squash(belt, 0, 0.3)
    pop(badge, 80, 0.3)
    rock(badge, 180, 12, 2, 100)
    return "The bag settles on the belt and the question badge pops in and tilts its head, wondering."


def _checklist(b, top_check, bot_check, top_line, bot_line, angle=0):
    c1 = b.part('check_top', b.I(top_check))
    c0 = b.part('check_bottom', b.I(bot_check))
    l1 = b.part('line_top', b.I(top_line))
    l0 = b.part('line_bottom', b.I(bot_line))
    check_draw(b, c1, 0, angle)
    redraw(b, l1, 120, angle)
    check_draw(b, c0, 200, angle)
    redraw(b, l0, 320, angle)


@spec('checklist')
def _(b):
    _checklist(b, 1, 0, 3, 2)
    return "Each item is ticked again in turn: the check is drawn, then its line is written."


@spec('checklist_rtl')
def _(b):
    _checklist(b, 1, 0, 3, 2, 180)
    return "Each item is ticked again in turn, right to left: the check is drawn, then its line is written."


@spec('checkroom')
def _(b):
    h = b.part('hanger', b.I(0), pivot=(12.0, 4.0))
    rock(h, 0, 5, 3, 150, SPATIAL_SLOW)
    return "The hanger swings on its hook and comes to rest."


@spec('cheer')
def _(b):
    l = b.part('left_hand', b.I(3), pivot='b')
    r = b.part('right_hand', b.I(4), pivot='b')
    sp = [b.part('spark%d' % k, b.I(i)) for k, i in enumerate([0, 1, 2])]
    for n, s in ((l, 1), (r, -1)):
        n.ty.to(0, -0.8, SPATIAL)
        n.rot.to(0, 5 * s, SPATIAL)
        n.rot.to(110, -4 * s, SPATIAL_FAST)
        n.ty.back(220, BOUNCY)
        n.rot.back(220, BOUNCY)
    stagger(sp, 120, 50, pop, low=0.0)
    return "Both hands shoot up and wave, and the sparkles pop above them one after another."


@spec('chef_hat')
def _(b):
    hat = b.part('hat', b.I(1), pivot=(12.0, 18.0))
    s0 = b.part('fold0', b.I(0), parent=hat)
    s1 = b.part('fold1', b.I(2), parent=hat)
    band = b.part('band', b.I(3), pivot='b')
    swell(hat, 0, 1.08, hold=120)
    squash(band, 40, 0.15)
    return "The chef's hat puffs up like rising dough and settles on its band."


# ---------------------------------------------------------------- chess

@spec('chess')
def _(b):
    top = b.part('top', b.I(1))
    base = b.part('base', b.I(0))
    piece = b.group('piece', [top, base], pivot='b')
    hop(piece, 0, 0.8, stretch=1.02)
    return "The piece is lifted, moves and is set down with a squash."


@spec('chess_pawn')
def _(b):
    p = b.part('pawn', b.I(0), pivot='b')
    hop(p, 0, 0.9, stretch=1.02)
    return "The pawn hops one square forward and lands with a squash."


@spec('chess_pawn_2')
def _(b):
    p = b.part('pawn', b.I(0), pivot='b')
    hop(p, 0, 0.9, stretch=1.02)
    return "The pawn hops one square forward and lands with a squash."


@spec('chess_knight')
def _(b):
    k = b.part('knight', b.I(0), pivot='b')
    k.sy.to(0, 0.9, SPATIAL_FAST)
    k.ty.to(70, -0.9, SPATIAL)
    k.sy.to(70, 1.02, SPATIAL_FAST)
    k.rot.to(70, 8, SPATIAL)
    k.tx.to(150, 1.2, SPATIAL)
    k.ty.to(240, 0.0, (700.0, 0.9))
    k.rot.to(240, 0.0, SPATIAL)
    k.sy.to(330, 0.9, SPATIAL_FAST)
    k.sy.back(400, BOUNCY)
    k.tx.back(400, SPATIAL)
    return "The knight leaps in an L: up, across, and down with a squash, then trots back."


@spec('chess_bishop')
def _(b):
    p = b.part('bishop', b.I(0), pivot='b')
    b.part('dot', b.I(1), parent=p)
    shift(p, 0, dx=0.8, dy=-0.8, hold=130)
    nod(p, 0, 6, hold=130)
    return "The bishop glides along its diagonal, leaning into the move, and slides back."


@spec('chess_bishop_2')
def _(b):
    head = b.part('head', b.I(0), pivot='b')
    cross = b.part('cross', b.I(2))
    base = b.part('base', b.I(1), pivot='b')
    p = b.group('piece', [head, base, cross], pivot='b')
    shift(p, 0, dx=0.8, dy=-0.8, hold=130)
    plus_badge(cross, 120, 0.7)
    return "The bishop glides along its diagonal and slides back; its cross contracts and springs back."


@spec('chess_king')
def _(b):
    crown = b.part('crown', b.I(0), pivot='b')
    base = b.part('base', b.I(1), pivot='b')
    squash(base, 0, 0.06)
    nod(crown, 60, -8, hold=100)
    return "The king settles on its base and its crown gives a regal nod."


@spec('chess_king_2')
def _(b):
    halves = b.geo_part('halves', [])
    right = b.bake('right', halves, b.I(0))
    left = b.bake('left', halves, b.I(1))
    cross = b.bake('cross', halves, b.I(2), pivot='b')
    shift(left, 0, dx=-0.5, hold=120)
    shift(right, 0, dx=0.5, hold=120)
    hop(cross, 30, 0.4, stretch=1.02)
    return "The two halves part and the cross hops between them, then everything settles back."


@spec('chess_queen')
def _(b):
    q = b.part('queen', b.I(0), pivot='b')
    pressxy(q, 0, 0.96, 1.07, hold=140, spec_out=SPATIAL)
    return "The queen rises to her full height and settles back with poise."


@spec('chess_rook')
def _(b):
    r = b.part('rook', b.I(0), pivot='b')
    r.tx.to(0, 1.0, SPATIAL)
    r.rot.to(0, 3, SPATIAL_FAST)
    r.rot.back(90, BOUNCY)
    r.tx.back(170, BOUNCY)
    return "The rook slides sideways in a straight line, as if castling, and slides back."


# ---------------------------------------------------------------- chevrons

# ---------------------------------------------------------------- child

@spec('chips')
def _(b):
    f = b.part('frame', b.I(1))
    bar = b.part('bar', b.I(0), parent=f)
    press(f, 0, 0.95)
    pressxy(bar, 40, 0.45, 1, hold=80, spec_out=BOUNCY)
    return "The chip is pressed and its bar shrinks to the middle and stretches back."


@spec('chrome_minimize')
def _(b):
    bar = b.part('bar', b.I(0))
    bar.ty.to(0, 1.2, SPATIAL)
    bar.ty.back(110, BOUNCY)
    pressxy(bar, 0, 0.7, 1, hold=110)
    return "The bar drops down a notch as the window minimizes and bounces back."


@spec('chrome_reader_mode')
def _(b):
    book = b.part('book', b.I(0))
    press(book, 0, 0.97)
    _ls = [b.part('line%d' % k, b.I(i)) for k, i in enumerate([3, 2, 1])]
    for k, n in enumerate(_ls):
        redraw(b, n, 50 + k * 70, 0)
    return "The page settles and its lines are written again from top to bottom."


@spec('chrome_restore')
def _(b):
    back = b.part('back', b.I(0))
    front = b.part('front', b.I(1))
    shift(back, 0, dx=0.6, dy=-0.6, hold=120)
    shift(front, 0, dx=-0.6, dy=0.6, hold=120)
    return "The two windows pull apart and snap back into their stacked places."


@spec('chromecast_device')
def _(b):
    dev = b.part('device', b.I(1))
    led = b.part('led', b.I(0))
    press(dev, 0, 0.94)
    blink(led, 60, 0.0, hold=80)
    blink(led, 260, 0.0, hold=80)
    return "The device gives and its light blinks twice."


@spec('chronic')
def _(b):
    clk = b.part('clock', b.I(1))
    hand = b.part('hand', b.I(0), pivot=(11.0, 11.0), parent=clk)
    dots = [b.part('dot%d' % k, b.I(i)) for k, i in enumerate([2, 3, 4])]
    spin(hand, 0, 360, SPATIAL_SLOW)
    stagger(dots, 60, 70, blink, low=0.1)
    return "The clock hand sweeps a full turn while the dots light up one after another: time keeps going."


@spec('church')
def _(b):
    c = b.part('church', b.I(0), pivot='b')
    w = b.part('window', b.I(1), parent=c)
    rock(c, 0, 3, 2, 120)
    blink(w, 80, 0.0, hold=80)
    return "The church sways as its bell rings and its window lights up."


@spec('circle')
def _(b):
    c = b.part('circle', b.I(0))
    press(c, 0, 0.85, hold=90)
    return "The circle squeezes and springs back with a bounce."


@spec('circle_circle')
def _(b):
    o = b.part('outer', b.I(0))
    i = b.part('inner', b.I(1), parent=o)
    press(o, 0, 0.94)
    pop(i, 40, 0.3)
    return "The outer ring gives and the inner ring pops back in."
