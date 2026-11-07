# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Second pass on icons 621-1020: richer specs for the icons whose first
# version was too plain. They use the techniques of the older icons: arrows
# that wind back squashing along their direction and dart stretching, heads
# that fly on an elastic shaft, shapes cut into pieces, parts that leave and
# come back from the other side.

from lib import *  # noqa: F401,F403


def room(n, angle, want, edge=23.8):
    """Largest dart distance (up to want) that keeps n inside the box."""
    x0, y0, x1, y1 = n.bb
    ux, uy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    lim = want
    if ux > 0.1:
        lim = min(lim, (edge - x1) / ux)
    if ux < -0.1:
        lim = min(lim, (x0 - (24 - edge)) / -ux)
    if uy > 0.1:
        lim = min(lim, (edge - y1) / uy)
    if uy < -0.1:
        lim = min(lim, (y0 - (24 - edge)) / -uy)
    return max(0.3, lim * 0.8)


# ---------------------------------------------------------------- call arrows

def _diag_arrow(b, island, head_tri, tail, angle, L, dist=1.7, concept=''):
    grp, p = b.split('arrow', b.I(island), [('head', head_tri, 'c')])
    shaft = p['arrow_rest']
    shaft.pivot = tail
    elastic(p['head'], shaft, 0, angle, L, dist=dist, wind=0.6)
    # the whole arrow gives a last nudge in its direction
    ux, uy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    grp.tx.kick(330, 12.0 * ux, BOUNCY)
    grp.ty.kick(330, 12.0 * uy, BOUNCY)
    return concept


@spec('call_made')
def _(b):
    return _diag_arrow(b, 0, [(8.5, 4.6), (19.4, 4.6), (19.4, 15.5)], (4.9, 19.1), -45, 12.8, dist=2.3, concept=
                       "The arrowhead winds back down the line and shoots out to the corner, its shaft "
                       "stretching like a rubber band, then snaps home.")


@spec('call_received')
def _(b):
    return _diag_arrow(b, 0, [(4.6, 8.6), (4.6, 19.4), (15.4, 19.4)], (18.9, 5.1), 135, 12.6, dist=2.3, concept=
                       "The arrowhead winds back up the line and shoots down into the corner, its shaft "
                       "stretching like a rubber band, then snaps home.")


def _missed(b, mirror):
    def X(x):
        return 24.0 - x if mirror else x
    head = [(X(2.6), 6.6), (X(13.4), 6.6), (X(2.6), 17.4)]
    arm = [(X(7.76), 8.24), (X(4.64), 11.36), (X(9.64), 16.36), (X(12.76), 13.24)]
    grp, p = b.split('arrow', b.I(0), [('head', head, 'c'), ('arm', arm, (X(11.2), 14.8))])
    angle = -45 if mirror else -135
    # the V dips first, as if the call fell through
    grp.pivot = (12.0, 16.6)
    grp.ty.to(0, 1.1, SPATIAL)
    grp.sy.to(0, 0.88, SPATIAL)
    grp.ty.back(120, BOUNCY)
    grp.sy.back(120, BOUNCY)
    elastic(p['head'], p['arm'], 140, angle, 7.07, dist=1.6, wind=0.4)


@spec('call_missed')
def _(b):
    _missed(b, False)
    return ("The line drops into its V and bounces back up; then the arrowhead shoots up to the left "
            "on a stretching arm and snaps home.")


@spec('call_missed_outgoing')
def _(b):
    _missed(b, True)
    return ("The line drops into its V and bounces back up; then the arrowhead shoots up to the right "
            "on a stretching arm and snaps home.")


@spec('call_split')
def _(b):
    head = [(3.6, 3.6), (11.0, 3.6), (3.6, 11.0)]
    arm = [(8.71, 5.89), (5.89, 8.71), (9.59, 12.41), (12.41, 9.59)]
    grp, p = b.split('left', b.I(0), [('head', head, 'c'), ('arm', arm, (11.0, 11.0))])
    stem = p['left_rest']
    stem.pivot = (12.0, 20.0)
    right = b.part('right', b.I(1))
    pressxy(stem, 0, 1, 0.9, hold=80)
    elastic(p['head'], p['arm'], 80, -135, 5.23, dist=1.5, wind=0.4)
    shoot(right, 140, -45, dist=1.4)
    return ("The stem crouches, then the line splits: the left head shoots out on a stretching arm "
            "and the right arrow darts off the other way, both snapping home.")


@spec('call_merge')
def _(b):
    grp, p = b.split('line', b.I(0), [('head', R(7.2, 3.2, 16.8, 9.25), 'c'),
                                      ('shaft', R(10.8, 9.25, 13.2, 13.0), (12.0, 13.0))])
    stub = b.part('branch', b.I(1))
    shift(stub, 0, dx=-1.2, dy=-1.2, hold=90, spec_out=BOUNCY)
    elastic(p['head'], p['shaft'], 110, -90, 3.75, dist=1.6, wind=0.4)
    return ("The side branch slides up into the line; at the merge the arrowhead shoots up on a "
            "stretching shaft and snaps home.")


# ---------------------------------------------------------------- chevrons

@spec('chevron_backward', 'chevron_left')
def _(b):
    c = b.part('chevron', b.I(0))
    shoot(c, 0, 180, dist=2.2, wind=0.7)
    shoot(c, 420, 180, dist=0.9, wind=0.2)
    return "The chevron winds up squashing, darts left with a stretch, springs home and nudges left once more."


@spec('chevron_forward', 'chevron_right')
def _(b):
    c = b.part('chevron', b.I(0))
    shoot(c, 0, 0, dist=2.2, wind=0.7)
    shoot(c, 420, 0, dist=0.9, wind=0.2)
    return "The chevron winds up squashing, darts right with a stretch, springs home and nudges right once more."


@spec('chevron_line_up')
def _(b):
    line = b.part('line', b.I(0))
    c = b.part('chevron', b.I(1))
    shoot(c, 0, -90, dist=2.8, wind=0.8)
    pressxy(line, 120, 1.08, 0.5, hold=50, spec_out=BOUNCY)
    line.ty.kick(120, -40.0, BOUNCY)
    return "The chevron crouches and shoots up into the line, which squashes and bounces with the hit."


@spec('chip_extraction')
def _(b):
    chip = b.part('chip', b.I(0), pivot='l')
    grp, p = b.split('arrow', b.I(1), [('head', R(14.6, 7.0, 21.0, 17.0), 'c')])
    shaft = p['arrow_rest']
    shaft.pivot = (9.0, 12.0)
    elastic(p['head'], shaft, 0, 0, 5.6, dist=1.6, wind=0.8)
    pressxy(chip, 0, 0.85, 1.04, hold=95, spec_out=BOUNCY)
    return ("The arrow is pulled back into the chip, which flexes, then shoots out with its shaft "
            "stretching like a rubber band and snaps home.")


# ---------------------------------------------------------------- car climate

