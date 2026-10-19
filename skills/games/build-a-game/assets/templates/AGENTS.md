# AGENTS.md: {{GAME_TITLE}}

{{ONE_PARAGRAPH_PITCH}} A {{CAMERA}} {{GENRE}} game that runs in the browser (Three.js) and deploys as a static site. Playthrough: {{LENGTH}}. Input: {{INPUT}}.

This project is built with the `build-a-game` skill's 10-step pipeline. **Start here:** `docs/HANDOFF.md` (where we are and how to continue).

## Sources of truth (read before changing anything)

| File | What it is |
|---|---|
| `docs/HANDOFF.md` | Current step, decisions log, demo links, next steps |
| `docs/GAME_DESIGN.md` | Story, characters, mechanics, beat sheet, set pieces (approved {{DATE}}) |
| `docs/SCRIPT.md` | Every line in story order, with ✅ recorded / ⏳ not recorded / — not voiced. **Never re-record or edit a ✅ line's audio entry.** |
| `docs/DESIGN_SYSTEM.md` | The look: palette, materials, characters, motion, light, UI, budgets, acceptance checklist. Breaking it is a defect. *(step 3)* |
| `design/styles/{{CHOSEN_MOCKUP}}.html` | The design system's reference implementation. Port from it; don't reinvent it. *(step 3)* |
| `docs/TECH_PLAN.md` | Stack, architecture, quality gates, milestones *(step 6)* |
| `docs/LEVEL_LAYOUT.md` | Shared coordinates and named anchors *(step 6)* |
| `docs/BACKLOG.md` | Every playtest and review finding, with id and status |
| `.claude/agents/*.md` | The reviewers: critic, {{GENRE_DIRECTOR}}, narrative director *(step 6)* |

## Hard rules

1. **Files are the memory.** Update HANDOFF (and any doc you changed) after every step.
2. **Keep every demo working forever.** Mockups, the comparison page, the audition page, the talking-character demo and the frozen snapshots in `snapshots/` (never rebuilt or edited) are all listed in HANDOFF. "Clean-up" never touches them. If you change an API a demo uses, update the demo in the same change.
3. **Everything visual is authored in code** (Three.js and GLSL). No Blender, no downloaded models.
4. **No clipping, floating or z-fighting.** Contacts are verified numerically in each scene's `LC.selfTest()`, not just by eye.
5. **Determinism for review.** Every page exposes `window.LC` (see `tools/capture.mjs`), so any moment can be jumped to and captured exactly.
6. **Audio is static files only**, generated ahead of time through `tools/gen-audio.mjs` (dry-run first, then `--max-credits`). The game never generates audio or calls an API. Never pay twice.
7. **No secrets in the game.** `ELEVENLABS_API_KEY` lives only in `.env.local` (gitignored) and is read only by `tools/`. Never print it.
8. **Performance budget** (mid-range laptop, 60 fps at 1080p): ≤ 150 draw calls, ≤ 150k triangles per view, ≤ 3 post passes, ≤ 2 shadow-casting lights, ≤ 6 real lights, instance anything repeated. Judge by the budget, not the dev machine's FPS.
9. **Player clarity.** Every beat shows the **goal**, **where** to go, **how** to do it and **whether it's working**. Never ignore the player's input silently.
10. **Reviewed before the user sees it.** The critic reviews everything. The {{GENRE_DIRECTOR}} designs and reviews every set piece (it isn't done until `LANDS`). The narrative director reviews everything that carries story (it isn't done until `ON TRACK`). Fix BLOCKERs and MAJORs first. Every milestone gets a fresh-eyes playtest before the user plays.
11. **Never deploy or publish publicly without the user's explicit yes.** In autonomous mode, take the recommended option, log it in HANDOFF tagged "(autonomous)", and keep going, but never spend credits or publish.
12. **A few long-lived helpers, one per domain**, not dozens of tiny ones. Every agent pays a start-up cost.
{{OPTIONAL_RULES}}
<!-- Add when relevant:
- Music-synced gameplay: analyse the real beats (beat map, < 15 ms), one audio clock, the song pauses with the game, verified in real time.
- Every voiced line is heard: at the player's position, speech clears everything else by ≥ 8 dB; beds duck under speech; measured by a check.
- Every character line is voiced (thoughts and hints too); only UI and readables are subtitle-only.
-->

## Visual debug workflow

```bash
node tools/capture.mjs <page.html> --times 0,2.4,5 --views diorama,fp --out captures/<name> --selftest
```

This writes the frames, `_contact-sheet.png` and `report.json`. Look at the images: a scene isn't done until its frames look right and `selfTest` passes.
