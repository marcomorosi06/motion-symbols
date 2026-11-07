# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 861-908 (coffee_maker .. content_paste).

from lib import *  # noqa: F401,F403


def drip(n, t, dy=1.6, back=-0.6):
    """A drop falls out of sight and a new one forms in its place."""
    n.ty.to(t, dy, (300.0, 1.0))
    n.alpha.to(t + 60, 0.0, EFFECTS_SLOW)
    n.ty.snap(t + 260, back)
    n.sx.snap(t + 260, 0.2)
    n.sy.snap(t + 260, 0.2)
    n.ty.to(t + 262, 0.0, SPATIAL)
    n.sx.to(t + 262, 1.0, BOUNCY)
    n.sy.to(t + 262, 1.0, BOUNCY)
    n.alpha.to(t + 262, 1.0, EFFECTS)
    return t + 700


@spec('coffee_maker')
def _(b):
    m = b.part('machine', b.I(0), pivot='b')
    d = b.part('drop', b.I(1))
    squash(m, 0, 0.04)
    drip(d, 40, 2.2, -0.4)
    return "The machine hums, a drop falls into the cup and the next one forms."


@spec('collapse_all')
def _(b):
    bot = b.part('bottom', b.I(0))
    top = b.part('top', b.I(1))
    dart(top, 0, 0, 1.2)
    dart(bot, 0, 0, -1.2)
    return "The two chevrons push toward each other, collapsing everything, and spring back."


@spec('collapse_content')
def _(b):
    bl = b.part('bottom_left', b.I(0))
    tr = b.part('top_right', b.I(1))
    dart(bl, 0, 0.8, -0.8)
    dart(tr, 0, -0.8, 0.8)
    return "The two corners push in toward the center and spring back."


@spec('collections_bookmark')
def _(b):
    front = b.part('front', b.I(0))
    back = b.part('back', b.I(1))
    shift(front, 0, dx=0.6, dy=-0.6, hold=120)
    shift(back, 40, dx=-0.4, dy=0.4, hold=100)
    return "The bookmarked page lifts off the stack and settles back."


@spec('colorize')
def _(b):
    d = b.part('dropper', b.I(0), pivot=(4.0, 20.0))
    nod(d, 0, -7, hold=100)
    pressxy(d, 150, 0.94, 0.94, hold=60)
    return "The dropper dips to pick up a color, squeezes and springs back."


@spec('colors')
def _(b):
    bucket = b.part('bucket', b.I(0), pivot=(17.0, 13.0))
    drop = b.part('drop', b.I(1), pivot='t')
    nod(bucket, 0, 12, hold=110)
    pop(drop, 90, 0.1, dt=60)
    return "The paint bucket tips and a fresh drop of paint drips out of it."


@spec('combine_columns')
def _(b):
    l = b.part('left', b.I(0))
    r = b.part('right', b.I(1))
    p = b.part('plus', b.I(2))
    shift(l, 0, dx=0.6, hold=100)
    shift(r, 0, dx=-0.6, hold=100)
    plus_badge(p, 40)
    return "The two columns push together and the plus between them contracts and springs back."


@spec('comedy_mask')
def _(b):
    face = b.part('mask', b.I(1), pivot='b')
    el = b.part('eye_l', b.I(2), parent=face)
    er = b.part('eye_r', b.I(3), parent=face)
    mouth = b.part('mouth', b.I(0), pivot='t', parent=face)
    pressxy(el, 0, 1, 0.4, hold=160, spec_out=SPATIAL)
    pressxy(er, 0, 1, 0.4, hold=160, spec_out=SPATIAL)
    pressxy(mouth, 0, 1.08, 1.25, hold=160, spec_out=SPATIAL)
    rock(face, 40, 5, 3, 90)
    return "The mask laughs: its eyes squint, its grin widens and it rocks with laughter."


@spec('comic_bubble')
def _(b):
    c = b.part('bubble', b.I(0))
    press(c, 0, 0.82, hold=80, spec_out=BOUNCY)
    c.rot.kick(80, 400.0, BOUNCY)
    return "The comic bubble bursts out with a bounce and a shake."


