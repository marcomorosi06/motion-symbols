# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 669-716 (call_to_action .. cardio_load).

from lib import *  # noqa: F401,F403


@spec('call_to_action')
def _(b):
    f = b.part('screen', b.I(0))
    bar = b.part('button', b.I(1), parent=f)
    pressxy(bar, 0, 0.94, 0.55, hold=90)
    press(f, 60, 0.97)
    return "The action button is pressed and springs back; the screen gives with it."


@spec('camera')
def _(b):
    c = b.part('aperture', b.I(0))
    press(c, 0, 0.9, hold=160)
    spin(c, 0, 60, SPATIAL)
    return "The aperture twists a sixth of a turn as it closes, and opens again."


@spec('camera_enhance')
def _(b):
    body = b.part('camera', b.I(1))
    lens = b.part('lens', b.I(0), parent=body)
    press(body, 0, 0.94)
    spin(lens, 60, 90, SPATIAL)
    swell(lens, 60, 1.12, hold=120)
    return "The camera clicks and the sparkle in the lens twinkles a quarter turn."


@spec('camera_front')
def _(b):
    phone = b.part('phone', b.I(1))
    face = b.part('face', b.I(3), pivot='b', parent=phone)
    arrow = b.part('arrow', b.I(0))
    dash = b.part('dash', b.I(2))
    press(phone, 0, 0.95)
    hop(face, 60, 0.7)
    dart(arrow, 40, 0.8, 0)
    dart(dash, 100, 0.6, 0)
    return "The phone clicks, the face in the front camera hops and the switch arrow darts across."


@spec('camera_indoor')
def _(b):
    h = b.part('house', b.I(0), pivot='b')
    cam = b.part('camera', b.I(1), parent=h)
    squash(h, 0, 0.05)
    press(cam, 80, 0.82)
    nod(cam, 160, -6)
    return "The house settles and the camera inside squeezes into recording and pans a little."


@spec('camera_outdoor')
def _(b):
    h = b.part('house', b.I(1), pivot='b')
    cam = b.part('camera', b.I(0), pivot='l')
    rock(cam, 0, 9, 2, 160)
    squash(h, 60, 0.04)
    return "The outdoor camera pans back and forth on its mount, watching the house."


@spec('camera_rear')
def _(b):
    phone = b.part('phone', b.I(0))
    lens = b.part('lens', b.I(1), parent=phone)
    arrow = b.part('arrow', b.I(2))
    dash = b.part('dash', b.I(3))
    press(phone, 0, 0.95)
    pop(lens, 40, 0.3)
    dart(arrow, 40, 0.8, 0)
    dart(dash, 100, 0.6, 0)
    return "The phone clicks, the rear lens pops and the switch arrow darts across."


@spec('camera_video')
def _(b):
    body = b.part('webcam', b.I(1))
    lens = b.part('lens', b.I(2), parent=body)
    led = b.part('led', b.I(0), parent=body)
    blink(led, 0, 0.0, hold=70)
    press(lens, 80, 0.8)
    press(body, 80, 0.97)
    return "The webcam's light blinks on and the lens focuses with a squeeze."


@spec('cameraswitch')
def _(b):
    cam = b.part('camera', b.I(0))
    lens = b.part('lens', b.I(1), parent=cam)
    a0 = b.part('a0', b.I(2))
    a1 = b.part('a1', b.I(3))
    arrows = b.group('arrows', [a0, a1], pivot=(12.0, 12.0))
    spin(arrows, 0, 180, SPATIAL)
    press(arrows, 0, 0.9, hold=200, spec_out=SPATIAL)
    press(cam, 0, 0.9)
    pop(lens, 120, 0.3)
    return "The arrows swing a half turn around the camera, which squeezes as it switches sides."


@spec('cancel_schedule_send')
def _(b):
    plane = b.part('plane', b.I(0), pivot='l')
    x = b.part('badge', b.I(1))
    plane.tx.to(0, 0.8, SPATIAL)
    plane.tx.to(110, -0.6, SPATIAL_FAST)
    plane.tx.back(220, BOUNCY)
    alert_badge(x, 120, 12)
    return "The plane starts to leave and is pulled back, while the cancel badge pops and shakes."


@spec('candle')
def _(b):
    holder = b.part('holder', b.I(1), pivot='b')
    flame = b.part('flame', b.I(0), pivot='b')
    flicker(flame, 0, 0.14)
    flicker(flame, 220, 0.08)
    squash(holder, 0, 0.03)
    return "The flame flickers twice in a draught and the holder settles."


@spec('candlestick_chart')
def _(b):
    l = b.part('left', b.I(0))
    r = b.part('right', b.I(1))
    pressxy(l, 0, 1, 0.78, hold=100)
    l.ty.to(0, 0.8, SPATIAL)
    l.ty.back(100, BOUNCY)
    pressxy(r, 90, 1, 1.12, hold=100)
    r.ty.to(90, -0.6, SPATIAL)
    r.ty.back(190, BOUNCY)
    return "The candles trade: the left one dips and shrinks, the right one rises and stretches."


