# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 621-668 (bubble .. call_split).

from lib import *  # noqa: F401,F403


@spec('bubble')
def _(b):
    circ = b.part('circle', b.I(0))
    arrow = b.part('arrow', b.I(1), pivot='bl')
    arrow.tx.to(0, -0.7, SPATIAL)
    arrow.ty.to(0, 0.7, SPATIAL)
    arrow.tx.to(120, 1.0, SPATIAL_FAST)
    arrow.ty.to(120, -1.0, SPATIAL_FAST)
    arrow.tx.back(240, BOUNCY)
    arrow.ty.back(240, BOUNCY)
    swell(circ, 120, 1.05, hold=110)
    return "The arrow winds back into the bubble and pops out toward the corner; the bubble swells as it lets go."


@spec('bubble_chart')
def _(b):
    small = b.part('small', b.I(0))
    big = b.part('big', b.I(1))
    mid = b.part('mid', b.I(2))
    for i, n in enumerate([small, mid, big]):
        t = i * 90
        swell(n, t, 1.1, hold=120)
        lift(n, t, -0.9, hold=140)
    return "The bubbles swell one after another and float up a little, like bubbles rising."


@spec('bubbles')
def _(b):
    frame = b.part('frame', b.I(2))
    arrow = b.part('arrow', b.I(0))
    dot = b.part('dot', b.I(1))
    dart(arrow, 0, 0.9, 0.9)
    pop(dot, 150, 0.4)
    press(frame, 150, 0.97)
    return "The arrow winds back and darts toward the corner bubble, which pops in response."


@spec('bucket_check')
def _(b):
    bucket = b.part('bucket', b.I(0), pivot=(12.0, 3.0))
    check = b.part('check', b.I(1), parent=bucket)
    rock(bucket, 0, 6, 2, 140)
    check_draw(b, check, 200)
    return "The bucket sways on its handle and the check is drawn again, popping at the end."


@spec('bug_report')
def _(b):
    body = b.part('body', b.I(0), pivot='b')
    s0 = b.part('s0', b.I(2), parent=body)
    s1 = b.part('s1', b.I(1), parent=body)
    for i, x in enumerate([-0.8, 0.8, -0.6]):
        body.tx.to(i * 90, x, SPATIAL_FAST)
        body.rot.to(i * 90, -x * 5, SPATIAL_FAST)
    body.tx.back(270, BOUNCY)
    body.rot.back(270, BOUNCY)
    blink(s0, 60, 0.2)
    blink(s1, 150, 0.2)
    return "The bug scurries left and right, wiggling, and its stripes flicker in turn."


@spec('build')
def _(b):
    w = b.part('wrench', b.I(0), pivot=(7.0, 7.0))
    w.rot.to(0, -12, SPATIAL)
    w.rot.to(150, 0, SPATIAL_FAST)
    w.rot.to(250, -12, SPATIAL)
    w.rot.back(400, BOUNCY)
    return "The wrench tightens a bolt with two ratchet turns and springs back."


@spec('build_circle')
def _(b):
    r = b.part('ring', b.I(1))
    w = b.part('wrench', b.I(0), pivot=(10.0, 10.0), parent=r)
    press(r, 0, 0.96)
    w.rot.to(0, -14, SPATIAL)
    w.rot.to(150, 0, SPATIAL_FAST)
    w.rot.to(250, -14, SPATIAL)
    w.rot.back(400, BOUNCY)
    return "The ring gives and the wrench inside tightens a bolt with two ratchet turns."


@spec('bungalow')
def _(b):
    h = b.part('house', b.I(0), pivot='b')
    w = b.part('window', b.I(1), parent=h)
    squash(h, 0, 0.1)
    blink(w, 120, 0.1, hold=80)
    return "The bungalow settles on its base and its window lights up with a blink."


@spec('burst_mode')
def _(b):
    f = b.part('frame', b.I(2))
    m = b.part('photo', b.I(3), parent=f)
    s1 = b.part('back1', b.I(1))
    s0 = b.part('back0', b.I(0))
    for k in range(3):
        t = k * 130
        f.sx.to(t, 0.92, SPATIAL_FAST)
        f.sy.to(t, 0.92, SPATIAL_FAST)
        f.sx.to(t + 55, 1.0, SPATIAL_FAST)
        f.sy.to(t + 55, 1.0, SPATIAL_FAST)
        s1.tx.kick(t + 20, -30.0, BOUNCY)
        s0.tx.kick(t + 50, -30.0, BOUNCY)
    f.sx.back(390, BOUNCY)
    f.sy.back(390, BOUNCY)
    return "The shutter fires three times: the photo squeezes and the back frames flick out one after another."