@spec('comment')
def _(b):
    bub = b.part('bubble', b.I(3), pivot=(3.0, 20.0))
    press(bub, 0, 0.95)
    for k, i in enumerate([2, 1, 0]):
        redraw(b, b.part('line%d' % k, b.I(i)), 50 + k * 70, 0)
    return "The bubble gives and its lines are written again one after another."


@spec('comment_bank')
def _(b):
    c = b.part('bubble', b.I(0), pivot=(3.0, 20.0))
    press(c, 0, 0.86, hold=90, spec_out=BOUNCY)
    return "The bubble with its bookmark pops up from its tail with a springy bounce."


@spec('comments_disabled')
def _(b):
    c = b.part('comment', b.all())
    off, on, t = off_icon(b, 'comment')
    press(c, t, 0.95)
    return "The slash retracts, showing the comment whole for a moment, and cuts across again; then it flinches."


@spec('commit')
def _(b):
    c = b.part('commit', b.I(0))
    pressxy(c, 0, 0.82, 1, hold=90)
    press(c, 90, 0.9, hold=70)
    return "The line pulls into the commit node, which pulses, and both spring back."


@spec('communication')
def _(b):
    lh = b.part('left_head', b.I(1), pivot='b')
    lb = b.part('left_body', b.I(0), pivot='b')
    rh = b.part('right_head', b.I(5), pivot='b')
    rb = b.part('right_body', b.I(4), pivot='b')
    w0 = b.part('wave_small', b.I(2))
    w1 = b.part('wave_big', b.I(3))
    nod(lh, 0, 10, hold=90)
    squash(lb, 0, 0.06)
    blink(w0, 80, 0.1)
    blink(w1, 140, 0.1)
    nod(rh, 220, -10, hold=90)
    squash(rb, 220, 0.06)
    return "One person speaks, the waves travel across, and the other nods in reply."


@spec('communities')
def _(b):
    ring_ = b.part('ring', b.I(3))
    dots = [b.part('p%d' % k, b.I(i), pivot='b', parent=ring_) for k, i in enumerate([2, 1, 0])]
    press(ring_, 0, 0.96)
    stagger(dots, 40, 80, hop, h=0.8, stretch=1.03)
    return "The members of the community hop one after another inside the circle."


@spec('commute')
def _(b):
    train = b.part('train', b.I(3), pivot='b')
    car = b.part('car', b.I(0), pivot='b')
    b.part('l0', b.I(1), parent=car)
    b.part('l1', b.I(2), parent=car)
    car.tx.to(0, 1.0, SPATIAL)
    car.tx.back(140, BOUNCY)
    squash(train, 120, 0.05)
    return "The car pulls out and back in beside the train, which settles."


@spec('compare')
def _(b):
    l = b.part('left', b.I(0))
    r = b.part('right', b.I(1))
    shift(l, 0, dx=-0.6, hold=120)
    shift(r, 0, dx=0.6, hold=120)
    return "The two halves slide apart to be compared and come back together."


@spec('compare_arrows')
def _(b):
    bot = b.part('right_arrow', b.I(0))
    top = b.part('left_arrow', b.I(1))
    dart(bot, 0, 0.9, 0)
    dart(top, 50, -0.9, 0)
    return "The two arrows dart past each other in opposite directions and spring back."


@spec('compass_calibration')
def _(b):
    ring_ = b.part('ring', b.I(0))
    arc = b.part('signal', b.I(1), pivot=(12.0, 17.0))
    press(arc, 0, 0.85, hold=80)
    press(arc, 220, 0.9, hold=80)
    press(ring_, 60, 0.9)
    return "The signal arc pulses twice over the ring as the compass calibrates."


@spec('component_exchange')
def _(b):
    top = b.part('top', b.I(1), pivot='b')
    right = b.part('right', b.I(2), pivot='b')
    left = b.part('left', b.I(0), pivot='b')
    stagger([top, right, left], 0, 90, hop, h=0.7, stretch=1.03)
    return "The three components hop one after another, passing the exchange around."


