# Step 6: The vertical slice (and the team)

**Goal:** plan how the whole game will be built, bring in the team, then build **one short, fully playable, polished section** (about 5 minutes) that uses almost every system: movement, the signature mechanic, a set piece (e.g. a scare), characters talking, music and sound, and the menus.

**Why it matters:** documents and mockups only tell you so much. One short play session of LAST CALL's slice surfaced seven problems that every document, mockup, review and test had missed. Finding them in 5 minutes of game is cheap. Finding them after building 30 minutes is not.

## Ask first

AskUserQuestion:
- **Which 5 minutes:** offer 2–3 stretches from the beat sheet. Recommend the one that touches the most systems, including the signature mechanic, a set piece and dialogue. (LAST CALL's: wake up in the restroom → the empty bar → pick up the drumsticks → the mechanic's first use → the realisation → the first scare → a mysterious phone call.)
- **How thorough the reviews are:** thorough (the reviewers each look separately, recommended if the user has plenty of usage) / lean (one combined reviewer, fewer screenshots, recommended if they're near their usage limit). Explain that this trades review depth for cost.
- **Tech stack:** TypeScript + Vite + Three.js, built as a static site that any web host can serve (Recommended; the host is picked in step 10) / something they prefer.

## Plan first

Write these before any game code, so parallel helpers build things that fit together:

- **`docs/TECH_PLAN.md`:**
  - the stack;
  - the source layout;
  - the key systems: one game clock (the audio clock for anything rhythmic), mood states of the world, rooms and culling, collision (a capsule against a simplified collision mesh, with no physics engine needed), characters (one rig builder with per-character data), audio buses with dialogue ducking, a narrative beat graph (each beat has enter conditions, objectives and checkpoints), and accessibility;
  - the quality gates for each milestone (below);
  - milestones (M0 foundation, M1 the slice, one milestone per act, a polish milestone, and deploy);
  - the slice's exact scope;
  - the audio budget against the credit ceiling.
- **`docs/LEVEL_LAYOUT.md`:** a shared map with real coordinates (metres) and **named anchor points** (door positions, the player's start, where each character stands). Every helper builds against the same numbers.
- **Add-a-file structure:** a new character, room, system or act is a **new file** that gets discovered automatically (e.g. Vite's `import.meta.glob` over `src/characters/cast/*.ts`). Nobody edits a shared list, so parallel helpers don't collide.

## The game's debug API

The game gets the same `window.LC` as the mockups, plus:
- `goto(beat)`: jump to any beat with the correct inventory and world state;
- `camera(pos, look)`;
- `state()`;
- a `selfTest` covering collision (the player can't get inside geometry), contacts, budgets and the registries.

Extend `tools/capture.mjs` to build or serve the game and run **scenarios** (named beats and views), grouped into suites per area.

## Bring in the team

Read `references/team.md`. Create the three reviewer agents in the user's `.claude/agents/` from `assets/templates/agents/`, filled in with *this* game's concept, story rules, characters and genre. Then run the build as a small pipeline of **a few big helpers**:

1. **Foundation:** the engine, the style module ported from the reference mockup, collision, input (keyboard, mouse and gamepad), save/checkpoints, the debug API and capture scenarios.
2. **In parallel, once the foundation lands:**
   - **audio** (wiring the recorded files into buses, spatial sound and ducking);
   - **world** (the slice's rooms, lighting and set dressing);
   - **characters** (everyone in the slice, built on the lip-sync demo's rig).
3. **Gameplay:** the signature mechanic, the set piece, dialogue and subtitles, objectives and UI, tying it all into the beat graph.
4. **Review → fix → verify:** the critic, the genre director (for the set piece) and the narrative director (for every line, clue and beat) review from real captures. Fix every BLOCKER and MAJOR, then check again.
5. **Fresh-eyes playtest:** a helper plays the slice knowing only what's on screen, and must finish it. Fix every moment it got stuck.

**Build player clarity in from the start** (ground rule 8). Each beat needs:
- an objective the player can see;
- a pull toward where to go (light, sound or a character);
- a one-time how-to card the first time a mechanic is needed, with keyboard *and* gamepad controls;
- immediate feedback for success *and* failure.

Also a **title screen with Continue and New game**, and a pause menu with **Restart**. LAST CALL's first playtest had none of these, and they all became fixes.

## Quality gates (every milestone, starting here)

1. The production build passes with no type errors.
2. The capture suite passes: `selfTest` (contacts, clipping, budgets), 0 console errors, every mood state captured.
3. The reviewers have no open BLOCKER or MAJOR findings. The genre director says the set piece **lands**, and the narrative director says the story is **on track**.
4. The performance budget is measured, including a software-GPU "weak laptop" run.
5. The fresh-eyes playtester completes it.
6. **Then** the user plays (step 7).

**Done when:** all six gates pass. Give the user the link (start the dev server, e.g. from `.claude/launch.json`), the controls, and how long it takes. Next: step 7, where they play it.
