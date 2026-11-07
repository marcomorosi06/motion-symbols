# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 717-764 (cardiology .. check).

from lib import *  # noqa: F401,F403


@spec('cardiology')
def _(b):
    top = b.part('top', b.I(0))
    bot = b.part('bottom', b.I(1))
    heart = b.group('heart', [top, bot], pivot=(12.0, 12.0))
    line = b.part('pulse', b.I(2))
    redraw(b, line, 0, 0, erase_ms=90, spec_draw=SPATIAL_SLOW)
    press(heart, 150, 0.88, hold=70)
    return "The ECG line is traced again from left to right and the heart beats as the pulse passes."


@spec('cards')
def _(b):
    f = b.part('frame', b.I(4))
    cards = [b.part('c%d' % k, b.I(i), parent=f) for k, i in enumerate([0, 2, 1, 3])]
    for k, c in enumerate(cards):
        c.sx.to(k * 70, 0.1, SPATIAL)
        c.sx.back(k * 70 + 110, BOUNCY)
    return "The four cards flip over one after another."


@spec('cards_star')
def _(b):
    front = b.part('front', b.I(1))
    star = b.part('star', b.I(0), pivot=(14.5, 9.367), parent=front)
    back = b.part('back', b.I(2))
    shift(front, 0, dx=0.6, dy=-0.6, hold=120)
    shift(back, 40, dx=-0.4, dy=0.4, hold=100)
    spin(star, 80, 72, SPATIAL)
    pop(star, 80, 0.4)
    return "The top card lifts off the stack and its star pops and twinkles a fifth of a turn."


@spec('carpenter')
def _(b):
    saw = b.part('saw', b.I(0))
    for k, s in enumerate([1, -1, 1]):
        saw.tx.to(k * 110, -0.7 * s, SPATIAL_FAST)
        saw.ty.to(k * 110, -0.7 * s, SPATIAL_FAST)
    saw.tx.back(330, BOUNCY)
    saw.ty.back(330, BOUNCY)
    return "The saw cuts back and forth along its blade and settles."


@spec('carry_on_bag')
def _(b):
    bag = b.part('bag', b.I(0), pivot=(16.0, 21.5))
    bag.rot.to(0, -6, SPATIAL)
    bag.tx.to(0, 0.6, SPATIAL)
    bag.rot.back(140, BOUNCY)
    bag.tx.back(140, BOUNCY)
    return "The bag tips onto its wheel, rolls a little and rocks back upright."


def _bag_badge(b, badge_fn):
    bag = b.part('bag', b.I(0), pivot='b')
    badge = b.part('badge', b.I(1))
    squash(bag, 0, 0.06)
    badge_fn(badge)


@spec('carry_on_bag_checked')
def _(b):
    _bag_badge(b, lambda n: (pop(n, 80, 0.3), nod(n, 200, -10, hold=80)))
    return "The bag settles and the check badge pops in with a nod."


@spec('carry_on_bag_question')
def _(b):
    _bag_badge(b, lambda n: (pop(n, 80, 0.3), rock(n, 180, 12, 2, 100)))
    return "The bag settles and the question badge pops in and tilts its head, wondering."


@spec('carry_on_bag_inactive')
def _(b):
    bag = b.part('bag', b.I(1), pivot='b')
    b.part('handle', b.I(0), parent=bag)
    bag.tx.kick(0, -35.0, (900.0, 0.25))
    return "The slashed bag gives a short shudder: it is out of use."


@spec('casino')
def _(b):
    f = b.part('frame', b.I(5))
    for k, i in enumerate([0, 1, 2, 3, 4]):
        b.part('pip%d' % k, b.I(i), parent=f)
    jump = b.group('die', [f], pivot='b')
    spin(f, 60, 90, SPATIAL)
    press(f, 40, 0.84, hold=170, spec_out=SPATIAL)
    hop(jump, 0, 1.0)
    return "The die hops, rolls a quarter turn in the air and lands on the same face."


def _cast_waves(b, dot, small, big, t0=0, corner=(2.0, 20.0)):
    d = b.part('dot', b.I(dot), pivot=corner)
    s = b.part('wave1', b.I(small), pivot=corner)
    g = b.part('wave2', b.I(big), pivot=corner)
    for k, n in enumerate([d, s, g]):
        press(n, t0 + k * 70, 0.6, hold=60, spec_out=BOUNCY)
    return [d, s, g]


@spec('cast')
def _(b):
    scr = b.part('screen', b.I(0))
    press(scr, 0, 0.98)
    _cast_waves(b, 3, 1, 2, 30)
    return "The casting waves ripple out of the corner one after another."