@spec('compress')
def _(b):
    top = b.part('top_arrow', b.I(3))
    bot = b.part('bottom_arrow', b.I(2))
    l1 = b.part('line_top', b.I(1))
    l0 = b.part('line_bottom', b.I(0))
    dart(top, 0, 0, 1.0)
    dart(bot, 0, 0, -1.0)
    shift(l1, 90, dy=0.5, hold=90)
    shift(l0, 90, dy=-0.5, hold=90)
    return "The arrows push in from above and below and squeeze the lines together."


def _computer(b, screen, base):
    scr = b.part('screen', b.I(screen))
    bs = b.part('base', b.I(base), pivot='b')
    press(scr, 0, 0.96)
    pressxy(bs, 0, 1, 0.55, hold=80)
    return scr


@spec('computer_arrow_up')
def _(b):
    scr = _computer(b, 2, 1)
    a = b.part('arrow', b.I(0), parent=scr)
    dart(a, 60, 0, -1.0)
    return "The screen gives and the arrow on it darts up."


@spec('computer_cancel')
def _(b):
    scr = _computer(b, 2, 1)
    x = b.part('x', b.I(0), parent=scr)
    rock(x, 60, 14, 3, 90)
    return "The screen gives and the x on it shakes its head."


@spec('computer_sound')
def _(b):
    scr = _computer(b, 1, 0)
    w0 = b.part('wave_small', b.I(2), pivot=(16.0, 10.5))
    w1 = b.part('wave_big', b.I(3), pivot=(16.0, 10.5))
    press(w0, 60, 0.6, hold=60, spec_out=BOUNCY)
    press(w1, 130, 0.75, hold=60, spec_out=SPATIAL)
    return "The screen gives and the sound waves ripple out of it one after another."


@spec('concierge')
def _(b):
    hand = b.part('hand', b.I(2))
    bell = b.part('bell', b.I(1), pivot='b')
    base = b.part('base', b.I(0), pivot='b')
    hand.ty.to(0, 0.9, SPATIAL_FAST)
    hand.ty.back(90, BOUNCY)
    squash(bell, 70, 0.12, hold=60)
    bell.rot.kick(140, 500.0, (900.0, 0.2))
    squash(base, 70, 0.2)
    return "The hand taps the service bell, which squashes and rings."


@spec('conditions')
def _(b):
    head = b.part('head', b.I(0), pivot='b')
    body = b.part('body', b.I(3), pivot='b')
    lens = b.part('lens', b.I(1))
    dot = b.part('dot', b.I(2))
    for k, (x, y) in enumerate([(-0.7, -0.5), (0.4, -0.8), (0.5, 0.3)]):
        lens.tx.to(k * 110, x, SPATIAL)
        lens.ty.to(k * 110, y, SPATIAL)
    lens.tx.back(330, BOUNCY)
    lens.ty.back(330, BOUNCY)
    nod(head, 120, -10, hold=100)
    squash(body, 120, 0.04)
    blink(dot, 200, 0.0)
    return "The magnifier looks the person over and they nod as it checks the conditions."


@spec('confirmation_number')
def _(b):
    t = b.part('ticket', b.I(0), pivot='b')
    dots = [b.part('d%d' % k, b.I(i), parent=t) for k, i in enumerate([3, 2, 1])]
    squash(t, 0, 0.06)
    stagger(dots, 60, 60, pop, low=0.0)
    return "The ticket is punched: its holes pop through one after another."


@spec('congenital')
def _(b):
    c = b.part('organ', b.I(0))
    press(c, 0, 0.9, hold=70)
    press(c, 200, 0.92, hold=70)
    return "The shape pulses twice, like a heartbeat."


@spec('connect_without_contact')
def _(b):
    lh = b.part('left_head', b.I(3), pivot='b')
    lb = b.part('left_body', b.I(2), pivot='b')
    rh = b.part('right_head', b.I(1), pivot='b')
    rb = b.part('right_body', b.I(0), pivot='b')
    w0 = b.part('wave_small', b.I(5))
    w1 = b.part('wave_big', b.I(4))
    nod(lh, 0, 10, hold=90)
    squash(lb, 0, 0.05)
    blink(w0, 80, 0.1)
    blink(w1, 140, 0.1)
    nod(rh, 220, -10, hold=90)
    squash(rb, 220, 0.05)
    return "The signal travels from one person to the other, who nods back: connected without contact."


