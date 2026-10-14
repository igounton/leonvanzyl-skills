# Leon YouTube

The slide system for Leon's YouTube videos: 1920×1080 slides recorded with the presenter's webcam on the right. It looks like a product keynote. A graphite stage is lit from above, and titles are set in very large white type with one accent-coloured line beneath them. Code sits in frosted-glass panels, product UI floats on the stage as white paper, glossy 3D icon tiles add personality, and an animated horizon wave of dots runs along the bottom of every slide.

> **On the name.** "YouTube" is where these slides are shown. This system carries none of YouTube's brand: no YouTube logo, no YouTube red, no Roboto.

## Sources

- **Style reference:** screenshots of a recent OpenAI product keynote (the Agents API, Codex Security and Dottie slides), used for the stage lighting, type scale, glass code panel, glowing cursor, glossy tiles, floating white cards and the orange horizon glow. Nothing was copied from their brand; there are no OpenAI marks, names or fonts here.
- **Previous deck:** the Jev explainer built on *Core Design System*, from which this keeps the 380px webcam lane and the dot-field wave, restyled.
- **First real deck:** "OpenAI Dots" (13 slides). The components added in v2 (SlideTitle, SpecRow, DataTable, StepList, ChatBubble) and the text-zone and density rules below come from reviewing it.
- **No logo exists for this system.** Wherever a mark is needed, set "Leon YouTube" in Figtree 600 at −0.035em, as `thumbnail.html` does. `assets/` is intentionally absent.

## Index

| Path | What's there |
| --- | --- |
| `styles.css` | The only file consumers link. `@import` lines only. |
| `tokens/` | `fonts`, `colors`, `typography`, `spacing`, `radii`, `elevation`, `motion`, and `components` (the component and slide-accent classes) |
| `components/slide/` | **Stage** (the slide itself), **SlideTitle** |
| `components/core/` | **IconTile**, **MonoLabel**, **Cursor** |
| `components/surfaces/` | **GlassPanel**, **CodePanel** |
| `components/lists/` | **SpecRow**, **DataTable**, **StepList** |
| `components/paper/` | **ProductWindow**, **ChatBubble**, **TaskCard**, **Pill** |
| `components/data/` | **Stat**, **BarRow**, **Track** |
| `guidelines/` | Specimen cards: colours, type, the slide frame, radii, glass and glow, the horizon wave |
| `ui_kits/sample-slides/` | Five 1920×1080 sample slides, one per core layout |
| `thumbnail.html` | Homepage tile |
| `SKILL.md` | Agent-Skills entry point for use outside this product |

Each component has a sibling `.d.ts` (props contract) and `.prompt.md` (what and when, a usage example, the rules). **Build slides from the components.** A hand-built title, list or table drifts from the system; if a component is missing, build it from the tokens and the `.ly-*` classes in `tokens/components.css`.

---

## The slide frame

- **Every slide is one `Stage`** at exactly 1920×1080. It paints the whole background (stage gradient, two soft light beams, the horizon wave, the vignette) and places its children in the **safe area**: `--margin` (100px) from the top and left, `--content-width` × `--content-height` (1440×880).
- **The right-hand `--webcam-lane` (380px, full height) stays empty.** No text, panels, cards, tiles, cursors or glows go in it; only the background and the wave run through it.
- **Text on the bare stage ends above y≈780** (the top 680px of the safe area). The wave's crest glows between roughly 800 and 960, and text over it becomes unreadable. Anything lower (a list, a table, a footnote) goes inside a GlassPanel or on paper, which blur the wave. Put a table's source line inside its panel, not under it.
- **Everything fits the safe area.** Title block plus visual plus footnote must total 880px or less, so nothing is pushed into the top margin. If it doesn't fit, cut copy or split the slide.
- **One accent per slide**, set with `accent`: `azure` by default, `ember` for security, controls, warnings and costs, or to vary the rhythm of a deck. Inside a Stage, `var(--slide-accent)` is that colour; use it (never a hex value) for accent text, so changing `accent` recolours the whole slide. `iris` and `mint` are for icon tiles only.
- **Keep the wave on.** `waveLevel="low"` is the default; use `"middle"` or `"high"` only when the lower half of the slide is empty. Lower `waveIntensity` to 0.6 behind tables; raise it to 1.4 on title-only slides.

## Decks

In a Claude Design deck, each `<section>` holds exactly one Stage (give the section `background: #000`). Expose one boolean `showLane` tweak on the deck and pass it to every Stage, so the webcam lane can be checked across the whole deck and turned off before recording.

## Layout patterns

Every slide starts with a `SlideTitle`. Its three sizes fix the title and subtitle sizes, so use them rather than choosing your own.

- **Hero:** `SlideTitle size="display"` with two tiles as children and an eyebrow, 760px wide, beside a `CodePanel` with `cursor` (616px), or alone and vertically centred.
- **Split:** `SlideTitle size="split"` (700px, two or three lines, optional `note`) on the left, and one visual on the right (680px): a `ProductWindow`, a `GlassPanel` of `SpecRow`s, or a `StepList`. A `TaskCard` may overlap the visual's lower-left edge by about 170px.
- **Comparison:** `SlideTitle` (headline) across the top, then two `GlassPanel`s in a two-column grid with `--gap-lg` (40px). The winner gets `highlight`, an accent `MonoLabel`, an accent `Stat` and a fast `Track`. The loser stays in `--text-secondary` with a slow one. One tile may sit on the winner's top edge, inside the panel's width.
- **Card row:** `SlideTitle` (headline), then three or four `GlassPanel`s in a grid, each with one 84px `IconTile` on its top-left edge (`position: absolute; top: -42px; left: 32px`) and a heading and one line inside. Highlight one card at most.
- **Table:** `SlideTitle` (headline), then one `GlassPanel` holding a `DataTable`, 48px below. Six rows and five columns at most, one line per cell, `waveIntensity` 0.6, and the source line inside the panel.
- **Big stat:** a `MonoLabel` eyebrow, a `Stat` at `size={220}` and the accent line on the left (560px), and a `GlassPanel` of `BarRow`s or `SpecRow`s on the right (820px). Stat shrinks long figures to fit the column.
- Everything is vertically centred in the safe area. The right-hand visual's right edge sits on the edge of the safe area, where the webcam lane begins.