@spec('cast_connected')
def _(b):
    scr = b.part('screen', b.I(1))
    fill = b.part('fill', b.I(0), parent=scr)
    _cast_waves(b, 4, 2, 3, 0)
    radial_pop(b, fill, 200)
    return "The casting waves ripple out of the corner and the screen fills up: connected."


@spec('cast_for_education')
def _(b):
    scr = b.part('screen', b.I(2))
    cap = b.part('cap', b.I(0))
    base = b.part('cap_base', b.I(1))
    hat = b.group('hat', [cap, base], pivot='b', parent=scr)
    _cast_waves(b, 5, 3, 4, 0)
    hop(hat, 150, 1.0)
    nod(cap, 230, -10, hold=80)
    return "The casting waves ripple out and the graduation cap is tossed up and lands with a tilt."


@spec('cast_pause')
def _(b):
    b.part('frame_r', b.I(0))
    b.part('frame_t', b.I(1))
    badge = b.part('badge', b.I(2))
    _cast_waves(b, 3, 4, 5, 0)
    press(badge, 120, 0.82, hold=180, spec_out=SPATIAL)
    return "The casting waves ripple out and the pause badge presses down and holds before letting go."


@spec('cast_warning')
def _(b):
    b.part('frame_r', b.I(0))
    b.part('frame_t', b.I(1))
    badge = b.part('badge', b.I(2))
    _cast_waves(b, 3, 4, 5, 0)
    alert_badge(badge, 120)
    return "The casting waves ripple out and the warning badge pops and shakes."


@spec('castle')
def _(b):
    c = b.part('castle', b.I(0), pivot='b')
    w0 = b.part('window0', b.I(1), parent=c)
    w1 = b.part('window1', b.I(2), parent=c)
    squash(c, 0, 0.06)
    blink(w0, 100, 0.0)
    blink(w1, 170, 0.0)
    return "The castle settles on its base and its windows light up one after the other."


@spec('category')
def _(b):
    tri = b.part('triangle', b.I(0), pivot='b')
    sq = b.part('square', b.I(2), pivot='b')
    ci = b.part('circle', b.I(1), pivot='b')
    stagger([tri, sq, ci], 0, 90, hop, h=1.0)
    return "The three shapes hop one after another: triangle, square, circle."


@spec('category_search')
def _(b):
    sq = b.part('square', b.I(0), pivot='b')
    tri = b.part('triangle', b.I(1), pivot='b')
    lens = b.part('lens', b.I(2))
    for k, (x, y) in enumerate([(-0.8, -0.4), (0.4, -0.8), (0.6, 0.3)]):
        lens.tx.to(k * 110, x, SPATIAL)
        lens.ty.to(k * 110, y, SPATIAL)
    lens.tx.back(330, BOUNCY)
    lens.ty.back(330, BOUNCY)
    hop(sq, 40, 0.8)
    hop(tri, 150, 0.8)
    return "The magnifier circles around searching and the shapes hop as it passes them."


@spec('celebration')
def _(b):
    cone = b.part('popper', b.I(4), pivot=(4.0, 20.0))
    mouth = (11.0, 13.0)
    bits = [b.part('c%d' % k, b.I(i), pivot=mouth) for k, i in enumerate([1, 2, 0, 3])]
    nod(cone, 0, -6, hold=70)
    for k, n in enumerate(bits):
        n.sx.to(20 + k * 25, 0.0, EFFECTS_FAST)
        n.sy.to(20 + k * 25, 0.0, EFFECTS_FAST)
        n.sx.back(110 + k * 25, SPATIAL)
        n.sy.back(110 + k * 25, SPATIAL)
    return "The popper kicks and the confetti bursts out of its mouth, piece after piece."


@spec('cell_merge')
def _(b):
    corners = [(0, 0.5, 0.5), (1, -0.5, 0.5), (4, 0.5, -0.5), (5, -0.5, -0.5)]
    cells = [(b.part('cell%d' % k, b.I(i)), dx, dy) for k, (i, dx, dy) in enumerate(corners)]
    right = b.part('arrow_in_r', b.I(2))
    left = b.part('arrow_in_l', b.I(3))
    dart(left, 0, 0.9, 0)
    dart(right, 0, -0.9, 0)
    for n, dx, dy in cells:
        shift(n, 90, dx=dx, dy=dy, hold=100)
    return "The arrows push in from both sides and the cells squeeze together, then spring apart."


@spec('cell_tower')
def _(b):
    tower = b.part('tower', b.I(2), pivot='b')
    c = (12.0, 10.0)
    in_l = b.part('in_l', b.I(1), pivot=c)
    in_r = b.part('in_r', b.I(3), pivot=c)
    out_l = b.part('out_l', b.I(0), pivot=c)
    out_r = b.part('out_r', b.I(4), pivot=c)
    squash(tower, 0, 0.05)
    for n in (in_l, in_r):
        press(n, 40, 0.75, hold=60, spec_out=SPATIAL)
    for n in (out_l, out_r):
        press(n, 120, 0.82, hold=60, spec_out=SPATIAL)
    return "The tower pulses and its signal waves ripple outward, inner pair first."


