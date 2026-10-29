# M3 Expressive Animated Icons

I've always wanted to use Google's animated Material Symbols since Material 3 Expressive came out, but I could never find them anywhere.

So I decided to make them myself with Claude. I'm making as many as I can and putting them here for everyone to use, because I think animated icons can make interfaces so much nicer.

Enjoy!

## Progress

**320 / 4,157 icons completed** · 7.7%

Icons are being created strictly in alphabetical order, following the original Material Symbols collection. No skipping ahead!

Progress is tracked in [`manifest.json`](manifest.json) and updated with every batch.

---

Material Symbols (Rounded, weight 400) animated following M3 Expressive, in two formats with the same animation:

- **Web:** animated SVG (SMIL); works inline, in `<img>` and as a background.
- **Android:** AnimatedVectorDrawable (XML).

Every icon comes in two variants:

- `loop`: gesture + pause, repeated forever. Use it only where a loop has a purpose (loading, waiting, calling attention).
- `oneshot`: the gesture once, for state changes.

## Fixed rules

- SVG: always `viewBox="0 0 24 24"` and `fill="currentColor"` on the root, no colors on paths. Change the color from CSS (`color`) or code.
- Android: white `fillColor` + `android:tint="?attr/colorControlNormal"`, the equivalent of currentColor. In Compose `Icon(tint = ...)` overrides it.
- The first and the last frame equal the original icon: the loop has no jump, and an animation stopped at its end shows the untouched icon.
- Original geometry: only rescaled from 960 to 24 and split into parts. Where a motion needs shapes the source cannot provide, a procedural copy is shown only while the icon moves and matches the source at rest.
- No frame draws outside the 24x24 box.
- A plus never rotates: at 45 degrees it reads as an x ("close").
- "_off" icons: the slash retracts and is drawn again; behind it the "on" icon is shown, so no outline of the cut is ever visible.

## Motion

- Physical spring-based motion, inspired by Compose `SpringSpec`.
- Spatial springs for position, rotation and scale (overshoot allowed).
- Effects springs for opacity (never past the final value).
- Reduced motion:
  - Web: `prefers-reduced-motion: reduce` shows the still icon.
  - Android: with animator duration scale 0 the animator jumps to its end, which is the still icon.

## Web usage

```html
<!-- Inline: the icon takes the text color -->
<span style="color:#6750a4">
  <!-- Insert the contents of web/loop/10mp.svg here -->
</span>

<!-- As an image -->
<img src="web/loop/10mp.svg" width="48" height="48" alt="10 MP">
```

Internal IDs (`clipPath`) contain the icon name and variant, so the loop and one-shot of the same icon can live on the same page. Multiple copies of the same icon can also be used on the same page.

To color an icon used as an external file: inline it, or use it as a `mask-image` on an element with a `background-color`.

Restart a one-shot from code: `svgElement.setCurrentTime(0)`.

## Android usage

Copy `android/drawable/*.xml` into `res/drawable/`.

```kotlin
// Compose (androidx.compose.animation:animation-graphics)
val image = AnimatedImageVector.animatedVectorResource(R.drawable.avd_10mp_oneshot)
var atEnd by remember { mutableStateOf(false) }
LaunchedEffect(Unit) { atEnd = true }

Icon(
    painter = rememberAnimatedVectorPainter(image, atEnd),
    contentDescription = "10 MP",
)
```

```kotlin
// Views: framework AnimatedVectorDrawable
val d = ContextCompat.getDrawable(context, R.drawable.avd_10mp_loop) as AnimatedVectorDrawable
imageView.setImageDrawable(d)
d.start()
```

For loop variants, check whether the Compose painter honors `repeatCount="-1"`. If not, use the framework `AnimatedVectorDrawable` for loops (also inside Compose through a Drawable painter) or restart the animation at the end of each cycle.

## Licenses

- Icons: derived from Google Material Symbols, Apache License 2.0.
- Original source: [google/material-design-icons](https://github.com/google/material-design-icons).
- See [LICENSE](LICENSE), [NOTICE](NOTICE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for licensing and attribution details.