@spec('bus_alert')
def _(b):
    bus = b.part('bus', b.I(0), pivot='b')
    l0 = b.part('light0', b.I(2), parent=bus)
    l1 = b.part('light1', b.I(3), parent=bus)
    badge = b.part('badge', b.I(1))
    squash(bus, 0, 0.08)
    blink(l0, 60, 0.1)
    blink(l1, 60, 0.1)
    alert_badge(badge, 120)
    return "The bus brakes with a jolt, its headlights flash, and the alert badge pops and shakes."


def _bus_pin(b, bus_i, lights, pin_i, dot_i):
    bus = b.part('bus', b.I(bus_i), pivot='b')
    for k, i in enumerate(lights):
        b.part('light%d' % k, b.I(i), parent=bus)
    pin = b.part('pin', b.I(pin_i), pivot='b')
    b.part('pin_dot', b.I(dot_i), parent=pin)
    pop(pin, 0, 0.3, dt=80, spec_out=SPATIAL_FAST)
    squash(bus, 150, 0.07)
    return "The pin pops up on its point and the bus bounces under it."


@spec('bus_map_pin')
def _(b):
    return _bus_pin(b, 2, [0, 1], 3, 4)


@spec('bus_map_pin_2')
def _(b):
    return _bus_pin(b, 0, [2, 3], 4, 1)


@spec('bus_railway')
def _(b):
    bus = b.part('bus', b.I(2), pivot='b')
    b.part('light', b.I(0), parent=bus)
    train = b.part('train', b.I(1), pivot='b')
    hop(train, 0, 1.2)
    squash(bus, 330, 0.06)
    return "The train hops in beside the bus; the bus settles as it lands."


@spec('business_center')
def _(b):
    bag = b.part('bag', b.I(0), pivot=(12.0, 2.0))
    drop = b.group('drop', [bag], pivot='b')
    bag.ty.to(0, -0.9, SPATIAL)
    rock(bag, 60, 4, 2, 110)
    bag.ty.to(280, 0.0, SPATIAL_FAST)
    squash(drop, 340, 0.06)
    return "The briefcase is lifted by its handle, swings and is set down with a squash."


@spec('business_chip')
def _(b):
    chip = b.part('chip', b.I(1))
    bag = b.part('bag', b.I(0), pivot='b', parent=chip)
    press(chip, 0, 0.96)
    hop(bag, 60, 0.9)
    return "The chip gives and the briefcase inside hops."


@spec('business_messages')
def _(b):
    f = b.part('bubble', b.I(0))
    top = b.part('right', b.I(2), parent=f)
    bot = b.part('left', b.I(1), parent=f)
    press(f, 0, 0.96)
    dart(top, 40, 1.2, 0)
    dart(bot, 100, -1.2, 0)
    return "The bubble gives and the two arrows dart in their directions, one after the other."


@spec('buttons_alt')
def _(b):
    f = b.part('button', b.I(0))
    p = b.part('plus', b.I(1), parent=f)
    pressxy(f, 0, 0.95, 0.88)
    plus_badge(p, 70)
    return "The button is pressed down and springs back; its plus contracts and springs back."


@spec('cabin')
def _(b):
    h = b.part('cabin', b.I(0), pivot='b')
    s = b.part('smoke', b.I(1), pivot='b')
    squash(h, 0, 0.06)
    s.ty.to(0, -0.9, SPATIAL_SLOW)
    s.alpha.to(0, 0.0, EFFECTS_SLOW)
    s.ty.snap(280, 0.7)
    s.ty.to(282, 0.0, SPATIAL_SLOW)
    s.alpha.to(282, 1.0, EFFECTS_SLOW)
    return "A puff of smoke rises from the chimney and a new one follows, while the cabin settles."


@spec('cached')
def _(b):
    a = b.part('a0', b.I(0))
    c = b.part('a1', b.I(1))
    g = b.group('arrows', [a, c], pivot=(12.0, 12.0))
    spin(g, 0, 180)
    return "Both arrows spin a half turn together and land on themselves."


@spec('cadence')
def _(b):
    mid = b.part('mid', b.I(0))
    l = b.part('left', b.I(1))
    r = b.part('right', b.I(2))
    dl = b.part('dot_l', b.I(4))
    dr = b.part('dot_r', b.I(5))
    arc = b.part('arc', b.I(3))
    pressxy(mid, 0, 1, 0.6)
    pressxy(l, 70, 1, 0.55)
    pressxy(r, 70, 1, 0.55)
    press(dl, 140, 0.5)
    press(dr, 140, 0.5)
    lift(arc, 90, -0.7)
    return "The bars bounce like an equalizer from the center outward and the arc above lifts with the beat."


@spec('cake')
def _(b):
    c = b.part('cake', b.I(0), pivot='b')
    hop(c, 0, 0.7)
    return "The cake gives a happy hop and lands with a squash, candle and all."


@spec('cake_add')
def _(b):
    c = b.part('cake', b.I(1), pivot='b')
    p = b.part('plus', b.I(0))
    hop(c, 0, 0.7)
    plus_badge(p, 200)
    return "The cake gives a happy hop; the plus contracts and springs back."