def _car(b, head, body, seat, waves=(), shield=None, arrows=(), t_air=60):
    s = b.part('seat', b.I(seat), pivot='b')
    bd = b.part('body', b.I(body))
    back_left = s.bb[0] + s.bb[2] < bd.bb[0] + bd.bb[2]
    sign = -1 if back_left else 1
    bd.pivot = (bd.bb[0] if back_left else bd.bb[2], bd.bb[3])
    hd = b.part('head', b.I(head), parent=bd)
    if shield is not None:
        sh = b.part('shield', b.I(shield), pivot='t')
        pressxy(sh, 0, 1.04, 0.9, hold=120, spec_out=BOUNCY)
    for k, i in enumerate(waves):
        w = b.part('wave%d' % k, b.I(i), pivot='b')
        redraw(b, w, 20 + k * 80, -90, erase_ms=90)
        w.ty.to(20 + k * 80, -0.7, SPATIAL_SLOW)
        w.ty.back(240 + k * 80, BOUNCY)
    dirs = {'left': 180, 'right': 0, 'down': 90}
    for k, (i, d) in enumerate(arrows):
        a = b.part('air_%s' % d, b.I(i))
        ang = dirs[d]
        t = t_air + k * 80
        shoot(a, t, ang, dist=room(a, ang, 1.4), wind=0.5)
        shoot(a, t + 300, ang, dist=room(a, ang, 0.8), wind=0.2)
    # the passenger is pushed back into the seat and settles
    t = t_air + 110
    bd.rot.to(t, 7 * sign, SPATIAL)
    bd.rot.back(t + 150, BOUNCY)
    hd.tx.to(t + 30, 0.6 * sign, SPATIAL)
    hd.tx.back(t + 180, BOUNCY)
    squash(s, t + 40, 0.06)


@spec('car_defrost_left', 'car_defrost_right')
def _(b):
    _car(b, 5, 3, 4, waves=[1, 0], shield=2, t_air=200)
    return ("The windshield flexes and the heat waves rise off it one after another; the warmth "
            "reaches the passenger, who sinks back into the seat and settles.")


@spec('car_defrost_low_left', 'car_defrost_low_right')
def _(b):
    _car(b, 2, 0, 1, waves=[5, 4], shield=6, arrows=[(3, 'down')], t_air=120)
    return ("The heat waves rise off the windshield, the air arrow gusts down to the feet twice and "
            "the passenger sinks back into the seat.")


@spec('car_defrost_mid_left', 'car_defrost_mid_low_left')
def _(b):
    _car(b, 3, 1, 2, waves=[5, 4], shield=6, arrows=[(0, 'left')], t_air=120)
    return ("The heat waves rise off the windshield, the air arrow gusts toward the passenger twice "
            "and pushes them back into the seat.")


@spec('car_defrost_mid_right')
def _(b):
    _car(b, 3, 1, 2, waves=[5, 4], shield=6, arrows=[(0, 'right')], t_air=120)
    return ("The heat waves rise off the windshield, the air arrow gusts toward the passenger twice "
            "and pushes them back into the seat.")


@spec('car_defrost_mid_low_right')
def _(b):
    _car(b, 4, 2, 3, waves=[6, 5], shield=7, arrows=[(0, 'right'), (1, 'down')], t_air=120)
    return ("The heat waves rise off the windshield, the air arrows gust at the body and the feet in "
            "turn, and the passenger sinks back into the seat.")


@spec('car_fan_low_left', 'car_fan_low_right')
def _(b):
    _car(b, 0, 1, 3, arrows=[(2, 'down')], t_air=0)
    return "The air arrow gusts down to the feet twice and the passenger sinks back into the seat."


@spec('car_fan_mid_left')
def _(b):
    _car(b, 1, 2, 3, arrows=[(0, 'left')], t_air=0)
    return "The air arrow gusts at the passenger twice, pushing them back into the seat."


@spec('car_fan_mid_right')
def _(b):
    _car(b, 1, 2, 3, arrows=[(0, 'right')], t_air=0)
    return "The air arrow gusts at the passenger twice, pushing them back into the seat."


@spec('car_fan_low_mid_left')
def _(b):
    _car(b, 2, 3, 4, arrows=[(0, 'left'), (1, 'down')], t_air=0)
    return ("The air arrows gust at the body and the feet in turn, and the passenger sinks back "
            "into the seat.")


@spec('car_fan_mid_low_right')
def _(b):
    _car(b, 2, 3, 4, arrows=[(0, 'right'), (1, 'down')], t_air=0)
    return ("The air arrows gust at the body and the feet in turn, and the passenger sinks back "
            "into the seat.")


@spec('car_fan_recirculate')
def _(b):
    car = b.part('car', b.I(2), pivot='b')
    arrow = b.part('arrow', b.I(0))
    hook = b.part('hook', b.I(1))
    w = b.group('arrow_wrap', [arrow])
    clip, lo, hi = clip_band((0.6, 3.6, 17.4, 15.4), 180, margin=0.0)
    w.clip = clip
    lo.to(0, 1.0, EFFECTS_FAST)
    lo.snap(100, 0.0)
    hi.snap(100, 0.0)
    hi.to(102, 1.0, SPATIAL)
    shoot(arrow, 330, 180, dist=room(arrow, 180, 1.0), wind=0.4)
    shoot(hook, 60, 0, dist=0.8, wind=0.3)
    car.tx.kick(380, -25.0, BOUNCY)
    squash(car, 380, 0.06)
    return ("The air is pulled back in: the hook flicks, the arrow is drawn again from right to left "
            "and darts left, and the car rocks with the draught.")


@spec('car_fan_recirculate_2')
def _(b):
    car = b.part('car', b.I(1), pivot='b')
    a = b.part('arrow', b.I(0), pivot=(11.0, 11.0))
    a.rot.to(0, 40, SPATIAL)
    a.rot.to(140, -25, SPATIAL_FAST)
    a.rot.back(260, BOUNCY)
    press(a, 0, 0.8, hold=140, spec_out=BOUNCY)
    pressxy(car, 160, 1.0, 0.9, hold=70, spec_out=BOUNCY)
    return ("The U-turn arrow winds back around its loop, whips the other way and springs home; "
            "the car bounces on its wheels.")


@spec('car_seat_off')
def _(b):
    seat = b.part('person', b.all())
    # Material Symbols has no "car_seat" icon: the on layer is drawn here, a
    # seated person in the same place (head circle, torso and thigh), shown
    # only inside the slash corridor while the slash moves.
    on = circle_path(8.0, 5.0, 2.0) + rounded_path(
        [(5.45, 7.6), (8.85, 7.6), (9.95, 13.0), (15.6, 13.0), (16.2, 18.0), (7.6, 18.0), (6.1, 11.0)], 1.0)
    off, onl, t = off_icon(b, None, on_subs=on, on_note=(
        'While moving, the slash is retracted over a seated person drawn for this icon '
        '(the set has no car_seat icon).'))
    seat.pivot = (12.0, 18.0)
    squash(seat, t, 0.12)
    seat.tx.kick(t + 60, -30.0, (900.0, 0.3))
    return ("The slash retracts, showing the seated passenger whole for a moment, and cuts across "
            "again; then the seat slumps and shudders.")


