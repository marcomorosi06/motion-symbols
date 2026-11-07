# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Specs for icons 813-860 (circle_notifications .. coffee).

from lib import *  # noqa: F401,F403
import math
from anim import Clip, Track


@spec('circle_notifications')
def _(b):
    ring_ = b.part('ring', b.I(1))
    bell = b.part('bell', b.I(2), pivot=(12.0, 5.5))
    clap = b.part('clapper', b.I(0), pivot=(12.0, 5.5))
    press(ring_, 0, 0.96)
    ring(bell, 0, 14)
    clap.rot.kick(60, -1100.0, (900.0, 0.2))
    return "The bell rings inside the circle: a quick shake, with the clapper swinging behind."


@spec('circles')
def _(b):
    arc = b.part('arc', b.I(0), pivot=(10.5, 13.5))
    ring_ = b.part('ring', b.I(1))
    nod(arc, 0, -10, hold=120)
    shift(ring_, 0, dx=-0.6, dy=0.6, hold=120)
    press(ring_, 0, 0.9)
    return "The arc swings back as the ring rolls into it, then both spring apart."


@spec('circles_ext')
def _(b):
    top = b.part('top', b.I(3))
    bl = b.part('left', b.I(0))
    br = b.part('right', b.I(1))
    dot = b.part('dot', b.I(2))
    pop(dot, 0, 0.2)
    shift(top, 60, dy=-0.7, hold=110)
    shift(bl, 60, dx=-0.6, dy=0.4, hold=110)
    shift(br, 60, dx=0.6, dy=0.4, hold=110)
    return "The center dot pops and pushes the three rings outward; they snap back together."


@spec('clarify')
def _(b):
    f = b.part('frame', b.I(4))
    press(f, 0, 0.97)
    ls = [b.part('line%d' % k, b.I(i)) for k, i in enumerate([3, 2, 0])]
    for k, n in enumerate(ls):
        redraw(b, n, 40 + k * 70, 0)
    bar = b.part('bar', b.I(1))
    pressxy(bar, 240, 1, 0.6, hold=80, spec_out=BOUNCY)
    return "The lines are written again one after another and the bar beside them springs to its full height."


@spec('clean_hands')
def _(b):
    hand = b.part('hand', b.I(0), pivot='b')
    pump = b.part('pump', b.I(1), pivot='b')
    drop = b.part('drop', b.I(2))
    pressxy(pump, 0, 1, 0.88, hold=80)
    drop.ty.to(60, 1.4, SPATIAL)
    drop.alpha.to(60, 0.0, EFFECTS_SLOW)
    drop.ty.snap(300, -1.0)
    drop.ty.to(302, 0.0, SPATIAL)
    drop.alpha.to(302, 1.0, EFFECTS)
    squash(hand, 160, 0.05)
    return "The pump is pressed, a drop falls into the hand and a new one forms."


@spec('cleaning')
def _(b):
    head = b.part('trigger', b.I(0), pivot='r')
    bottle = b.part('bottle', b.I(1), pivot='b')
    for k in range(2):
        pressxy(head, k * 160, 0.8, 1, hold=60, spec_out=SPATIAL_FAST)
        press(bottle, k * 160, 0.97, hold=60)
    return "The spray trigger is squeezed twice and the bottle gives with each squeeze."


@spec('cleaning_bucket')
def _(b):
    bucket = b.part('bucket', b.I(0), pivot='b')
    b.part('sponge', b.I(1), parent=bucket)
    big = b.part('bubble_big', b.I(3))
    small = b.part('bubble_small', b.I(2))
    squash(bucket, 0, 0.06)
    for k, n in enumerate([small, big]):
        t = 60 + k * 90
        n.ty.to(t, -0.8, SPATIAL_SLOW)
        n.sx.to(t + 150, 0.0, EFFECTS_FAST)
        n.sy.to(t + 150, 0.0, EFFECTS_FAST)
        n.ty.snap(t + 230, 0.0)
        n.sx.back(t + 232, BOUNCY)
        n.sy.back(t + 232, BOUNCY)
    return "The bucket sloshes and its bubbles float up and pop one after the other; new ones bubble up in their place."


@spec('cleaning_services')
def _(b):
    br = b.part('broom', b.I(0), pivot=(12.0, 1.0))
    rock(br, 0, 8, 3, 130)
    return "The broom sweeps back and forth and settles."