## Density

- Glass-panel lists: seven `SpecRow`s at most. Tables: six rows by five columns. Steps: five. Card row: four cards.
- Text sizes on the stage: subtitle 40–46, body 30, list values 30, table cells 24, captions 22, mono labels 22 (16–18 inside panels). Nothing smaller than 14px, and only pills inside paper go that small.
- Every cell and list value should be one line, two at most. Shorten the copy before shrinking the type.

---

## Content fundamentals

- **Titles are nouns or short claims**, six words at most, in sentence case, without a full stop.
- **The subtitle is one clause** in the accent: what the title means for the viewer. No full stop.
- **Say the number, with its unit:** "70–500 ms", "~70×", "$21". Label what was measured and, when you didn't measure it, where it came from: "vendor figures", "list prices, September 2026".
- **One idea per slide.** If a slide needs a second subtitle, it is two slides.
- **Mono labels are a few words**, parts separated by a middle dot: "System 1 · Jev".
- No emoji, exclamation marks, hype adjectives or rhetorical questions.

## Visual foundations

### Colour
The stage is `--stage-900`, fading from `--stage-800` at the top to `--stage-950` at the bottom under a soft overhead spotlight. There is no light theme. Titles are `--text` (white), supporting copy `--text-secondary`, labels and footnotes `--text-muted`. The losing side of any comparison is `--text-secondary`; the winner is white or the accent. Paper UI uses `--paper` with `--ink` and `--ink-2`. Accent text on paper uses the `-ink` shade, and pills use the matching `-wash`. Status on paper is a `Pill` (mint allowed, ember ask or warn, neutral blocked), never coloured text. In bar charts the highlighted row takes the accent and glows; every other bar is `--bar-rest`.

### Type
Two faces. **Figtree** (500/600) for everything you read: display at −0.035em, headlines at −0.03em, panel statements at −0.025em. **Geist Mono** (400/500) for labels (uppercase, 0.14em tracking), data and code. Figures always use tabular numerals.

### Surfaces
Glass (`GlassPanel`, `CodePanel`) is `--glass-fill` with a `--glass-blur` backdrop blur, a `--hairline` border and `--shadow-panel`; the wave shows softly through it. Paper floats with `--shadow-card` or `--shadow-window`. The winning panel gets an accent hairline and bloom, on one element per slide. No glass inside glass, no paper inside glass.

### Radii
`--radius-panel` 28 for glass, `--radius-card` 24 for task cards, `--radius-window` 22 for product windows, `--radius-chip` 14 inside paper, `--radius-tile` 28.5% for icon tiles, and `--radius-pill` for pills, bars and tracks.

### Motion
Nothing enters: slides are recorded as held frames, so every moment is already complete. Motion is ambient and looping. The wave drifts at 30fps, tiles float 12px over 7–8s (stagger a second tile with a negative `animation-delay`), the cursor nudges every 4s, and `Track` dots loop. All of it stops under reduced motion.

## Iconography

Icon tiles carry the personality; use the glyphs `IconTile` provides (`code`, `eyes`, `shield`, `sparkle`, `bars`, `bolt`, `arrow`, `check`). For line icons elsewhere, use 24px inline SVG with white strokes at 1.7 width and round caps and joins. No emoji, and no other companies' logos. Screenshots of real products go inside a `ProductWindow` or `GlassPanel`, never full-bleed.

## Fonts

Figtree and Geist Mono load from Google Fonts via `@import` in `tokens/fonts.css`, so there are no `@font-face` rules. Figtree is a free stand-in for the geometric sans of the keynote reference. To use licensed fonts, replace the `@import` with local `@font-face` rules pointing at `assets/fonts/`.

## Using it in Claude Design

The components are `window.LeonYouTube_792a19`. A split slide in a deck section:

```html
<section data-label="Infrastructure" style="background: #000">
  <x-import component-from-global-scope="LeonYouTube_792a19.Stage" accent="azure" show-lane="{{ showLane }}" hint-size="1920px,1080px">
    <div style="display: flex; align-items: center; gap: 60px; height: 100%">
      <x-import component-from-global-scope="LeonYouTube_792a19.SlideTitle" size="split" title="Its own computer, running 24/7" subtitle="Hosted by OpenAI, so work continues with your laptop closed" style="width: 700px; flex-shrink: 0"></x-import>
      <x-import component-from-global-scope="LeonYouTube_792a19.GlassPanel" style="width: 680px; flex-shrink: 0">
        <x-import component-from-global-scope="LeonYouTube_792a19.SpecRow" label="Model" value="GPT-6 Astra"></x-import>
        <x-import component-from-global-scope="LeonYouTube_792a19.SpecRow" label="Uptime" value="24/7, several projects at once" highlight="{{ true }}"></x-import>
        <x-import component-from-global-scope="LeonYouTube_792a19.SpecRow" label="Your laptop" value="Opt-in, off by default"></x-import>
      </x-import>
    </div>
  </x-import>
</section>
```
