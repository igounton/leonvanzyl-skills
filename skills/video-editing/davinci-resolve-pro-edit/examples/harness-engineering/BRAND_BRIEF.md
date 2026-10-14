# Brand restyle brief: every graphic moves to Leon's channel design system

Leon's verdict on the white-world look: it doesn't match his channel. His slides, the keyword pops (already approved:
"Now that looks cool") and now ALL graphics follow his design system "Leon YouTube"
(now bundled in the skill's `references/design-system/` - read `readme.md` and skim `tokens/*.css` and the component
`.prompt.md` files; don't modify anything there). He said: "I don't care about the time. It needs to be done right."

The graphics engine already has the theme (`theme: 'stage'` is now the DEFAULT for every page): the graphite stage
(stage-800 -> stage-950 gradient with an overhead spotlight), two soft light beams, the animated horizon WAVE of dots
glowing in the accent (Stage.jsx `paintWave`, time-driven) and the vignette are painted behind your world. Fonts and
tokens are loaded. See `scripts/build_gfx_common.py` (CSS + `tile_html`) and `gfx/engine.js` (`skin()`, `paintWave`).

## Building blocks
- Card kinds (engine): `glass` (frosted stage-800 at 62% + backdrop blur, white hairline, panel shadow, white text;
  `highlight=True` = accent hairline + bloom, on ONE card per scene), `window` (white product window, radius 22, the
  window shadow + hairline), `paper` (white card, radius 24, card shadow), `media` (screenshots, window shadow),
  `capture` via `capture_card(...)` (real pages: a white window frame on a DARK washed, blurred clone), `tile`
  (rounded 28 - prefer glass now), `plain`/`logo` (no skin).
- CSS classes in the page: `.display` (Figtree 600 140), `.h1` (96), `.h2` (54, panel statements), `.sub` (500 46,
  accent colour - the subtitle line), `.body` (30, text-secondary), `.caption` (22, muted), `.label` (Geist Mono 500
  22 uppercase 0.14em, muted; `.label.accent`, `.label.white`), `.mono` (Geist Mono code, with `.code-k/.code-s/
  .code-n/.code-c` token colours), `.ink` / `.ink2` (text on paper), `.pill` (+ `.mint` / `.ember` / `.neutral`, on
  paper only), `.hair` (a hairline divider), `.accent` / `.secondary` / `.muted`.
- CSS variables: `--azure #2F95FF`, `--ember #FF8A5B`, `--iris #9C7CFF`, `--mint #4FD6A0`, `--accent` (azure, or ember
  with `accent='ember'` in the CFG), `--text`, `--text-secondary #A3A6AD`, `--text-muted #7E818A`, `--hairline`,
  `--paper`, `--paper-2`, `--ink #111214`, `--ink-2 #5F636B`, `--azure-wash`, `--azure-ink`, `--mint-wash`, etc.
- Glossy icon tiles: `tile_html(color, glyph, size, tilt)` - colors azure|iris|ember|mint, glyphs code, arrow, check,
  shield, sparkle, bolt, bars, eyes (or pass your own white `svg`). They replace the CSS squircles you drew by hand
  (Configure = azure code, Build = iris bolt, Orchestrate = mint eyes/robot, Memory = ember bars, Checks = mint check).
- CFG options: `accent='azure'|'ember'` (one accent per scene; ember for costs, security, warnings, refusals),
  `wave=dict(level='low'|'middle'|'high', k=1.0)` or `wave=False` (keep it on - it's the signature; `k` 0.6 behind
  dense panels, up to 1.4 on sparse scenes), `theme='paper'` only as a last resort.

## Rules (from the design system, adapted to animated B-roll)
1. **Dark stage, light type.** No full-frame white backgrounds, no white "world". Explanations and diagrams live on
   `glass` panels; real product UI, chat transcripts, files, issues, repo cards and captures are white `window`/
   `paper` (text `.ink`/`.ink2`, status as `.pill`s, accent text on paper uses `--accent-ink`).
2. **Type:** Figtree 600 for anything read big (titles -0.03em, statements -0.025em), Figtree 500 accent `.sub`, body
   in text-secondary, Geist Mono uppercase `.label`s ("System 1 · Jev" style, middle dots), code in Geist Mono.
   Nothing below 22 px on the stage (pills inside paper may go to 14). No Poppins, no Instrument Serif.
3. **Colour:** azure is the accent; ember second (warnings, costs, blocked, the ✕ stamp); mint for passes/checks
   (replace #34C759 with `--mint`), iris and mint otherwise only on tiles. NO clay (#D97757 / #B25730 / #FBEEE8) and no
   pure red anywhere. The winner of a comparison is white or accent; the loser text-secondary.
4. **Highlights:** on paper/captures a band in `--azure-wash` under multiply (or `rgba(47,149,255,.18)`), on glass/dark UI
   `rgba(47,149,255,.22)` with the accent line; boxes/outlines in accent with a soft accent glow
   (`box-shadow: 0 0 24px rgba(47,149,255,.45)`). Connectors/wires: accent at ~70% with a glow when active,
   `--bar-rest #5A5D64` when idle.
5. **Layout:** the webcam lane stays clear exactly as before (fvp content left of x 1504; the bottom-left PiP beats
   mirrored). Text sitting directly on the bare stage ends above y≈780 (the wave's crest glows lower); anything lower
   goes on glass or paper.
6. **Real logos stay** (Claude, OpenAI/Codex, GitHub, Upstash...) - put them on paper chips or glass tiles; use the
   `_on-dark` variants on glass and `_on-light` on paper (captures/logos). Leon's real YouTube thumbnails/pages stay.
7. Keep everything that already works: the timings, cue words, camera moves, depth of field, the story of each beat,
   the SFX events. This is a restyle, not a redesign of the beat's idea - but where a beat only worked because of the
   white world (e.g. a white page as the whole scene), rebuild that scene the way his slides would show it.

## Procedure
1. Look at 2-3 of Leon's real slides first: `python scripts/look.py 212 240 2` (his "Agent = model + harness",
   "Three levels" and title slides; output in `look/`), so your scenes feel like his deck in motion.
2. Restyle your module (`scripts/gfx_a.py` / `scripts/gfx_b.py`), `$PY scripts/build_gfx.py <a|b>`, drafts
   (`render_gfx.sh draft`), `draftsheet.py` - LOOK, fix - then `render_gfx.sh full`.
3. Compose to NEW file names, because Resolve holds the current files open: `$PY scripts/compose.py <ids> --tag brand`
   -> `<id>_brand.mp4` in the media dir. (g02 is a split: its RVM matte is already in split/, just compose.)
4. Check one full-resolution frame of every beat (`compose.py <id> --tag brand --preview t` writes preview/ stills).
5. Report per beat: what changed visually, the file, anything you couldn't do. Don't touch Resolve, the plan timings,
   or the other agent's module.
