# Changelog

Icons are added in alphabetical order (C locale) of the Material Symbols
collection. Indexes refer to `manifest.json`.

## 2026-11-07: icons 621-1020

- Added 400 icons, from `bubble` (621) to `deblur` (1020), in all four
  variants (web loop, web one-shot, Android loop, Android one-shot).
  Progress: 1020 / 4,157 (24.5%).
- Every icon has its own concept in `manifest.json`. Families share one
  motion grammar: calendars flip their page, handsets ring, checks are drawn
  again, counters roll like an odometer, clock loaders empty and refill
  clockwise, chess pieces move the way they move on the board, currency
  symbols flip like a coin, and `_off` / `_disabled` icons retract their
  slash over the "on" icon and cut across again.
- Added the generator used for these icons in `tools/m3a` (generator
  `0.12.0`, Apache License 2.0), with its checks: no frame outside the box,
  first and last frame equal to the untouched icon, real SMIL playback in
  Chrome compared with the motion model, structural validation of the
  AnimatedVectorDrawable files.
- Second pass on 82 of these icons whose first version was too plain (for
  example the call arrows, the chevrons, `close`, the car climate icons,
  `cloud_download`, `database`): larger moves, squash and stretch along the
  direction of motion, arrowheads that fly on an elastic shaft, shapes cut
  into pieces while they move, parts that leave and come back from the other
  side. `car_seat_off` now retracts its slash like the other `_off` icons.
- `preview.html`: new cards and progress.
- `NOTICE`: documents the `_off` icon mechanism and the clock loader copies
  used while moving, and the generator.
- `THIRD_PARTY_NOTICES.md`: lists the tools the generator uses (none of them
  is distributed).

## 2026-11-03: icons 321-620

- Icons 321-370, then 371-470 (`autopause` to `battery_charging_50`), then
  471-620 (up to `brush`).
- `battery_20` ... `battery_90`: upstream drawing corrected (see `NOTICE`).
- Preview, README and manifest updated.

## 2026-10-30: first release

- Icons 1-320.
- Affiliation disclaimer and source details in `NOTICE`.
