# Step 8: Build the rest of the game

**Goal:** build every remaining act with the same team, let the user play each act as it lands, and finish with a frozen, fully playable release candidate.

**Why it matters:** the slice built the shared systems, so the rest is many pieces that can be built side by side. This is where usage costs can explode, and where the user's play sessions keep finding the things that make the game good.

## Ask first

AskUserQuestion:
- **How to run it:** on its own, with a decisions log, pausing after each act for the user to play (Recommended) / check in at every decision. Autonomy never covers spending credits or publishing.
- **Usage:** lean (combined reviewer, fewer screenshots, fix only BLOCKERs per piece and MAJORs per act) / thorough. Recommend lean if they've mentioned limits.
- **Git isolation for parallel helpers** (Recommended if git is set up): each helper works in its own copy of the project and merges back.

## Pay down the slice first

Before going parallel, fix the shortcuts that would make helpers collide:
- **Every helper's brief** names the files it owns and the shared contracts it builds against (types, anchors from `LEVEL_LAYOUT.md`, the character and audio APIs). Everything else is read-only for it.
- **Add-a-file registries** for characters, rooms, systems, acts and capture scenarios.
- **Per-group audio files**: manifest, ledger and index fragments, so two audio helpers never write the same file.
- **One capture suite per area**, so each helper can prove its own work.

## Run it

- **A few long-lived helpers, one per domain**, each working through its whole list: audio (all remaining voices, sound effects and music), cast (the remaining characters), gameplay systems, world and set pieces, and performances and cutscenes. Each writes progress to a status file (`docs/production/status/<domain>.md`) and checks its own work against the design system and the script.
- **Then one integrator per act** wires the pieces into the beat graph and runs the act's suite. The reviewers check the act (the narrative director reads the whole act in order), then the fresh-eyes playtester plays it, then **the user plays it**.
- **Record the remaining voices batch by batch**, per act: dry-run, show the estimate, get a yes, buy with a cap.
- If the user is away (e.g. overnight), keep going with the recommended options, log each decision in HANDOFF tagged "(autonomous)", and never publish anything.

> **The expensive lesson:** LAST CALL's first production run split the game into 50 tiny units, each with its own builder, reviewers and fixer, up to 16 at once. It burned about 30% of a week's usage in a few hours, because every agent re-paid the start-up cost. It was stopped and replaced by about 8 domain helpers. Parallelism is good. *Agent count* is what costs.

## Rules that save whole fix rounds (add them to AGENTS.md now)

LAST CALL learned each of these from a play session. Build them in from the start:

- **Music the player keeps time with:**
  - analyse the real audio's beats with a beat analyser (tested first on click tracks with known answers) and drive the judge and cues from that **beat map**, never from a nominal BPM;
  - use **one clock**, the song's own playback position, compensated for output latency;
  - when the game pauses (the pause menu, a hidden tab, lost focus), **the song pauses too**, and everything resumes in sync;
  - schedule any parts played automatically on the music's clock, never on the player's tap;
  - verify in real time with a check that records what the player hears: under 15 ms.
- **Every voiced line is heard:** a check plays the game and measures each line at the player's position against everything else (≥ 8 dB clear of it). Music, crowd and effects duck under speech, and distant voices don't fade too far. In LAST CALL, 14 lines failed, one of them level with the room noise.
- **Guidance, game-wide:**
  - an objective line always on screen, in plain words (verb, object, place, control);
  - a how-to card the first time each mechanic is needed, which stays until it's done once;
  - the target glints after a few seconds, with an edge arrow if it's off screen;
  - hints at 15, 30 and 45 seconds stuck, plus a hint key;
  - check that every hint ladder really fires for a stuck player.
- **Interactions are measured:** pick-up, inspect, doors and drawers are checked frame by frame. Objects lift out of the world smoothly and go back where they came from, and the prompt only targets things you can use.

## When the user plays, they say how it feels

Encourage feelings over fixes: "the monster is too static", "the hands look like blobs", "picking things up feels glitchy", "make it creepier". For each one:
- give it to one focused helper (and to the genre director first for anything set-piece shaped);
- find the measurable cause;
- fix it;
- show a before/after.

## Release pass

When every act is in:
1. Make a production build. Run every gate once: the capture suites, the sync and dialogue checks if relevant, every chapter start, and **a bot that plays the whole game from New game to the end** in real time.
2. Fix what fails and re-run only that.
3. **Freeze the release candidate** in `snapshots/<milestone>/` on its own port, and smoke-test it (New game, a chapter start, each set piece, the ending).
4. Update HANDOFF and BACKLOG, list what's left for polish, and give the user the link.

**Done when:** the bot finishes the whole game with 0 errors and the user has played the release candidate. Next: step 9, polish.