@spec('cell_wifi')
def _(b):
    tri = b.part('cell', b.I(0), pivot='br')
    dot = b.part('dot', b.I(1))
    a1 = b.part('arc1', b.I(2))
    a2 = b.part('arc2', b.I(3))
    press(tri, 0, 0.92)
    for k, n in enumerate([dot, a1, a2]):
        blink(n, 60 + k * 70, 0.1, hold=60)
    return "The cell signal gives and the wifi waves light up from the dot outward."


def _focus(b, ring_s):
    ring = b.part('target', b.I(4))
    dirs = {0: (0.8, -0.8), 1: (-0.8, -0.8), 2: (0.8, 0.8), 3: (-0.8, 0.8)}
    for i, (dx, dy) in dirs.items():
        n = b.part('corner%d' % i, b.I(i))
        shift(n, 0, dx=dx, dy=dy, hold=110, spec_out=SPATIAL_FAST)
    press(ring, 60, ring_s, hold=90)


@spec('center_focus_strong')
def _(b):
    _focus(b, 0.8)
    return "The frame corners close in to focus and the target pulses sharply."


@spec('center_focus_weak')
def _(b):
    _focus(b, 0.9)
    return "The frame corners close in to focus and the target pulses softly."


@spec('chair')
def _(b):
    c = b.part('chair', b.I(0), pivot='b')
    squash(c, 0, 0.1, hold=120)
    return "Someone sits down: the armchair squashes into its cushion and springs back."


@spec('chair_alt')
def _(b):
    c = b.part('chair', b.I(0), pivot='b')
    c.rot.to(0, -5, SPATIAL)
    c.rot.back(110, BOUNCY)
    squash(c, 110, 0.07)
    return "The chair tips back on its legs and drops down with a squash."


@spec('chair_counter')
def _(b):
    c = b.part('stool', b.I(0), pivot='b')
    pressxy(c, 0, 1.0, 0.86, hold=100, spec_out=BOUNCY)
    return "The bar stool is pushed down on its spring and bounces back up."


@spec('chair_fireplace')
def _(b):
    chair = b.part('chair', b.I(2), pivot='b')
    fire = b.part('fireplace', b.I(1))
    flame = b.part('flame', b.I(0), pivot='b', parent=fire)
    flicker(flame, 0, 0.25)
    flicker(flame, 220, 0.15)
    rock(chair, 60, 4, 2, 170, SPATIAL_SLOW)
    return "The fire flickers in the fireplace and the chair rocks gently in front of it."


@spec('chair_umbrella')
def _(b):
    chair = b.part('chair', b.I(0), pivot='b')
    umb = b.part('umbrella', b.I(1), pivot=(13.5, 21.0))
    table = b.part('table', b.I(2), pivot='b')
    rock(umb, 0, 4, 2, 160, SPATIAL_SLOW)
    squash(chair, 80, 0.05)
    squash(table, 140, 0.05)
    return "The umbrella sways in the breeze and the chair and table settle in its shade."


@spec('chalet')
def _(b):
    h = b.part('chalet', b.I(1), pivot='b')
    flake = b.part('snowflake', b.I(0))
    spin(flake, 0, 90, SPATIAL_SLOW)
    flake.ty.to(0, 0.6, SPATIAL_SLOW)
    flake.ty.back(260, SPATIAL)
    squash(h, 120, 0.05)
    return "The snowflake drifts down a little, turning, and the chalet settles under the snow."


@spec('change_circle')
def _(b):
    ring = b.part('ring', b.I(2))
    a0 = b.part('a0', b.I(0))
    a1 = b.part('a1', b.I(1))
    g = b.group('arrows', [a0, a1], pivot=(12.0, 12.0), parent=ring)
    press(ring, 0, 0.95)
    spin(g, 0, 180, SPATIAL)
    return "The two arrows inside the circle swap places with a half turn."


@spec('change_history')
def _(b):
    t = b.part('triangle', b.I(0), pivot='b')
    hop(t, 0, 1.0)
    return "The triangle hops and lands with a squash."


@spec('charger')
def _(b):
    ring = b.part('ring', b.I(1))
    bolt = b.part('bolt', b.I(0), parent=ring)
    press(ring, 0, 0.95)
    blink(bolt, 0, 0.0, hold=60)
    pop(bolt, 140, 0.5)
    return "The charge bolt flashes and pops back in, and the ring gives with the jolt."


@spec('charging_station')
def _(b):
    body = b.part('station', b.I(1))
    bolt = b.part('bolt', b.I(0), parent=body)
    press(body, 0, 0.96)
    blink(bolt, 0, 0.0, hold=60)
    pop(bolt, 140, 0.5)
    return "The charge bolt flashes and pops back in, and the station gives with the jolt."