# ---------------------------------------------------------------- calendars

@spec('calendar_view_day')
def _(b):
    card = b.part('card', b.I(0))
    top = b.part('top', b.I(1))
    bot = b.part('bottom', b.I(2))
    card.sy.to(0, 0.08, SPATIAL)
    card.sx.to(0, 1.05, SPATIAL)
    card.sy.to(130, 1.0, BOUNCY)
    card.sx.to(130, 1.0, BOUNCY)
    for n, d in ((top, -1.4), (bot, 1.4)):
        n.ty.to(20, d, SPATIAL_FAST)
        n.ty.back(150, BOUNCY)
        n.sy.to(210, 0.5, SPATIAL_FAST)
        n.sy.back(260, BOUNCY)
    return ("The day card flips over to the next day; the bars above and below are thrown off and "
            "snap back, squashing as they land.")


@spec('calendar_view_month')
def _(b):
    g = b.part('grid', b.I(0))
    cells = [b.hole('cell%d' % k, g, b.isl[0], k) for k in range(6)]
    order = [(0, 0), (1, 1), (3, 1), (2, 2), (4, 2), (5, 3)]
    for k, step in order:
        c = cells[k]
        t = step * 60
        c.sx.to(t, 0.0, EFFECTS_FAST)
        c.sy.to(t, 0.0, EFFECTS_FAST)
        c.sx.back(t + 260, BOUNCY)
        c.sy.back(t + 260, BOUNCY)
    press(g, 160, 0.95, hold=120)
    return ("The days fill in diagonally from the top left like a month being marked off, then "
            "open again in the same order with a bounce.")


@spec('calendar_view_week')
def _(b):
    g = b.part('grid', b.I(0))
    cols = [b.hole('day%d' % k, g, b.isl[0], k, pivot='t') for k in range(4)]
    for k, n in enumerate([cols[2], cols[1], cols[0], cols[3]]):
        t = k * 70
        n.sy.to(t, 0.0, SPATIAL)
        n.sy.back(t + 260, BOUNCY)
    pressxy(g, 280, 1.0, 0.94, hold=80)
    return ("The days of the week fill up from the bottom one after another, left to right, then "
            "empty again with a bounce.")


# ---------------------------------------------------------------- misc C

@spec('bullet_chart')
def _(b):
    grp, p = b.split('chart', b.I(0), [
        ('bar_l', R(3.9, 8.8, 10.6, 15.2), (4.0, 12.0)),
        ('bar_r', R(13.4, 8.8, 16.6, 15.2), (4.0, 12.0)),
    ])
    for k in ('bar_l', 'bar_r'):
        n = p[k]
        n.sx.to(0, 0.05, EFFECTS_FAST)
        n.sx.to(110, 1.0, (500.0, 0.5))
    grp.pivot = (12.0, 12.0)
    pressxy(grp, 170, 1.0, 0.94, hold=60, spec_out=BOUNCY)
    return ("The bar snaps back to the left edge and shoots out again past the target line, "
            "overshooting; the chart flinches as it is crossed.")


@spec('cable')
def _(b):
    grp, p = b.split('cable', b.I(0), [
        ('plug_r', R(16.3, 1.5, 21.7, 15.0), (19.0, 15.0)),
        ('plug_l', R(2.3, 6.0, 7.2, 21.7), (4.75, 6.0)),
    ])
    r, l, mid = p['plug_r'], p['plug_l'], p['cable_rest']
    r.sy.to(0, 1.1, SPATIAL)
    r.sy.to(140, 0.88, SPATIAL_FAST)
    r.sy.back(210, BOUNCY)
    l.sy.to(220, 1.06, SPATIAL_FAST)
    l.sy.back(290, BOUNCY)
    return ("The plug is pulled up on its stretchy cable and slammed back into its socket; the jolt "
            "runs down the cable to the other plug.")


@spec('cable_car')
def _(b):
    grp, p = b.split('car', b.I(0), [('roof', R(2.4, 1.4, 21.6, 5.6), (12.0, 5.6))])
    dot = b.part('light', b.I(1))
    whole = b.group('cabin', [grp, dot], pivot=(12.0, 21.0))
    whole.ty.to(0, -0.9, SPATIAL)
    whole.ty.to(150, 0.0, (700.0, 0.9))
    squash(whole, 220, 0.07)
    p['roof'].ty.to(60, -0.5, SPATIAL)
    p['roof'].ty.back(200, BOUNCY)
    whole.rot.kick(240, 120.0, BOUNCY)
    dot.ty.kick(240, 40.0, BOUNCY)
    return ("The cable car rides over a bump: it lifts, the roof lags behind, and it lands with a "
            "rattle that bounces the light inside.")


@spec('camera_roll')
def _(b):
    grp, p = b.split('roll', b.I(0), [('strip', R(11.2, 4.5, 21.6, 19.5), (11.2, 12.0))])
    strip = p['strip']
    holes = b.group('holes', [b.part('hole%d' % k, b.I(i)) for k, i in enumerate([1, 2, 3, 4, 5, 6])],
                    pivot=(11.2, 12.0))
    can = p['roll_rest']
    can.pivot = (6.0, 12.0)
    for n in (strip, holes):
        n.sx.to(0, 1.16, SPATIAL)
        n.sx.to(160, 0.9, SPATIAL_FAST)
        n.sx.back(250, BOUNCY)
    pressxy(can, 160, 0.94, 1.03, hold=50, spec_out=BOUNCY)
    return ("The film is pulled out of its canister, then rewinds back in with a snap that makes the "
            "can flinch; the sprocket holes ride along.")


@spec('campaign')
def _(b):
    horn = b.part('megaphone', b.I(3), pivot=(4.0, 15.0))
    mouth = b.part('flare', b.I(4), pivot='l')
    horn.tx.to(0, -1.0, SPATIAL_FAST)
    horn.rot.to(0, -8, SPATIAL_FAST)
    horn.tx.back(100, BOUNCY)
    horn.rot.back(100, BOUNCY)
    mouth.tx.to(0, -1.0, SPATIAL_FAST)
    mouth.tx.back(100, BOUNCY)
    pressxy(mouth, 60, 1.6, 1.15, hold=90, spec_out=BOUNCY)
    for k, (i, ang) in enumerate([(2, -40), (0, 0), (1, 40)]):
        n = b.part('line%d' % k, b.I(i))
        t = 90 + k * 50
        n.axis = float(ang)
        n.sx.to(t - 60, 0.0, EFFECTS_FAST)
        n.sy.to(t - 60, 0.0, EFFECTS_FAST)
        n.sx.to(t, 1.0, BOUNCY)
        n.sy.to(t, 1.0, BOUNCY)
        ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        n.tx.to(t, ux * 0.9, SPATIAL_FAST)
        n.ty.to(t, uy * 0.9, SPATIAL_FAST)
        n.tx.back(t + 120, BOUNCY)
        n.ty.back(t + 120, BOUNCY)
    return ("The megaphone kicks back as it shouts, its bell flares, and the sound lines burst out "
            "of it one after another.")