@spec('clear_all')
def _(b):
    ls = [b.part('line%d' % k, b.I(i)) for k, i in enumerate([2, 1, 0])]
    for k, n in enumerate(ls):
        redraw(b, n, k * 70, 0)
    return "The lines are swept away one after another and written back in."


@spec('clear_day')
def _(b):
    core = b.part('core', b.I(8))
    rays = [b.part('ray%d' % k, b.I(k)) for k in range(8)]
    g = b.group('rays', rays, pivot=(12.0, 12.0))
    spin(g, 0, 45, SPATIAL)
    press(core, 0, 0.85)
    return "The sun turns an eighth and lands on itself while its core pulses."


@spec('clear_night')
def _(b):
    m = b.part('moon', b.I(0))
    rock(m, 0, 8, 3, 170, SPATIAL_SLOW)
    return "The moon rocks gently, like a cradle."


@spec('climate_mini_split')
def _(b):
    unit = b.part('unit', b.I(0))
    vent = b.part('vent', b.I(2), pivot='t', parent=unit)
    press(unit, 0, 0.98)
    pressxy(vent, 0, 1, 0.6, hold=90)
    for k, i in enumerate([1, 3, 4]):
        n = b.part('air%d' % k, b.I(i))
        redraw(b, n, 90 + k * 60, 90)
    return "The vent flap opens and the air streams flow out downward, center first."


@spec('clinical_notes')
def _(b):
    page = b.part('page', b.I(2))
    press(page, 0, 0.98)
    for k, i in enumerate([3, 4, 5]):
        redraw(b, b.part('line%d' % k, b.I(i)), 40 + k * 70, 0)
    head = b.part('head', b.I(0))
    body = b.part('body', b.I(1))
    doc = b.group('doctor', [head, body], pivot='b')
    hop(doc, 120, 0.7, stretch=1.02)
    return "The notes are written again line by line and the doctor hops up beside them."


def _clock_arrow(b, dy):
    clk = b.part('clock', b.I(0))
    hand = b.part('hand', b.I(1), pivot=(8.5, 12.0), parent=clk)
    arrow = b.part('arrow', b.I(2))
    spin(hand, 0, 360, SPATIAL_SLOW)
    dart(arrow, 60, 0, dy)


@spec('clock_arrow_down')
def _(b):
    _clock_arrow(b, 1.0)
    return "The clock hand sweeps a full turn and the arrow darts down beside it."


@spec('clock_arrow_up')
def _(b):
    _clock_arrow(b, -1.0)
    return "The clock hand sweeps a full turn and the arrow darts up beside it."


def _loader(b, deg):
    """Ring plus filled wedge from 12 o'clock to deg. The ring part and the
    wedge part are the same source geometry under two clips that overlap
    only inside solid areas, so no edge is drawn twice at rest; the wedge
    clip sweeps."""
    isl = b.isl[0]
    subs = [b.subs[k] for k in isl.sub_ids]
    m = 4.0

    def P(r, a):
        a = math.radians(a - 90)
        return (12.0 + r * math.cos(a), 12.0 + r * math.sin(a))
    hole = [P(8.6, -m + (deg + 2 * m) * k / 48.0) for k in range(49)]
    hole += [P(7.95, deg + m + (360 - deg - 2 * m) * k / 48.0) for k in range(49)]
    src = b.part('ring', isl)
    ring_ = b.geo_part('ring_moving', subs)
    ring_.clip = Clip(lambda v: complement_d(hole), [])
    wedge = b.geo_part('wedge', subs)
    clip, p = clip_sweep(12.0, 12.0, 9.2, -m - 1.5, deg + 2 * m + 3.0, n=64)
    wedge.clip = clip
    p.to(0, 0.0, EFFECTS)
    p.to(220, 1.0, SPATIAL_SLOW)
    t_end = 220 + settle_ms(SPATIAL_SLOW, 1.0, 'p')
    # the two clipped copies are shown only while the wedge moves; at rest
    # the untouched source path is drawn
    src.alpha.snap(2, 0.0)
    src.alpha.snap(t_end, 1.0)
    for n in (ring_, wedge):
        n.alpha = Track(0.0, 'a')
        n.alpha.snap(2, 1.0)
        n.alpha.snap(t_end, 0.0)
    g = b.group('loader', [src, ring_, wedge], pivot=(12.0, 12.0))
    b.fixes_note = 'While moving, the wedge is drawn by two clipped copies of the same path.'
    press(g, 300, 0.95)