@spec('chart_data')
def _(b):
    f = b.part('frame', b.I(1))
    line = b.part('trend', b.I(0), parent=f)
    redraw(b, line, 0, -35, erase_ms=90)
    dart(line, 300, 0.5, -0.35, wind=0.0, go=40, hold=60)
    return "The trend line is drawn again from the bottom left and gives a last push upward."


def _lines(b, ids, t0=0, dt=70, angle=0):
    ls = [b.part('line%d' % k, b.I(i)) for k, i in enumerate(ids)]
    for k, n in enumerate(ls):
        redraw(b, n, t0 + k * dt, angle)
    return ls


@spec('chat')
def _(b):
    bub = b.part('bubble', b.I(0), pivot=(3.0, 20.0))
    press(bub, 0, 0.95)
    _lines(b, [3, 2, 1], 50)
    return "The bubble gives and its lines are written again one after another."


@spec('chat_add_on')
def _(b):
    bub = b.part('bubble', b.I(0), pivot=(3.0, 19.0))
    press(bub, 0, 0.95)
    _lines(b, [1, 2], 50)
    p = b.part('plus', b.I(3))
    plus_badge(p, 150)
    return "The bubble gives, its lines are written again and the plus contracts and springs back."


@spec('chat_apps_script')
def _(b):
    bub = b.part('bubble', b.I(1), pivot=(3.0, 19.0))
    press(bub, 0, 0.95)
    _lines(b, [2, 3], 50)
    a = b.part('arrow', b.I(0))
    dart(a, 150, 0.6, 0.6)
    return "The bubble gives, its lines are written again and the script arrow darts to the corner."


@spec('chat_bubble')
def _(b):
    bub = b.part('bubble', b.I(0), pivot=(3.0, 20.0))
    press(bub, 0, 0.84, hold=90, spec_out=BOUNCY)
    return "The bubble pops up from its tail with a springy bounce."


@spec('chat_bubble_off')
def _(b):
    p0 = b.part('rest', b.I(0))
    p1 = b.part('slashed', b.I(1))
    off, on, t = off_icon(b, 'chat_bubble')
    press(p1, t, 0.96)
    return "The slash retracts, showing the bubble whole for a moment, and cuts across again; then the bubble flinches."


@spec('chat_dashed')
def _(b):
    order = [7, 6, 5, 4, 3, 2, 1, 0]
    dashes = [b.part('d%d' % k, b.I(i)) for k, i in enumerate(order)]
    stagger(dashes, 0, 45, blink, low=0.1, hold=50)
    return "The dashes light up in turn around the bubble, like marching ants."


@spec('chat_display')
def _(b):
    bub = b.part('bubble', b.I(2), pivot=(3.0, 20.0))
    press(bub, 0, 0.96)
    _lines(b, [1, 0, 3], 40)
    disp = b.part('display', b.I(4))
    pop(disp, 120, 0.4)
    return "The bubble gives, its lines are written again and the display pops in."


@spec('chat_error')
def _(b):
    bub = b.part('bubble', b.I(1), pivot=(3.0, 20.0))
    x = b.part('x', b.I(0), parent=bub)
    press(bub, 0, 0.95)
    rock(x, 40, 14, 3, 90)
    return "The bubble gives and the x inside shakes its head."


@spec('chat_info')
def _(b):
    bub = b.part('bubble', b.I(2), pivot=(3.0, 20.0))
    dot = b.part('dot', b.I(0), pivot='b', parent=bub)
    bar = b.part('bar', b.I(1), pivot='b', parent=bub)
    press(bub, 0, 0.95)
    pressxy(bar, 40, 1, 0.75, hold=80)
    hop(dot, 60, 1.0)
    return "The bubble gives, the i squashes and its dot hops."


@spec('chat_paste_go')
def _(b):
    bub = b.part('bubble', b.I(1), pivot=(3.0, 19.0))
    press(bub, 0, 0.95)
    _lines(b, [2, 3], 40)
    a = b.part('arrow', b.I(0))
    dart(a, 100, 0.9, 0)
    return "The bubble gives, its lines are written again and the arrow darts on to send it."


@spec('chat_paste_go_2')
def _(b):
    bub = b.part('bubble', b.I(1), pivot=(3.0, 19.0))
    press(bub, 0, 0.95)
    a = b.part('arrow', b.I(0))
    dart(a, 60, 0.9, 0)
    return "The bubble gives and the arrow winds back and darts on to send it."


@spec('check')
def _(b):
    k = b.part('check', b.I(0))
    check_draw(b, k, 0)
    return "The check is erased and drawn again from left to right, popping at the end."