@spec('camping')
def _(b):
    grp, p = b.split('tent', b.I(0), [
        ('door', [(8.0, 19.7), (12.0, 12.9), (16.0, 19.7)], (12.0, 19.7)),
        ('poles', R(10.4, 1.4, 13.6, 4.8), (12.0, 4.8)),
    ])
    grp.pivot = (12.0, 22.0)
    pressxy(grp, 0, 1.06, 0.86, hold=110, spec_out=BOUNCY)
    p['door'].sx.to(60, 1.6, SPATIAL)
    p['door'].sx.to(200, 0.75, SPATIAL)
    p['door'].sx.back(320, BOUNCY)
    p['poles'].rot.kick(80, 900.0, (700.0, 0.25))
    return ("A gust hits the tent: it squashes, the door flap billows open and shut, and the pole "
            "tips wobble before everything settles.")


def _cross(b, isl, cx, cy, half, t=0):
    """Close/cancel x: both strokes are slashed in again one after the other
    and the x lands with a punch. Returns the group."""
    w = 1.75
    e = half + 1.0

    def band(ax, ay, bx, by):
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * w, dx / L * w
        return [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)]
    s1 = band(cx - e, cy - e, cx + e, cy + e)
    s2 = band(cx + e, cy - e, cx - e, cy + e)
    grp, p = b.split('x', isl, [('stroke1', s1, (cx, cy)), ('stroke2', s2, (cx, cy))], grow=0.0, rest=False)
    grp.pivot = (cx, cy)
    box = (cx - half - 0.6, cy - half - 0.6, cx + half + 0.6, cy + half + 0.6)
    for k, (name, ang) in enumerate((('stroke1', 45), ('stroke2', 135))):
        wr = b.group(name + '_w', [p[name]], parent=grp)
        clip, lo, hi = clip_band(box, ang, margin=0.0)
        wr.clip = clip
        lo.to(t, 1.0, EFFECTS_FAST)
        ts = t + 90 + k * 110
        lo.snap(ts, 0.0)
        hi.snap(ts, 0.0)
        hi.to(ts + 2, 1.0, (900.0, 0.85))
    tp = t + 330
    grp.sx.to(tp, 1.22, SPATIAL_FAST)
    grp.sy.to(tp, 1.22, SPATIAL_FAST)
    grp.sx.to(tp + 60, 0.88, SPATIAL_FAST)
    grp.sy.to(tp + 60, 0.88, SPATIAL_FAST)
    grp.sx.back(tp + 120, BOUNCY)
    grp.sy.back(tp + 120, BOUNCY)
    return grp, tp


@spec('close')
def _(b):
    _cross(b, b.I(0), 12.0, 12.0, 6.6)
    return ("The x is struck out again: one stroke slashes in, then the other, and it lands with a "
            "punch.")


@spec('close_small')
def _(b):
    _cross(b, b.I(0), 12.0, 12.05, 4.6)
    return ("The x is struck out again: one stroke slashes in, then the other, and it lands with a "
            "punch.")


@spec('cancel')
def _(b):
    ring_ = b.part('circle', b.I(1))
    g, tp = _cross(b, b.I(0), 12.0, 12.0, 4.6)
    press(ring_, tp + 40, 0.88, hold=60, spec_out=BOUNCY)
    return ("The x inside is struck out again stroke by stroke and lands with a punch that makes "
            "the circle flinch.")


@spec('cancel_presentation')
def _(b):
    scr = b.part('screen', b.I(1))
    g, tp = _cross(b, b.I(0), 12.0, 12.0, 3.6)
    press(scr, tp + 40, 0.9, hold=60, spec_out=BOUNCY)
    return ("The x on the screen is struck out again stroke by stroke and lands with a punch that "
            "makes the screen flinch.")


@spec('captive_portal')
def _(b):
    globe = b.part('globe', b.I(1))
    cur = b.part('cursor', b.I(0))
    shoot(cur, 0, -135, dist=1.6, wind=0.7)
    press(globe, 120, 0.86, hold=70, spec_out=BOUNCY)
    globe.rot.kick(160, -250.0, BOUNCY)
    return ("The cursor winds back and shoots at the globe, which gives under the click and wobbles.")


@spec('capture')
def _(b):
    f = b.part('frame', b.I(0))
    inner = b.part('inner', b.I(1), parent=f)
    inner.sy.to(0, 0.02, EFFECTS_FAST)
    inner.sx.to(0, 1.08, EFFECTS_FAST)
    press(f, 0, 0.9, hold=80, spec_out=BOUNCY)
    inner.sy.to(110, 1.0, BOUNCY)
    inner.sx.to(110, 1.0, BOUNCY)
    swell(inner, 330, 1.07, hold=60)
    return ("The shutter slams shut to a slit with a flash of the frame, then snaps open with a "
            "bounce and a little afterglow.")


@spec('cardio_load')
def _(b):
    h = b.part('heart', b.I(0), pivot=(12.0, 12.0))
    band = b.hole('band', h, b.isl[0], 1)
    tip = b.hole('tip', h, b.isl[0], 2, pivot='t')
    for k, t in enumerate((0, 260)):
        h.sx.to(t, 0.8, SPATIAL_FAST)
        h.sy.to(t, 0.8, SPATIAL_FAST)
        h.sx.to(t + 70, 1.08 - k * 0.03, SPATIAL_FAST)
        h.sy.to(t + 70, 1.08 - k * 0.03, SPATIAL_FAST)
        h.sx.back(t + 150, BOUNCY)
        h.sy.back(t + 150, BOUNCY)
    for k, n in enumerate((tip, band)):
        n.sx.to(60 + k * 260, 0.0, EFFECTS_FAST)
        n.sy.to(60 + k * 260, 0.0, EFFECTS_FAST)
        n.sx.back(420 + k * 60, BOUNCY)
        n.sy.back(420 + k * 60, BOUNCY)
    return ("The heart beats hard twice and its load bars fill in from the bottom, one with each "
            "beat, then clear again.")


@spec('cards_stack')
def _(b):
    front = b.part('front', b.I(0), pivot=(6.0, 16.0))
    b.part('line0', b.I(1), parent=front)
    b.part('line1', b.I(2), parent=front)
    back = b.part('back', b.I(3), pivot='bl')
    front.tx.to(0, 1.0, SPATIAL)
    front.ty.to(0, -1.1, SPATIAL)
    front.rot.to(0, -6, SPATIAL)
    back.tx.to(80, 0.9, SPATIAL)
    back.ty.to(80, -0.9, SPATIAL)
    front.tx.back(220, BOUNCY)
    front.ty.back(220, BOUNCY)
    front.rot.back(220, BOUNCY)
    back.tx.back(250, BOUNCY)
    back.ty.back(250, BOUNCY)
    squash(front, 330, 0.05)
    return ("The top card is flicked off the stack with a tilt, the card behind slides up into its "
            "place, then the top card lands back on it with a squash.")