@spec('cannabis')
def _(b):
    leaf = b.part('leaf', b.I(0), pivot=(12.0, 22.0))
    rock(leaf, 0, 4, 3, 150, SPATIAL_SLOW)
    return "The leaf sways gently on its stem."


@spec('car_crash')
def _(b):
    car = b.part('car', b.I(0), pivot='b')
    b.part('l0', b.I(1), parent=car)
    b.part('l1', b.I(2), parent=car)
    badge = b.part('badge', b.I(3))
    car.tx.kick(0, -40.0, BOUNCY)
    car.rot.kick(0, -150.0, BOUNCY)
    alert_badge(badge, 90)
    return "The car is jolted by the impact and the alert badge pops and shakes."


@spec('car_gear')
def _(b):
    car = b.part('car', b.I(1), pivot='b')
    b.part('l0', b.I(2), parent=car)
    b.part('l1', b.I(3), parent=car)
    gear = b.part('gear', b.I(0), pivot=(18.0, 6.0))
    spin(gear, 0, 60, SPATIAL)
    squash(car, 80, 0.05)
    return "The gear turns a sixth and lands on its teeth; the car settles."


@spec('car_lock')
def _(b):
    car = b.part('car', b.I(2), pivot='b')
    b.part('l0', b.I(0), parent=car)
    b.part('l1', b.I(1), parent=car)
    lk = b.part('lock', b.I(3), pivot='b')
    lk.ty.to(0, -0.7, SPATIAL_FAST)
    lk.ty.back(80, BOUNCY)
    wobble(lk, 140, 300.0)
    squash(car, 80, 0.05)
    return "The lock clicks shut with a jolt and the car settles."


def _waves(b, ids, t0=0, dt=80):
    ws = [b.part('w%d' % k, b.I(i)) for k, i in enumerate(ids)]
    for k, w in enumerate(ws):
        redraw(b, w, t0 + k * dt, -90)
    return ws


@spec('car_mirror_heat')
def _(b):
    m = b.part('mirror', b.I(0))
    press(m, 0, 0.97)
    _waves(b, [3, 2, 1], 40, 80)
    return "Heat waves rise from the mirror one after another: each is erased and drawn up again."


@spec('car_rental')
def _(b):
    key = b.part('key', b.I(0))
    car = b.part('car', b.I(3), pivot='b')
    l0 = b.part('l0', b.I(1), parent=car)
    l1 = b.part('l1', b.I(2), parent=car)
    pressxy(key, 0, 1, 0.25, hold=90)
    blink(l0, 140, 0.0)
    blink(l1, 140, 0.0)
    squash(car, 120, 0.05)
    return "The key turns in place and the car answers by flashing its lights."


@spec('car_repair')
def _(b):
    car = b.part('car', b.I(3), pivot='b')
    b.part('l0', b.I(1), parent=car)
    b.part('l1', b.I(2), parent=car)
    base = b.part('lift', b.I(0), pivot='b')
    car.ty.to(0, -1.0, SPATIAL)
    car.ty.to(220, 0.0, SPATIAL_FAST)
    squash(car, 300, 0.06)
    squash(base, 300, 0.12)
    return "The car is raised on the lift and set back down with a bounce."


@spec('car_spark')
def _(b):
    car = b.part('car', b.I(2), pivot='b')
    b.part('l0', b.I(0), parent=car)
    b.part('l1', b.I(1), parent=car)
    sp = b.part('spark', b.I(3))
    spin(sp, 0, 90, SPATIAL)
    pop(sp, 0, 0.3)
    squash(car, 80, 0.05)
    return "The sparkle pops and twinkles a quarter turn; the car settles."


@spec('car_tag')
def _(b):
    car = b.part('car', b.I(2), pivot='b')
    b.part('l0', b.I(0), parent=car)
    b.part('l1', b.I(1), parent=car)
    tag = b.part('tag', b.I(4), pivot=(15.0, 5.0))
    b.part('hole', b.I(3), parent=tag)
    rock(tag, 0, 10, 3, 140, SPATIAL)
    squash(car, 60, 0.04)
    return "The price tag swings on its string and the car settles."


@spec('card_membership')
def _(b):
    c = b.part('card', b.I(0))
    c.sx.to(0, 0.15, SPATIAL)
    c.sx.back(140, BOUNCY)
    return "The card flips over in place and settles."


@spec('card_travel')
def _(b):
    c = b.part('case', b.I(0), pivot=(12.0, 2.0))
    drop = b.group('drop', [c], pivot='b')
    c.ty.to(0, -0.9, SPATIAL)
    rock(c, 60, 4, 2, 110)
    c.ty.to(280, 0.0, SPATIAL_FAST)
    squash(drop, 340, 0.06)
    return "The travel case is lifted by its handle, swings and is set down with a squash."
