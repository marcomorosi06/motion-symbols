# Copyright 2026 Marco Morosi
# Licensed under the Apache License, Version 2.0 (see LICENSE at repo root).
#
# Small nonzero-winding rasterizer (numpy) used to analyse icons, for
# example to locate the slash of "_off" icons against their "on" icon.

import numpy as np

import geom

RES = 20  # pixels per unit: 480 x 480 for the 24 box


def rasterize(subs, res=RES):
    n = 24 * res
    img = np.zeros((n, n), dtype=np.int32)
    ys = (np.arange(n) + 0.5) / res
    xs = (np.arange(n) + 0.5) / res
    edges = []
    for sp in subs:
        poly = geom.flatten(sp, 10)
        if len(poly) < 3:
            continue
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            if y1 != y2:
                edges.append((x1, y1, x2, y2))
    if not edges:
        return img > 0
    E = np.array(edges)
    x1, y1, x2, y2 = E[:, 0], E[:, 1], E[:, 2], E[:, 3]
    up = (y2 > y1).astype(np.int32) * 2 - 1
    ylo = np.minimum(y1, y2)
    yhi = np.maximum(y1, y2)
    for r, y in enumerate(ys):
        m = (ylo <= y) & (y < yhi)
        if not m.any():
            continue
        xx = x1[m] + (y - y1[m]) * (x2[m] - x1[m]) / (y2[m] - y1[m])
        w = up[m]
        order = np.argsort(xx)
        xx = xx[order]
        w = w[order]
        cum = np.cumsum(w)
        idx = np.searchsorted(xx, xs, side='right')
        wn = np.where(idx > 0, cum[np.maximum(idx - 1, 0)], 0)
        img[r] = wn
    return img != 0


def slash_fit(off, on, res=RES):
    """Fit the slash: pixels in off but not on are the bar, pixels in on but
    not off are the gap. The line is refitted on the pixels close to it, so
    other small design differences do not bend it. Returns (A, B, hw,
    mismatch) with A the upper end and hw the corridor half width."""
    bar = off & ~on
    gap = on & ~off
    yy, xx = np.nonzero(bar)
    if len(xx) < 50:
        raise ValueError('no slash found')
    P = np.stack([(xx + 0.5) / res, (yy + 0.5) / res], 1)
    keep = np.ones(len(P), bool)
    for it in range(4):
        Q = P[keep]
        c = Q.mean(0)
        u, s, vt = np.linalg.svd(Q - c, full_matrices=False)
        d = vt[0]
        nrm = np.array([-d[1], d[0]])
        dist = np.abs((P - c) @ nrm)
        keep = dist < (2.0 if it else 3.0)
    Q = P[keep]
    proj = (Q - c) @ d
    hw_bar = float(np.percentile(np.abs((Q - c) @ nrm), 99))
    A = c + d * proj.min()
    B = c + d * proj.max()
    hw = hw_bar
    mism = 0.0
    gy, gx = np.nonzero(gap)
    if len(gx):
        G = np.stack([(gx + 0.5) / res, (gy + 0.5) / res], 1)
        gd = np.abs((G - c) @ nrm)
        gp = (G - c) @ d
        inside = (gd <= 5.0) & (gp >= proj.min() - 1.0) & (gp <= proj.max() + 1.0)
        if inside.any():
            hw = max(hw, float(gd[inside].max()))
        mism = float((~inside).sum()) / float(max(1, on.sum()))
    hw = hw + 0.15
    if A[1] > B[1]:
        A, B = B, A
    return (float(A[0]), float(A[1])), (float(B[0]), float(B[1])), hw, mism