@spec('cases')
def _(b):
    front = b.part('front', b.I(1), pivot=(14.0, 1.0))
    back = b.part('back', b.I(0), pivot='bl')
    drop = b.group('drop', [front], pivot=(14.0, 18.0))
    front.ty.to(0, -0.75, SPATIAL)
    front.rot.to(60, 7, SPATIAL)
    front.rot.to(170, -5, SPATIAL)
    front.rot.back(280, BOUNCY)
    front.ty.to(260, 0.0, (900.0, 0.9))
    squash(drop, 320, 0.1)
    back.tx.kick(330, -25.0, BOUNCY)
    back.ty.kick(330, 20.0, BOUNCY)
    return ("The front case is hoisted by its handle, swings back and forth and is dropped on the "
            "one behind, which gets bumped.")


@spec('child_care')
def _(b):
    face = b.part('face', b.I(3), pivot=(12.0, 21.0))
    l = b.part('eye_l', b.I(1), parent=face)
    r = b.part('eye_r', b.I(0), parent=face)
    smile = b.part('smile', b.I(2), parent=face, pivot='t')
    for n in (l, r):
        n.sy.to(0, 0.1, SPATIAL_FAST)
        n.sy.back(380, BOUNCY)
    smile.sx.to(0, 1.2, SPATIAL)
    smile.sy.to(0, 1.3, SPATIAL)
    smile.sx.back(380, BOUNCY)
    smile.sy.back(380, BOUNCY)
    for k in range(2):
        t = 40 + k * 170
        face.ty.to(t, -0.6, SPATIAL_FAST)
        face.ty.to(t + 80, 0.0, SPATIAL_FAST)
        face.rot.to(t, 6 * (1 - 2 * k), SPATIAL_FAST)
    face.ty.back(380, BOUNCY)
    face.rot.back(380, BOUNCY)
    return ("The baby giggles: its eyes squeeze shut, its smile opens wide and it bounces twice, "
            "wiggling, before settling.")


@spec('child_friendly')
def _(b):
    body = b.part('stroller', b.I(3), pivot=(18.0, 20.0))
    hood = b.part('hood', b.I(2), pivot=(10.0, 7.0), parent=body)
    w0 = b.part('wheel0', b.I(0), pivot='b')
    w1 = b.part('wheel1', b.I(1), pivot='b')
    pram = b.group('pram', [body, w0, w1], pivot='b')
    pram.tx.to(0, 1.3, SPATIAL)
    body.rot.to(0, -7, SPATIAL)
    hood.rot.to(40, -12, SPATIAL)
    pram.tx.back(180, BOUNCY)
    body.rot.back(180, BOUNCY)
    hood.rot.back(220, BOUNCY)
    for w in (w0, w1):
        pressxy(w, 180, 1.15, 0.75, hold=50, spec_out=BOUNCY)
    return ("The stroller is pushed: it rolls forward tipping back on its wheels, the hood bobs, "
            "and it rolls back and lands on its wheels.")


@spec('child_hat')
def _(b):
    face = b.part('face', b.I(3), pivot=(12.0, 22.0))
    hat = b.part('hat', b.I(4), pivot=(4.0, 10.0))
    l = b.part('eye_l', b.I(1), parent=face)
    r = b.part('eye_r', b.I(2), parent=face)
    smile = b.part('smile', b.I(0), parent=face, pivot='t')
    hat.rot.to(0, -8, SPATIAL)
    hat.rot.back(200, BOUNCY)
    face.ty.to(40, -0.5, SPATIAL_FAST)
    face.ty.back(150, BOUNCY)
    for n in (l, r):
        pressxy(n, 120, 1, 0.1, hold=70, spec_out=SPATIAL_FAST)
    pressxy(smile, 120, 1.25, 1.45, hold=160, spec_out=BOUNCY)
    return ("The child tips its cap up with a hop, blinks and breaks into a wide smile; the cap "
            "drops back into place.")


@spec('chrome_maximize')
def _(b):
    w = b.part('window', b.I(0))
    w.sx.to(0, 0.88, SPATIAL)
    w.sy.to(0, 0.88, SPATIAL)
    w.sx.to(100, 1.32, SPATIAL_FAST)
    w.sy.to(140, 1.32, SPATIAL_FAST)
    w.sx.back(240, BOUNCY)
    w.sy.back(270, BOUNCY)
    return ("The window gathers itself, then snaps out to fill the screen, first in width and then "
            "in height, and settles back with a bounce.")


@spec('chrome_tote')
def _(b):
    front = b.part('front', b.I(2))
    arrow = b.part('arrow', b.I(0), parent=front)
    back = b.part('back', b.I(1))
    shoot(arrow, 0, 90, dist=room(arrow, 90, 1.2), wind=0.6)
    front.ty.to(110, 0.7, SPATIAL_FAST)
    front.ty.back(170, BOUNCY)
    back.tx.to(130, -0.7, SPATIAL_FAST)
    back.ty.to(130, 0.7, SPATIAL_FAST)
    back.tx.back(200, BOUNCY)
    back.ty.back(200, BOUNCY)
    return ("The arrow winds up and drops into the front card, which is knocked down onto the one "
            "behind; both bounce back.")


@spec('chromecast_2')
def _(b):
    grp, p = b.split('dongle', b.I(0), [
        ('puck', R(1.5, 7.4, 16.5, 21.5), (9.0, 7.4)),
        ('plug', [(20.75, 7.94), (24.69, 11.02), (20.99, 15.74), (17.05, 12.66)], (19.5, 11.5)),
    ])
    plug, puck = p['plug'], p['puck']
    plug.tx.to(0, 0.7, SPATIAL_FAST)
    plug.ty.to(0, 0.55, SPATIAL_FAST)
    plug.tx.back(90, BOUNCY)
    plug.ty.back(90, BOUNCY)
    puck.rot.to(60, 12, SPATIAL)
    puck.rot.to(200, -8, SPATIAL)
    puck.rot.back(330, BOUNCY)
    return ("The plug clicks into its socket and the puck swings on its cable like a pendulum before "
            "coming to rest.")


