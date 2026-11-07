# Generator

`tools/m3a` builds the animated icons from the Material Symbols sources.
It is used for icons 621 and later (generator `0.12.0` in `manifest.json`).

Copyright 2026 Marco Morosi. Licensed under the Apache License, Version 2.0
(see [LICENSE](../LICENSE)).

## Requirements

- Python 3 with `numpy` and `Pillow`.
- `rsvg-convert` (librsvg), used by the checks and the filmstrips.
- The Material Symbols sources: folder `symbols/web` of
  [google/material-design-icons](https://github.com/google/material-design-icons)
  at the commit in `manifest.json` (`source_commit`). Set `M3A_SRC` to that
  folder, or place the clone next to this repository as
  `material-design-icons`.
- Optional, only for `verify_chrome.py`: Node, `puppeteer` (`M3A_PUPPETEER`)
  and a Chrome binary (`M3A_CHROME`).

None of these are distributed with the project.

## Files

- `geom.py`: path parsing, rescaling from 960 to 24, islands (outline plus
  its holes), transforms, path formatting.
- `anim.py`: spring tracks (Compose `SpringSpec` physics with the M3
  Expressive motion scheme), parts, clips, keyframe reduction.
- `emit.py`: animated SVG (SMIL) and AnimatedVectorDrawable output, loop and
  one-shot.
- `lib.py`: icon builder and motion vocabulary (press, hop, dart, redraw,
  roll, spin, ...), and the `_off` slash mechanism.
- `raster.py`: small rasterizer, used to find the slash of `_off` icons.
- `specs_*.py`: one spec per icon: its parts, its motion and its concept.
- `build.py`: checks and writes the files and the manifest entries.
- `update_docs.py`: rebuilds the grid of `preview.html` and the progress
  lines of `preview.html` and `README.md` from the manifest.
- `validate.py`: structural checks of the generated files.
- `render.py`, `sheet.py`, `verify_chrome.py`, `shot.js`: development aids
  (filmstrips, contact sheets, comparison with real SMIL playback in Chrome).

## Usage

```sh
cd tools/m3a
python3 build.py check bubble cloud_off          # checks only
python3 build.py strip /tmp/strip bubble         # filmstrip PNG
M3A_DATE=2026-11-07 python3 build.py write 621 1020
python3 update_docs.py
python3 validate.py bubble cloud_off
```

## Checks

`build.py` refuses an icon when:

- any frame draws outside the 24x24 box;
- the first or the last frame differs from the untouched icon (raster
  comparison of the motion model with the source path);
- the gesture is longer than 1600 ms.

`verify_chrome.py` renders the emitted SVG files in Chrome at several times
and compares them with the model; `validate.py` checks the fixed rules of the
README and the AnimatedVectorDrawable structure (names, targets, keyframe
order, compatible path morphs).
