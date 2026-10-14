# The channel's design system ("Leon YouTube"), bundled

A copy of the design system Leon's slides are built in, so this skill is self-contained: no folder outside the skill is
needed, on any machine. The graphics already implement it in code (`assets/gfx/engine.js` theme `stage`,
`scripts/build_gfx_common.py` tiles and type, the glass cards in `scripts/compose.py`, the keyword pops, CTA cards and zoom marks in `scripts/overlay.py` / `zoom.py`); this folder is the
reference behind them. Read `readme.md` and skim `tokens/*.css` and the component `.prompt.md` files before designing
anything new, and build from these values rather than inventing new ones.

| Path | What's there |
|---|---|
| `readme.md` | the rules: the stage, type scale, colours and accents, glass vs paper, icon tiles, the horizon wave, density |
| `tokens/` | the exact values: `colors.css`, `typography.css`, `spacing.css`, `radii.css`, `elevation.css`, `motion.css`, `fonts.css`, `components.css` |
| `components/` | the React reference components (Stage, SlideTitle, IconTile, MonoLabel, Cursor, GlassPanel, CodePanel, SpecRow, DataTable, StepList, ProductWindow, ChatBubble, TaskCard, Pill, Stat, BarRow, Track), each with a `.d.ts` props contract and a `.prompt.md` (what, when, rules) |
| `guidelines/` | specimen cards for colours, type, radii, elevation, the backdrop and slide spacing |
| `ui_kits/sample-slides/` | five 1920x1080 sample slides, one per core layout |
| `_ds_bundle.js`, `styles.css`, `thumbnail.html` | the bundled components, the stylesheet entry point, the homepage tile |
| `design-skill.md` | the design system's own Agent-Skills entry point, renamed from `SKILL.md` so skill installers don't list it as a separate skill |

Fonts: Figtree and Geist Mono (OFL) are already in `assets/fonts/`.

**Snapshot:** copied unchanged (apart from that rename) on 2026-10-14 from the design-system project on Leon's machine
(`C:\cognaitiv-ai\design-system\leon-youtube`, last changed 2026-09-30). If the design system changes there, copy the
folder again into BOTH video skills (create-video-shorts and davinci-resolve-pro-edit) and rename its `SKILL.md` again.