@spec('cinematic_blur')
def _(b):
    grp, p = b.split('board', b.I(0), [('clapper', R(1.5, 2.4, 22.5, 8.6), (2.2, 8.6))])
    head = b.part('head', b.I(2))
    body = b.part('body', b.I(1))
    person = b.group('subject', [head, body], pivot=(12.0, 14.0))
    cl = p['clapper']
    cl.rot.to(0, -6, SPATIAL)
    cl.rot.to(150, 0.0, (1200.0, 0.5))
    pressxy(p['board_rest'], 170, 1.03, 0.94, hold=50)
    person.sx.to(0, 0.75, SPATIAL)
    person.sy.to(0, 0.75, SPATIAL)
    person.alpha.to(0, 0.35, EFFECTS)
    person.sx.to(180, 1.0, BOUNCY)
    person.sy.to(180, 1.0, BOUNCY)
    person.alpha.to(180, 1.0, EFFECTS_FAST)
    return ("The clapper opens and claps shut; the subject, blurred while it opens, snaps back into "
            "focus on the clap.")


@spec('cloud_download')
def _(b):
    grp, p = b.split('cloud', b.I(0), [('head', R(8.2, 10.6, 15.8, 15.8), 'c'),
                                       ('shaft', R(10.8, 6.3, 13.2, 10.6), (12.0, 6.3))])
    cloud = grp
    cloud.pivot = (12.0, 20.0)
    elastic(p['head'], p['shaft'], 0, 90, 4.3, dist=1.6, wind=0.6)
    squash(cloud, 120, 0.08)
    return ("The arrow is pulled up into the cloud and shoots down on a stretching shaft; the cloud "
            "squashes as the download lands, then everything snaps back.")


@spec('cloud_upload')
def _(b):
    grp, p = b.split('cloud', b.I(0), [('head', R(8.2, 9.2, 15.8, 14.2), 'c'),
                                       ('shaft', R(10.8, 14.2, 13.2, 17.8), (12.0, 17.8))])
    grp.pivot = (12.0, 20.0)
    squash(grp, 0, 0.07, hold=90, spec_out=SPATIAL)
    elastic(p['head'], p['shaft'], 60, -90, 3.6, dist=1.8, wind=0.5)
    grp.ty.to(150, -0.6, SPATIAL)
    grp.ty.back(260, BOUNCY)
    return ("The cloud crouches, the arrow shoots up through it on a stretching shaft and the cloud "
            "lifts with it, then everything snaps back.")


@spec('co_present')
def _(b):
    scr = b.part('screen', b.I(0), pivot='tr')
    head = b.part('head', b.I(1), pivot='b')
    body = b.part('body', b.I(2), pivot='b')
    person = b.group('presenter', [head, body], pivot='b')
    pressxy(scr, 0, 0.94, 0.94, hold=150)
    hop(person, 0, 1.0, stretch=1.04)
    nod(head, 300, -12, hold=90)
    nod(head, 470, 8, hold=70)
    return ("The presenter hops forward as the screen behind pulls back, then nods to the audience "
            "twice.")


@spec('cognition')
def _(b):
    head = b.part('head', b.I(1), pivot=(8.0, 22.0))
    sp = b.part('spiral', b.I(0), pivot=(12.0, 11.1), parent=head)
    spin(sp, 0, 360, SPATIAL_SLOW)
    press(sp, 0, 0.7, hold=260, spec_out=BOUNCY)
    head.rot.to(0, -5, SPATIAL_SLOW)
    head.rot.to(260, 3, SPATIAL)
    head.rot.back(380, BOUNCY)
    return ("The thought spirals: the swirl tightens and spins a full turn while the head tilts back "
            "in thought, then it springs open and the head nods.")


@spec('cognition_2')
def _(b):
    head = b.part('head', b.I(1), pivot=(8.0, 22.0))
    brain = b.part('brain', b.I(0), parent=head)
    for k, t in enumerate((0, 200)):
        brain.sx.to(t, 0.8, SPATIAL_FAST)
        brain.sy.to(t, 0.8, SPATIAL_FAST)
        brain.sx.to(t + 70, 1.15, SPATIAL_FAST)
        brain.sy.to(t + 70, 1.15, SPATIAL_FAST)
        brain.rot.kick(t + 70, 400.0 * (1 - 2 * k), BOUNCY)
    brain.sx.back(330, BOUNCY)
    brain.sy.back(330, BOUNCY)
    nod(head, 60, -5, hold=90)
    nod(head, 260, -4, hold=80)
    return ("The brain fires twice: it clenches, bursts bigger with a twist and the head nods with "
            "each spark.")


@spec('compost')
def _(b):
    grp, p = b.split('compost', b.I(0), [
        ('sprout', R(7.6, 8.4, 17.0, 15.4), (12.0, 15.4)),
        ('head', R(11.9, 0.4, 15.9, 7.6), (12.0, 4.0)),
    ])
    grp.pivot = (12.0, 12.0)
    grp.rot.to(0, -25, SPATIAL)
    grp.rot.back(150, BOUNCY)
    sp = p['sprout']
    sp.sy.to(0, 0.2, SPATIAL)
    sp.sx.to(0, 0.6, SPATIAL)
    sp.sy.to(170, 1.0, BOUNCY)
    sp.sx.to(170, 1.0, BOUNCY)
    return ("The cycle winds back and turns forward, and the sprout shoots up "
            "out of the soil with a bounce.")


@spec('computer')
def _(b):
    scr = b.part('screen', b.I(1), pivot=(12.0, 18.0))
    base = b.part('base', b.I(0), pivot='b')
    scr.sy.to(0, 0.05, SPATIAL_FAST)
    pressxy(base, 60, 1.0, 0.5, hold=50, spec_out=BOUNCY)
    scr.sy.to(130, 1.0, (500.0, 0.6))
    pressxy(base, 230, 1.0, 0.7, hold=40, spec_out=BOUNCY)
    return ("The laptop snaps shut onto its base and flips open again with a springy bounce.")


@spec('connecting_airports')
def _(b):
    top = b.part('plane_right', b.I(1))
    bot = b.part('plane_left', b.I(0))
    through(top, 0, 30.0, 0, gap=120, spec_out=SPATIAL_FAST)
    through(bot, 90, -30.0, 0, gap=120, spec_out=SPATIAL_FAST)
    top.rot.kick(240, 200.0, BOUNCY)
    bot.rot.kick(330, -200.0, BOUNCY)
    return ("The two planes fly off in opposite directions and come back in from the other side, "
            "banking as they land on their routes.")


@spec('construction')
def _(b):
    head = [(9.5, 0.5), (14.75, 5.75), (4.25, 16.25), (0.5, 12.5), (0.5, 0.5)]
    grp, p = b.split('tools', b.I(1), [('hammer_head', head, (11.0, 11.0))])
    handle = b.part('hammer_handle', b.I(0), pivot=(11.0, 11.0))
    hammer = b.group('hammer', [p['hammer_head'], handle], pivot=(11.0, 11.0), parent=grp)
    hammer.rot.to(0, -20, SPATIAL)
    hammer.rot.to(140, 6, (900.0, 0.6))
    hammer.rot.back(240, BOUNCY)
    wr = p['tools_rest']
    wr.pivot = (11.0, 11.0)
    wr.rot.kick(170, -300.0, BOUNCY)
    grp.pivot = (12.0, 12.0)
    press(grp, 170, 0.94, hold=50)
    return ("The hammer is raised and strikes; the wrench shudders with the blow and both tools "
            "bounce.")