@spec('clock_loader_10')
def _(b):
    _loader(b, 45)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('clock_loader_20')
def _(b):
    _loader(b, 90)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('clock_loader_40')
def _(b):
    _loader(b, 135)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('clock_loader_60')
def _(b):
    _loader(b, 225)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('clock_loader_80')
def _(b):
    _loader(b, 270)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('clock_loader_90')
def _(b):
    _loader(b, 315)
    return "The loader empties and fills again clockwise up to its level, then gives a little squeeze."


@spec('close_fullscreen')
def _(b):
    a = b.part('bottom_left', b.I(0))
    c = b.part('top_right', b.I(1))
    dart(a, 0, 0.7, -0.7)
    dart(c, 0, -0.7, 0.7)
    return "Both arrows wind back and dart in toward the center, closing the full screen."


def _cc(b, frame, c_ids, t0=40):
    f = b.part('frame', b.I(frame))
    press(f, 0, 0.97)
    cs = [b.part('c%d' % k, b.I(i), pivot='b', parent=f) for k, i in enumerate(c_ids)]
    stagger(cs, t0, 90, hop, h=0.7, stretch=1.03)
    return f, cs


@spec('closed_caption')
def _(b):
    _cc(b, 0, [1, 2])
    return "The screen gives and the two Cs hop one after the other, like captions appearing."


@spec('closed_caption_add')
def _(b):
    _cc(b, 0, [3, 2])
    p = b.part('plus', b.I(1))
    plus_badge(p, 220)
    return "The two Cs hop one after the other and the plus contracts and springs back."


@spec('closed_caption_disabled')
def _(b):
    cc = b.part('captions', b.all())
    off, on, t = off_icon(b, 'closed_caption')
    press(cc, t, 0.95)
    return "The slash retracts, showing the captions on for a moment, and cuts across again; then the captions flinch."


@spec('closed_caption_display')
def _(b):
    f = b.part('frame', b.I(2))
    c0 = b.part('c0', b.I(0), pivot='b', parent=f)
    c1 = b.part('c1', b.I(1), pivot='b', parent=f)
    press(f, 0, 0.97)
    stagger([c0, c1], 40, 90, hop, h=0.6, stretch=1.03)
    disp = b.part('display', b.I(3))
    pop(disp, 200, 0.4)
    return "The Cs hop one after the other and the display pops in."


def _float(n, t=0, dy=-0.8):
    n.ty.to(t, dy, SPATIAL_SLOW)
    n.ty.back(t + 220, SPATIAL)
    return t + 600


@spec('cloud', 'cloud_queue')
def _(b):
    c = b.part('cloud', b.I(0))
    _float(c)
    swell(c, 60, 1.04, hold=160, spec_out=SPATIAL)
    return "The cloud drifts up, puffing a little, and settles back."


@spec('cloudy', 'cloudy_filled')
def _(b):
    c = b.part('cloud', b.I(0))
    c.tx.to(0, 0.8, SPATIAL_SLOW)
    c.tx.to(240, -0.4, SPATIAL_SLOW)
    c.tx.back(460, SPATIAL)
    return "The cloud drifts sideways with the wind and comes back to rest."


@spec('cloud_alert')
def _(b):
    c = b.part('cloud', b.I(0))
    bar = b.part('bar', b.I(2), pivot='b', parent=c)
    dot = b.part('dot', b.I(1), parent=c)
    c.tx.kick(0, -30.0, BOUNCY)
    pressxy(bar, 60, 1, 0.6, hold=80, spec_out=BOUNCY)
    pop(dot, 120, 0.0)
    return "The cloud shudders and its exclamation mark springs up, dot last."


@spec('cloud_circle')
def _(b):
    ring_ = b.part('ring', b.I(1))
    c = b.part('cloud', b.I(0), parent=ring_)
    press(ring_, 0, 0.96)
    c.tx.to(0, 1.0, SPATIAL_SLOW)
    c.tx.to(230, -0.6, SPATIAL_SLOW)
    c.tx.back(440, SPATIAL)
    return "The cloud drifts back and forth inside the circle."


@spec('cloud_done')
def _(b):
    c = b.part('cloud', b.I(1))
    k = b.part('check', b.I(0), parent=c)
    _float(c, 0, -0.6)
    check_draw(b, k, 60, pop_s=1.12)
    return "The cloud lifts and the check inside is drawn again, popping at the end."


