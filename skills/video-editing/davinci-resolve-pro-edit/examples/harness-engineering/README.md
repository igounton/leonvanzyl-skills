# The reference edit: "Harness Engineering" (YTHD60, October 2026)

The edit Leon called "a massive step up ... energetic, things move, constantly showing examples and B-roll", and
of the explainers: "even the slides, the software factory slides and animations ... absolutely spot on". This is
the bar. These are the real files that built it; copy their patterns (not their content) into the next video's
`W/scripts/gfx_<name>.py`.

| File | What it is |
|---|---|
| `make_plan.py` | the plan generator: 72 beats (34 zooms, 27 graphics, 3 keyword pops, 4 CTAs, 3 punch-ins, 1 flash patch), chapters, caption fixes, music (`file`, `under_voice_lu`), `sfx_prefer` |
| `make_zoom_specs.py` | zoom framings and marks for all 34 zooms (box / band / underline on the word) |
| `gfx_a.py` | graphics agent A: g01-g12 and r01-r03 (hook + level 1) |
| `gfx_b.py` | graphics agent B: g13-g21 and r04-r06 (levels 2 and 3, the software factory) |
| `GFX_BRIEF.md`, `BRAND_BRIEF.md` | the briefs the two long-lived graphics agents worked from (beats, cue words, assets, PiP rules, the brand pass) |

## Patterns worth copying
- **A continuous world over two beats** - `gfx_b.py` `factory()` (g20 + g21, the software-factory swarm): one
  function of "factory time" F renders both beats, each its own window of F, so g21's first frame is the frame after
  g20's last. Repos as white GitHub windows -> the Factory on glass -> the agent swarm (worker pool) on highlighted
  glass; issues fly as paper chips along glowing connectors, workers claim them (azure ring, spinner), the pool fills
  20/20, the next issue waits (ember pulse), one worker finishes (PR, checks passed in mint) and takes it. Every event
  is cued on a word with `W()`.
- **Concept diagrams that build word by word** - g02 (the three-level staircase with a crowd bouncing off locked
  level 2), g03 (levels unlock with the speaker's own slide icons), g04 (models dock into a socket), g05 (real tool
  calls, then a checks terminal ticking), g06 (hook events lighting up along the agent life cycle), g12 (the Stop-hook
  loop: blocked -> feedback -> fixed -> passes), g15 (a context budget at true scale), g16 (a harness stripped down,
  its meter rolling from ~30K to ~1.4K), g17-g19 (an org harness, an orchestrator, a long-running board).
- **Real sources** - r01-r03 and r06 (`capture_card` + `overlay` bands on the cited line), r04/r05 (`watch()`: the
  speaker's own YouTube watch page, band on the title), g14 (his channel with the real thumbnails and titles).
- **The brand pieces** - `tile()` / `robot_tile()` (his slide icons as glossy tiles), `win_head()` (product windows),
  `chip()`, `ring()`, `mint_check()`, `gh_label()`, line icons (`LINE` / `line_ico`), `PAPER` vs glass.
- **Custom per-frame UI** - everything time-driven lives in a `CFG_RENDER(t)` that is a pure function of t
  (counters, spinners, typing, chips flying along bezier paths), so renders are seek-safe.

Asset paths (`assets/b_*.png`, `captures/...`) are this project's; the research subagent captures the next video's.
Never reuse a sponsor's name or logo unless that video is sponsored by them (Leon removed "Upstash Box" from g20/g21:
the sponsor of an earlier video, not of this one).