@spec('content_copy')
def _(b):
    front = b.part('front', b.I(0), pivot='b')
    back = b.part('back', b.I(1), pivot='bl')
    front.tx.to(0, 1.4, SPATIAL)
    front.ty.to(0, -1.4, SPATIAL)
    back.tx.to(80, 1.0, SPATIAL)
    back.ty.to(80, -1.0, SPATIAL)
    front.tx.back(200, BOUNCY)
    front.ty.back(200, BOUNCY)
    back.tx.back(220, BOUNCY)
    back.ty.back(220, BOUNCY)
    squash(front, 300, 0.06)
    return ("The page slides off the original, which pops forward to follow it; then the copy lands "
            "back on top with a squash.")


def _scissors(b):
    sc = b.part('scissors', b.I(0), pivot=(12.0, 12.0))
    blade = b.part('blade', b.I(1), pivot=(12.0, 12.0))
    pair = b.group('pair', [sc, blade], pivot=(12.0, 12.0))
    for k in range(2):
        t = k * 190
        blade.rot.to(t, 22, (900.0, 0.7))
        sc.rot.to(t, -5, (900.0, 0.7))
        blade.rot.to(t + 90, 0, SPATIAL_FAST)
        sc.rot.to(t + 90, 0, SPATIAL_FAST)
        pair.tx.to(t + 20, 0.7, SPATIAL_FAST)
        pair.ty.to(t + 20, -0.7, SPATIAL_FAST)
        pair.tx.to(t + 110, 0.0, SPATIAL)
        pair.ty.to(t + 110, 0.0, SPATIAL)
    blade.rot.back(380, BOUNCY)
    sc.rot.back(380, BOUNCY)
    pair.tx.back(380, BOUNCY)
    pair.ty.back(380, BOUNCY)


@spec('content_cut')
def _(b):
    _scissors(b)
    return "The scissors snip twice, both blades closing hard, and lunge forward with each cut."


@spec('cut')
def _(b):
    _scissors(b)
    return "The scissors snip twice, both blades closing hard, and lunge forward with each cut."


@spec('content_paste')
def _(b):
    grp, p = b.split('board', b.I(0), [('clip', R(7.6, 0.6, 16.4, 6.6), (12.0, 6.6))])
    grp.pivot = (12.0, 21.0)
    grp.ty.to(0, -0.6, SPATIAL)
    grp.ty.to(120, 0.0, (900.0, 0.9))
    squash(grp, 170, 0.08)
    clip = p['clip']
    clip.sy.to(170, 0.55, SPATIAL_FAST)
    clip.sy.back(230, BOUNCY)
    return ("The clipboard is lifted and slammed down, and its clip bites shut with a bounce.")


@spec('contrast')
def _(b):
    c = b.part('contrast', b.I(0))
    spin(c, 0, 360, SPATIAL_SLOW)
    press(c, 0, 0.82, hold=250, spec_out=BOUNCY)
    return ("The circle spins a full turn, light and dark chasing each other, shrinking as it turns, "
            "and lands back in place with a bounce.")


@spec('copy_all')
def _(b):
    pg = b.part('page', b.I(0))
    dots = [b.part('d%d' % k, b.I(i)) for k, i in enumerate([1, 2, 3, 4, 5, 6, 7, 8])]
    for k, d in enumerate(dots):
        d.sx.to(k * 35, 0.0, EFFECTS_FAST)
        d.sy.to(k * 35, 0.0, EFFECTS_FAST)
        d.sx.to(k * 35 + 70, 1.0, BOUNCY)
        d.sy.to(k * 35 + 70, 1.0, BOUNCY)
    pg.sx.to(330, 0.82, SPATIAL_FAST)
    pg.sy.to(330, 0.82, SPATIAL_FAST)
    pg.sx.back(400, BOUNCY)
    pg.sy.back(400, BOUNCY)
    return ("The dashed outline is traced again around the page, dash by dash, and the page stamps "
            "down a copy with a punch.")


@spec('countertops')
def _(b):
    grp, p = b.split('counter', b.I(0), [
        ('faucet', R(11.8, 3.8, 18.2, 9.95), (17.0, 9.95)),
        ('knob', R(3.8, 3.8, 10.2, 9.95), (7.0, 7.0)),
    ])
    k, f = p['knob'], p['faucet']
    k.rot.to(0, 45, SPATIAL)
    k.rot.back(170, BOUNCY)
    f.rot.to(80, -18, SPATIAL)
    f.rot.back(240, BOUNCY)
    grp.pivot = (12.0, 20.0)
    pressxy(grp, 200, 1.0, 0.94, hold=60)
    return ("The knob is twisted, the faucet swings round on its base and the counter gives a little "
            "bounce.")


@spec('credit_card')
def _(b):
    c = b.part('card', b.I(0))
    c.sx.to(0, 0.9, SPATIAL)
    through(c, 60, 32.0, 0, gap=140, spec_out=SPATIAL_FAST)
    c.sx.back(300, BOUNCY)
    return ("The card is swiped: it winds back, slides out through the reader and comes back in from "
            "the other side, landing with a bounce.")


@spec('crop')
def _(b):
    outer = b.part('outer', b.I(0))
    inner = b.part('inner', b.I(1))
    for n, s in ((outer, 1), (inner, -1)):
        n.tx.to(0, -0.7 * s, SPATIAL)
        n.ty.to(0, 0.7 * s, SPATIAL)
        n.tx.to(130, 0.9 * s, (900.0, 0.7))
        n.ty.to(130, -0.9 * s, (900.0, 0.7))
        n.tx.back(220, BOUNCY)
        n.ty.back(220, BOUNCY)
    return ("The crop handles pull apart, then snap in tight past their places and bounce back to "
            "settle.")


@spec('cruelty_free')
def _(b):
    grp, p = b.split('rabbit', b.I(0), [
        ('ear_l', R(4.6, 1.5, 11.6, 12.4), (8.75, 12.4)),
        ('ear_r', R(12.4, 1.5, 19.4, 12.4), (15.25, 12.4)),
    ])
    el = b.part('eye_l', b.I(1))
    er = b.part('eye_r', b.I(2))
    head = b.group('head', [grp, el, er], pivot=(12.0, 22.0))
    p['ear_l'].rot.kick(0, -700.0, (700.0, 0.3))
    p['ear_r'].rot.kick(160, 700.0, (700.0, 0.3))
    head.ty.to(0, -0.5, SPATIAL_FAST)
    head.ty.back(90, BOUNCY)
    for n in (el, er):
        pressxy(n, 230, 1, 0.1, hold=60, spec_out=SPATIAL_FAST)
    return ("The rabbit perks up: one ear twitches, then the other, and it blinks.")