@spec('cloud_lock')
def _(b):
    c = b.part('cloud', b.I(0))
    lk = b.part('lock', b.I(1), pivot='b')
    _float(c, 0, -0.6)
    lk.ty.to(60, -0.7, SPATIAL_FAST)
    lk.ty.back(140, BOUNCY)
    wobble(lk, 200, 300.0)
    return "The cloud lifts and the lock clicks shut with a jolt."


@spec('cloud_off')
def _(b):
    a = b.part('rest', b.I(1))
    s = b.part('slashed', b.I(0))
    off, on, t = off_icon(b, 'cloud')
    a.ty.to(t, -0.5, SPATIAL)
    a.ty.back(t + 100, BOUNCY)
    return "The slash retracts, showing the cloud whole for a moment, and cuts across again; then the cloud flinches."


@spec('cloud_sync')
def _(b):
    arc = b.part('arc', b.I(0), pivot=(12.0, 12.0))
    head = b.part('arrow', b.I(2))
    c = b.part('cloud', b.I(1), pivot='r')
    nod(arc, 0, -14, hold=110)
    dart(head, 40, 0.5, -0.5)
    press(c, 80, 0.9, hold=110)
    return "The sync arrows swing around and the little cloud squeezes as it syncs."


@spec('cloudy_snowing')
def _(b):
    c = b.part('cloud', b.I(5))
    _float(c, 0, -0.5)
    flakes = [b.part('f%d' % k, b.I(i)) for k, i in enumerate([0, 3, 1, 2, 4])]
    for k, n in enumerate(flakes):
        t = 40 + k * 55
        n.ty.to(t, 0.9, SPATIAL_SLOW)
        n.alpha.to(t, 0.0, EFFECTS_SLOW)
        n.ty.snap(t + 230, -0.9)
        n.ty.to(t + 232, 0.0, SPATIAL_SLOW)
        n.alpha.to(t + 232, 1.0, EFFECTS_SLOW)
    return "The snowflakes fall out of sight one after another and new ones drift in from the cloud."


@spec('co2')
def _(b):
    c = b.part('c', b.I(2), pivot='b')
    o = b.part('o', b.I(0), pivot='b')
    two = b.part('two', b.I(1), pivot='b')
    stagger([c, o], 0, 80, hop, h=0.8, stretch=1.03)
    hop(two, 170, 0.6, stretch=1.03)
    return "The letters hop one after another and the small 2 follows with a bounce."


@spec('code')
def _(b):
    l = b.part('left', b.I(0))
    r = b.part('right', b.I(1))
    dart(l, 0, -0.9, 0)
    dart(r, 0, 0.9, 0)
    return "The two brackets wind in and push outward, then spring back."


@spec('code_blocks')
def _(b):
    f = b.part('frame', b.I(2))
    l = b.part('left', b.I(0), parent=f)
    r = b.part('right', b.I(1), parent=f)
    press(f, 0, 0.96)
    dart(l, 30, -0.8, 0)
    dart(r, 30, 0.8, 0)
    return "The block gives and the brackets inside push outward, then spring back."


@spec('code_off')
def _(b):
    s = b.part('slashed', b.I(0))
    r = b.part('right', b.I(1))
    off, on, t = off_icon(b, 'code')
    dart(r, t, 0.6, 0)
    return "The slash retracts, showing the code brackets whole for a moment, and cuts across again; then the bracket flinches."


@spec('code_xml')
def _(b):
    l = b.part('left', b.I(0))
    s = b.part('slash', b.I(1))
    r = b.part('right', b.I(2))
    dart(l, 0, -0.8, 0)
    dart(r, 0, 0.8, 0)
    nod(s, 60, 12, hold=90)
    return "The brackets push outward and the slash between them tips and springs back."


@spec('coffee')
def _(b):
    cup = b.part('cup', b.I(0), pivot='b')
    saucer = b.part('saucer', b.I(1), pivot='b')
    cup.ty.to(0, -0.9, SPATIAL)
    cup.rot.to(0, -4, SPATIAL)
    cup.ty.to(150, 0.0, (700.0, 0.9))
    cup.rot.to(150, 0.0, SPATIAL)
    squash(cup, 230, 0.05)
    squash(saucer, 230, 0.25)
    return "The cup is lifted for a sip and set back down on its saucer."
