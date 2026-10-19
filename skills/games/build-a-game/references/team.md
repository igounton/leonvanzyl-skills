# The team: reviewers, helpers and costs

You set the team up in step 6. The user doesn't have to. This file covers who's on it, when each one runs, and how to keep it affordable.

## The reviewers (they check everything before the user does)

Create these in the user's project at `.claude/agents/`, from `assets/templates/agents/`. **Fill in the placeholders** with this game's concept, genre, story rules, characters and tone, so each reviewer judges against *this* game, not games in general. All three return a verdict, ranked findings (BLOCKER / MAJOR / MINOR, each with *what's wrong → why it matters to the player → the exact fix*) and a short Keep list of what must survive.

| Reviewer | Owns | Passes with | Runs on |
|---|---|---|---|
| **Critic** (`game-critic.md`) | Everything a bit: fidelity to the brief, tone, story logic, player clarity, pacing, mechanic feel, feasibility, performance, visual correctness, accessibility | `SHIP` (or `REVISE` with no open BLOCKER or MAJOR) | Every piece, every act, every milestone |
| **Genre director** (`genre-director.md`) | The moments that define the genre. Horror: a **scare director** (scares led by sound: silence, misdirection, the hit, the aftermath, a warm beat after). Comedy: a comedy director (setups, timing, callbacks). Puzzle: a puzzle designer (fairness, the "aha"). Action: an encounter designer. | `LANDS` | Designs each set piece *before* it's built (a spec in `docs/<set-pieces>/`), then reviews it *after*, from captures and event logs |
| **Narrative director** (`narrative-director.md`) | Story coherence, character voice, setups and payoffs, continuity, the emotional arc. It also improves weak lines inside the approved story. | `ON TRACK` | Every piece that carries story (lines, cutscenes, set pieces, rooms with clues, on-screen text) and every finished act |

Rules for reviewers:
- **Use real evidence:** contact sheets, `report.json`, event logs, subtitle dumps. They look at images and don't assume the build matches the docs.
- **Reviewers specify; builders build.** The genre director writes only its specs, and the narrative director edits only the script, the backlog and the decisions log. Neither touches game code.
- **Story changes stay proposals.** Anything that changes the plot, a rule, the ending or a logged user decision goes to the user. So does re-recording a ✅ line, because it costs credits.

## The fresh-eyes playtester

Spawn it fresh for each milestone. It knows **only what's on screen**: no docs, no code, no debug jumps. Give it a prompt like:

> You're playing a browser game for the first time. You know nothing about it except what's on screen. Play it with the real controls (keyboard and mouse) by looking at screenshots, from New game until it ends or you're truly stuck. Report every moment you didn't know the goal, where to go, how to do something, or whether it was working, with a screenshot and what you tried. Don't read any files in the project.

Everything it reports gets fixed before the user plays.

## The helpers (they build)

- **A few, long-lived, one per domain.** Each learns the codebase once, then works through its whole list, and brings back a short summary. Typical domains are foundation/engine, audio, world (rooms and lighting), cast (characters), gameplay systems, performances and cutscenes, then one integrator per act.
- **Each owns its files.** Its brief lists the files it may write and the shared contracts it builds against. Everything else is read-only for it. Add-a-file registries mean nobody edits shared lists.
- **Parallel where independent.** Voice recording and room building don't depend on each other, so run them at the same time. Integration waits for the pieces it wires.
- **Status files** (`docs/production/status/<domain>.md`) let you, the user and a future session see progress without reading transcripts.
- **Use the strongest model available and set the effort explicitly:** high for builders, extra-high only for the hardest integration, and medium to high for reviewers.

## Keep the main conversation light

The main conversation is the director's chair: it plans, asks the user, dispatches helpers and reads summaries. Investigation, code reading, edits, captures and fixes go to helpers. That keeps the main conversation from overflowing on a long build, and the project memory in `docs/` lets anything resume after it's compacted.

## Costs

Every agent pays a start-up cost before doing any work: instructions, tools, reading the docs, exploring the code and screenshots.

| Approach | LAST CALL's cost |
|---|---|
| The whole vertical slice, 5 big agents | ≈ 10% of a week's usage |
| The first production run, 50 tiny units with builders, reviewers and fixers, up to 16 at once | ≈ 30% in a few hours (stopped) |
| Replaced by ≈ 8 domain helpers | The rest of the game |

**Lean mode**, when the user is near their limits:
- builders on high effort;
- one combined reviewer (critic, genre and narrative lenses together) on medium;
- review only the pieces that are visual or carry story;
- per-piece fixes for BLOCKERs only, with MAJORs deferred to the act's fix pass;
- one fresh-eyes playtest per milestone;
- at most about 6 images per review (use contact sheets).

Tell the user roughly how heavy a run will be before starting it.