@spec('currency_franc')
def _(b):
    grp, p = b.split('franc', b.I(0), [
        ('top', R(9.05, 2.6, 18.4, 5.4), (9.0, 4.0)),
        ('mid', R(9.05, 10.6, 17.4, 13.4), (9.0, 12.0)),
        ('cross_r', R(9.05, 15.6, 13.4, 18.4), (9.0, 17.0)),
        ('cross_l', R(4.6, 15.6, 6.95, 18.4), (7.0, 17.0)),
    ])
    for k, name in enumerate(('top', 'mid', 'cross_r', 'cross_l')):
        n = p[name]
        t0 = k * 70 if k < 3 else 140
        n.sx.to(0, 0.05, EFFECTS_FAST)
        n.sx.to(80 + t0, 1.0, (500.0, 0.45))
    grp.pivot = (8.0, 21.0)
    grp.ty.to(330, -0.6, SPATIAL_FAST)
    grp.ty.back(400, BOUNCY)
    return ("The bars of the franc sign snap back into the stem and shoot out again one after "
            "another with a wobble; the sign bounces when the cross bar lands.")


@spec('curtains_closed')
def _(b):
    c = b.part('curtains', b.I(0), pivot='t')
    mid = b.hole('gap', c, b.isl[0], 1)
    left = b.hole('fold_l', c, b.isl[0], 0)
    right = b.hole('fold_r', c, b.isl[0], 2)
    mid.sx.to(0, 2.6, SPATIAL)
    for n in (left, right):
        n.sx.to(0, 0.55, SPATIAL)
    mid.sx.back(220, BOUNCY)
    left.sx.back(240, BOUNCY)
    right.sx.back(240, BOUNCY)
    rock(c, 200, 2, 2, 120)
    return ("The curtains are pulled apart in the middle, their folds bunching to the sides, then "
            "swish closed again and sway on the rod.")


@spec('custom_typography')
def _(b):
    a = b.part('a', b.I(2), pivot='b')
    dash = b.part('dash', b.I(1))
    caret = b.part('caret', b.I(0))
    a.ty.to(0, -1.6, SPATIAL)
    a.sy.to(0, 1.06, SPATIAL)
    a.ty.to(140, 0.0, (900.0, 0.9))
    a.sy.to(140, 1.0, SPATIAL)
    squash(a, 200, 0.18, hold=60)
    shift(dash, 200, dx=-0.9, hold=70)
    shift(caret, 200, dx=0.9, hold=70)
    blink(caret, 320, 0.0, hold=70)
    return ("The letter is lifted and dropped onto the baseline with a squash; the guides are "
            "pushed aside by the impact and the caret blinks.")


@spec('data_exploration')
def _(b):
    grp, p = b.split('chart', b.I(0), [('trend', R(5.6, 7.7, 18.3, 15.9), 'c')])
    tr = p['trend']
    wr = b.group('trend_w', [tr], parent=grp)
    clip, lo, hi = clip_band((5.0, 7.0, 19.0, 16.6), -30, margin=0.0)
    wr.clip = clip
    lo.to(0, 1.0, EFFECTS_FAST)
    lo.snap(100, 0.0)
    hi.snap(100, 0.0)
    hi.to(102, 1.0, SPATIAL_SLOW)
    shoot(tr, 300, -45, dist=0.7, wind=0.2)
    grp.pivot = (12.0, 12.0)
    press(grp, 330, 0.9, hold=60, spec_out=BOUNCY)
    return ("The trend line is drawn again across the bubble, its arrow darts up to the corner and "
            "the bubble gives with the push.")


@spec('data_thresholding')
def _(b):
    grp, p = b.split('frame', b.I(0), [('hatch', R(4.6, 13.4, 19.4, 18.8), 'c')])
    h = p['hatch']
    wr = b.group('hatch_w', [h], parent=grp)
    clip, lo, hi = clip_band((4.4, 13.0, 19.6, 19.0), 0, margin=0.0)
    wr.clip = clip
    lo.to(0, 1.0, EFFECTS_FAST)
    lo.snap(90, 0.0)
    hi.snap(90, 0.0)
    hi.to(92, 1.0, SPATIAL)
    line = b.part('trend', b.I(1), pivot='b')
    redraw(b, line, 120, -30, erase_ms=80)
    line.ty.to(260, -1.2, SPATIAL_FAST)
    line.ty.to(360, 0.0, (900.0, 0.9))
    squash(line, 420, 0.15)
    return ("The threshold zone is hatched in again from left to right, the trend line is drawn and "
            "jumps above it, landing with a squash.")


@spec('database')
def _(b):
    d = b.part('database', b.I(0), pivot='b')
    hop(d, 0, 1.0, stretch=1.04)
    d.rot.kick(330, 150.0, BOUNCY)
    return "The database stack hops, lands with a squash and wobbles as it settles."


@spec('database_off')
def _(b):
    c = b.part('database', b.all())
    off, on, t = off_icon(b, 'database', spec_back=BOUNCY)
    c.pivot = (12.0, 21.0)
    squash(c, t - 60, 0.14, hold=70)
    c.tx.kick(t - 20, -40.0, (900.0, 0.3))
    return ("The slash retracts, showing the database whole for a moment, and cuts back across with "
            "a bounce; the stack slumps under the blow and shudders.")


@spec('database_search')
def _(b):
    d = b.part('database', b.I(0), pivot='b')
    lens = b.part('lens', b.I(1))
    path = [(-1.6, -1.2), (-2.4, -4.0), (-0.6, -5.6), (0.4, -2.4)]
    for k, (x, y) in enumerate(path):
        lens.tx.to(k * 100, x * 0.55, SPATIAL)
        lens.ty.to(k * 100, y * 0.55, SPATIAL)
    lens.tx.back(400, BOUNCY)
    lens.ty.back(400, BOUNCY)
    swell(lens, 200, 1.18, hold=100)
    squash(d, 400, 0.06)
    pop(lens, 430, 0.7, dt=60)
    return ("The magnifier sweeps a loop over the database, zooming in on a record, then drops back "
            "with a pop: found.")


@spec('database_upload')
def _(b):
    d = b.part('database', b.I(1), pivot='b')
    badge = b.part('badge', b.I(0), pivot='b')
    arrow = b.hole('arrow', badge, b.isl[0], 0)
    squash(badge, 0, 0.12, hold=80, spec_out=SPATIAL)
    badge.ty.to(110, -1.0, SPATIAL_FAST)
    badge.sy.to(110, 1.06, SPATIAL_FAST)
    badge.ty.to(220, 0.0, (900.0, 0.9))
    badge.sy.to(220, 1.0, SPATIAL)
    dart(arrow, 80, 0, -0.6, wind=0.5)
    pressxy(d, 120, 1.02, 0.94, hold=60, spec_out=BOUNCY)
    return ("The upload badge crouches and launches off the database, its arrow pushing up, then "
            "drops back; the database recoils.")