@spec('connected_tv')
def _(b):
    tv = b.part('tv', b.I(0))
    corner = (5.0, 16.0)
    d = b.part('dot', b.I(1), pivot=corner, parent=tv)
    s = b.part('wave_small', b.I(3), pivot=corner, parent=tv)
    g = b.part('wave_big', b.I(2), pivot=corner, parent=tv)
    press(tv, 0, 0.97)
    for k, n in enumerate([d, s, g]):
        press(n, 30 + k * 70, 0.6, hold=60, spec_out=BOUNCY)
    return "The TV gives and the casting waves ripple out of its corner one after another."


def _contact_card(b, card, head):
    c = b.part('card', b.I(card))
    h = b.part('head', b.I(head), pivot='b', parent=c)
    hop(h, 0, 0.6, stretch=1.03)
    return c


@spec('contact_emergency')
def _(b):
    c = _contact_card(b, 0, 1)
    a = b.part('asterisk', b.I(2), pivot=(18.0, 9.0), parent=c)
    spin(a, 60, 60, SPATIAL)
    pop(a, 60, 0.3)
    return "The person on the card hops and the emergency asterisk pops and turns a sixth."


@spec('contact_mail')
def _(b):
    c = _contact_card(b, 1, 2)
    env = b.part('envelope', b.I(0), pivot='b', parent=c)
    hop(env, 100, 0.8, stretch=1.03)
    return "The person on the card hops and the envelope beside them bounces in."


@spec('contact_page')
def _(b):
    pg = b.part('page', b.I(2))
    head = b.part('head', b.I(0), pivot='b')
    sh = b.part('shoulders', b.I(1), pivot='b')
    p = b.group('person', [head, sh], pivot='b', parent=pg)
    press(pg, 0, 0.97)
    hop(p, 40, 0.8, stretch=1.03)
    return "The page gives and the person on it hops."


@spec('contact_phone')
def _(b):
    c = _contact_card(b, 1, 2)
    h = b.part('handset', b.I(0), parent=c)
    ring(h, 80, 14)
    return "The person on the card hops and the handset beside them rings."


@spec('contact_support')
def _(b):
    bub = b.part('bubble', b.I(0), pivot=(12.0, 21.0))
    q = b.part('question', b.I(2), pivot='b', parent=bub)
    dot = b.part('dot', b.I(1), pivot='b', parent=bub)
    press(bub, 0, 0.95)
    rock(q, 40, 12, 2, 100)
    hop(dot, 60, 0.7, stretch=1.03)
    return "The bubble gives, the question mark tilts its head and its dot hops."


@spec('contactless')
def _(b):
    ring_ = b.part('ring', b.I(3))
    c = (5.0, 12.0)
    ws = [b.part('w%d' % k, b.I(i), pivot=c, parent=ring_) for k, i in enumerate([0, 1, 2])]
    press(ring_, 0, 0.96)
    for k, n in enumerate(ws):
        press(n, 30 + k * 70, 0.7, hold=60, spec_out=BOUNCY)
    return "The contactless waves ripple outward one after another inside the circle."


@spec('contactless_off')
def _(b):
    c = b.part('contactless', b.all())
    off, on, t = off_icon(b, 'contactless')
    press(c, t, 0.95)
    return "The slash retracts, showing the waves whole for a moment, and cuts across again; then the icon flinches."


@spec('contacts')
def _(b):
    card = b.part('card', b.I(3))
    top = b.part('top', b.I(1))
    bot = b.part('bottom', b.I(0))
    head = b.part('head', b.I(2), pivot='b', parent=card)
    press(card, 0, 0.95)
    shift(top, 0, dy=-0.6, hold=100)
    shift(bot, 0, dy=0.6, hold=100)
    hop(head, 60, 0.6, stretch=1.03)
    return "The contact card gives, the bars above and below spring apart and the person hops."


@spec('contacts_product')
def _(b):
    head = b.part('head', b.I(2), pivot='b')
    body = b.part('body', b.I(1), pivot='b')
    hand = b.part('hand', b.I(0), pivot='b')
    nod(head, 0, -10, hold=100)
    squash(body, 0, 0.05)
    lift(hand, 60, -0.8, hold=100)
    return "The person nods and lifts the product toward you."