@spec('calculate')
def _(b):
    f = b.part('frame', b.I(5))
    plus = b.part('plus', b.I(0), parent=f)
    minus = b.part('minus', b.I(4), parent=f)
    times = b.part('times', b.I(3), parent=f)
    e0 = b.part('eq0', b.I(2))
    e1 = b.part('eq1', b.I(1))
    eq = b.group('equals', [e0, e1], parent=f)
    for i, n in enumerate([plus, minus, times, eq]):
        press(n, i * 90, 0.6, hold=70, spec_out=BOUNCY)
    press(f, 270, 0.96)
    return "The keys are pressed one after another, the equals last, and the calculator gives."


def cal_flip(n, t):
    """Calendar page flip: squeezes toward its rings and drops back."""
    n.sy.to(t, 0.86, SPATIAL)
    n.sx.to(t, 1.03, SPATIAL)
    n.sy.back(t + 110, BOUNCY)
    n.sx.back(t + 110, BOUNCY)
    return t + 400


@spec('calendar_add_on')
def _(b):
    c = b.part('calendar', b.I(1), pivot='t')
    p = b.part('plus', b.I(0))
    cal_flip(c, 0)
    plus_badge(p, 140)
    return "The calendar page flips up and drops back; the plus contracts and springs back."


@spec('calendar_apps_script')
def _(b):
    c = b.part('calendar', b.I(1), pivot='t')
    a = b.part('arrow', b.I(0))
    cal_flip(c, 0)
    dart(a, 120, 0.6, 0.6)
    return "The calendar page flips and the script arrow winds back and darts to the corner."


@spec('calendar_check')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    k = b.part('check', b.I(1))
    cal_flip(c, 0)
    check_draw(b, k, 140)
    return "The calendar page flips and the check is drawn again, popping at the end."


@spec('calendar_clock')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    clk = b.part('clock', b.I(1))
    hands = b.hole('hands', clk, b.isl[1], 0, pivot=(18.0, 18.0))
    cal_flip(c, 0)
    press(clk, 80, 0.9)
    spin(hands, 120, 360, SPATIAL_SLOW)
    return "The calendar page flips and the clock hands sweep a full turn."


@spec('calendar_lock')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    lk = b.part('lock', b.I(1), pivot='b')
    cal_flip(c, 0)
    lk.ty.to(120, -0.7, SPATIAL_FAST)
    lk.ty.back(200, BOUNCY)
    wobble(lk, 260, 300.0)
    return "The calendar page flips and the lock clicks shut with a jolt."


@spec('calendar_meal')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    fork = b.part('fork', b.I(1), pivot='b', parent=c)
    knife = b.part('knife', b.I(2), pivot='b', parent=c)
    cal_flip(c, 0)
    nod(fork, 120, 6, hold=90)
    nod(knife, 120, -6, hold=90)
    return "The calendar page flips and the fork and knife lean in for a clink."


@spec('calendar_meal_2')
def _(b):
    c = b.part('calendar', b.I(1), pivot='t')
    m = b.part('meal', b.I(0), pivot='b', parent=c)
    cal_flip(c, 0)
    hop(m, 110, 0.8)
    return "The calendar page flips and the meal inside hops."


@spec('calendar_month')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    order = [2, 1, 3, 5, 4, 6]
    dots = [b.part('d%d' % k, b.I(i), parent=c) for k, i in enumerate(order)]
    cal_flip(c, 0)
    stagger(dots, 100, 45, pop, low=0.2)
    return "The calendar page flips and the days pop in one after another."


@spec('calendar_today')
def _(b):
    c = b.part('calendar', b.I(0), pivot='t')
    cal_flip(c, 0)
    return "The calendar page flips up and drops back with a bounce."


@spec('call')
def _(b):
    h = b.part('handset', b.I(0))
    ring(h, 0, 12)
    return "The handset rings: a quick shake that dies down."


@spec('call_end')
def _(b):
    h = b.part('handset', b.I(0), pivot='b')
    h.ty.to(0, 1.2, SPATIAL)
    h.ty.back(150, SPATIAL)
    rock(h, 40, 6, 2, 120)
    return "The handset is put down: it dips, rocks and settles."


@spec('call_log')
def _(b):
    h = b.part('handset', b.I(0))
    lines = [b.part('l%d' % k, b.I(i)) for k, i in enumerate([1, 2, 3])]
    ring(h, 0, 6)
    for k, n in enumerate(lines):
        redraw(b, n, 80 + k * 70, 0)
    return "The handset rings and the log lines are written again one after another."


@spec('call_quality')
def _(b):
    h = b.part('handset', b.I(0))
    i = b.part('badge', b.I(1), pivot='b')
    ring(h, 0, 6)
    pop(i, 150, 0.3, dt=80)
    lift(i, 260, -0.6, hold=90)
    return "The handset rings and the info badge pops in and nods."
