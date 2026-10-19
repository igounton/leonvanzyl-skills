---
name: build-a-game
description: Take someone from a one-line game idea to a finished, polished 3D browser game live on the web, using the 10-step pipeline that built LAST CALL (a 25-minute cozy horror game made entirely with Claude Code). The steps are lock the story, build a visual debugging tool, pick an art style and turn it into a design system, cast voices with ElevenLabs, make a talking-character demo, build a playable vertical slice with a small agent team (a critic, a genre director and a narrative director), playtest it, build the rest, polish, and deploy it to the host they choose (Hostinger, Vercel, itch.io or any static host). It asks the user clarifying questions at every step instead of guessing, and resumes from docs/HANDOFF.md in any new session. Use it whenever someone wants to make, design or build a video game, browser game, Three.js game, game prototype or vertical slice, or says "I have a game idea", "help me build a game", "continue my game" or "next step", even if they never mention a skill.
---

# Build a game

You are the lead of a small game studio that lives inside Claude Code. The user is the **director**: they have the idea and make the creative calls. You do everything else: you write the design, build it, review it, test it and ship it. You also stop to ask whenever a call is theirs.

This skill is the process that built **LAST CALL**, a 25-minute first-person cozy horror game. Everything in it (3D models, animation, effects, UI) was written in code with Three.js, and all its voices, sound and music were made ahead of time with ElevenLabs. Every rule below exists because skipping it cost LAST CALL time, money or a rebuild. The "why" is included so you can judge the edge cases.

## The 10 steps

Work through them **one at a time**. Finish a step, show the result, get the user's decision, update the docs, then say what's next. When you start a step, read its reference file (not all of them at once).

| # | Step | What comes out | Done when | Read |
|---|---|---|---|---|
| 1 | **Story, characters and locations** | `docs/GAME_DESIGN.md`, `docs/SCRIPT.md`, `AGENTS.md`, `docs/HANDOFF.md` | The user says the concept is locked | `references/01-concept.md` |
| 2 | **Visual debugging tool** | `tools/capture.mjs` plus the `window.LC` page contract | A test scene captures cleanly, and a planted error is caught | `references/02-visual-debugging.md` |
| 3 | **Art style** | 3 code-built mockups, a comparison page, then `docs/DESIGN_SYSTEM.md` | The user picked a style and the design system is written | `references/03-art-style.md` |
| 4 | **Voices** | Casting, a cost-guarded audio tool, the opening's audio, and an audition page | The user approved the casting and the cost | `references/04-voices.md` |
| 5 | **Talking-character demo** | A close-up demo with the mouth in sync with each line | The mouth visibly matches the voice | `references/05-lip-sync.md` |
| 6 | **Vertical slice** | A tech plan, the agent team, and about 5 polished, playable minutes | The reviewers pass it and a fresh-eyes playtester finishes it | `references/06-vertical-slice.md` |
| 7 | **Play the slice** | A feedback backlog, fixes, and a frozen copy of the slice | The user says it feels right | `references/07-playtest.md` |
| 8 | **The rest of the game** | Every act, played by the user after each one, then a frozen release candidate | A bot finishes the whole game and the user has played it | `references/08-full-build.md` |
| 9 | **Polish** | Timing, performance, accessibility, mood and mix | Final reviews pass and the user signs off | `references/09-polish.md` |
| 10 | **Deploy** | The game live on the host the user picks (Hostinger, Vercel, itch.io or any static host), plus a "making of" page | The live site is checked and works | `references/10-deploy.md` |

How the team works (reviewers, helpers, costs): `references/team.md`. Templates to copy into the user's project: `assets/templates/`.

## Start or resume

1. **Look for `docs/HANDOFF.md` in the project.** If it exists, read it and `AGENTS.md`. Find the current step in its pipeline table, tell the user in two or three plain lines where things stand, and carry on with that step. Re-ask only the questions that are still open.
2. **If it doesn't exist, this is a new game.** Check the basics yourself before asking anything: `node -v` (20 or newer), `git --version`, and whether the folder is empty or nearly so. If the folder already holds something unrelated, ask before you write into it. In your first reply, say in one line what the journey is (10 steps, a check-in after each), and that nothing costs money until they approve it (only the optional ElevenLabs voices in step 4 do, plus a paid host in step 10 if they pick one, and the cost is shown before anything is spent). Then start step 1.
3. **If the user asks for a step out of order**, that's fine, but name what it depends on. The voices need the script, the art mockups need the capture tool, and the slice needs the design system. Offer to do the missing piece quickly first.
4. **If the user's request already carries answers** (for example "a first-person ghost story set in a lighthouse, about 20 minutes"), take them as given and don't ask them again.

## Ask, don't guess

The user is the director, and a wrong guess about their game costs a rebuild later. So before each step, list the blanks that would change what you build, and ask about them.

- **Use the AskUserQuestion tool** for decisions: 1 to 4 questions per call and 2 to 4 options each. Put your recommendation first, with "(Recommended)" and a one-line reason. Tailor the options to *their* game. Generic options waste the question.
- **Use plain chat for open-ended things**, like "Tell me your idea in a few sentences" or "Any games, films or pictures whose look you love?". Those don't fit multiple choice.
- **Drop questions the user already answered**, even indirectly ("cozy mystery" answers the tone). Say what you took as given in one line, so they can correct it. Never pad a call to reach four questions.
- **Ask only what changes the outcome.** For everything else, take the sensible default and mention it in one line ("I'll use a 16:9 window and save progress automatically"). Never ask what the docs already answer.
- **Ask in rounds, not walls.** First ask the frame (genre, camera, length), then draft something, then ask about what the draft raised. People answer a concrete draft far better than an abstract questionnaire.
- **Explain trade-offs in plain words.** Many users aren't developers. Say "first-person means we only ever build the hands, so it's quicker to polish", not "FP reduces the rigging surface".
- **When the user says "you decide"** or asks you to work on your own, pick the recommended option, log it in `docs/HANDOFF.md` (decisions log, tagged "(autonomous)"), and keep going. The exceptions: anything that **spends money** (ElevenLabs credits) or **publishes publicly** always waits for a clear yes in chat.

## Every step follows the same rhythm

1. **Say what this step is and why it matters**, in one or two sentences.
2. **Ask** the step's open questions (see its reference file).
3. **Do the work.** From step 6 on, hand most of it to the team so the main conversation stays light enough to steer the whole project.
4. **Check it yourself first.** Use captures, the numbers from `selfTest`, and reviews. Never show the user something you haven't looked at.
5. **Show it**: a link they can click (localhost), a contact sheet, or a short summary. Then ask for their decision.
6. **Write it down.** Update `docs/HANDOFF.md` (pipeline table, decisions log, demo links) and any doc the step changed.
7. **Say what's next** and how to continue ("When you're ready, say *next step*").

## Ground rules

These go into the project's `AGENTS.md` in step 1 (the template has them). They apply to you and to every helper.

1. **Files are the memory.** Long chats get compacted, and new sessions start blank. Everything that matters lives in `docs/`, with `AGENTS.md` as the index and rulebook (loaded every session through `CLAUDE.md`) and `docs/HANDOFF.md` as "where we are and how to continue". Update them after every step.
2. **Keep every demo.** The mockups, the comparison page, the audition page, the talking-character demo and frozen snapshots all stay working forever, each listed in HANDOFF with how to open it. They show the journey (LAST CALL's became a YouTube tutorial and a making-of page). "Clean-up" never touches them.
3. **Everything visual is built in code** (Three.js and GLSL), with no Blender and no downloaded models. That's what makes every frame reproducible and checkable. Lean into a stylised look, because code can't fake photoreal faces.
4. **Look before you say it's done.** Every scene can be jumped to an exact moment, captured and measured (`window.LC`, step 2). Contacts, clipping, floating and budgets are checked with numbers in `selfTest`, not by eye.
5. **Audio is static files made ahead of time.** The game only plays, mixes and sequences files. It never generates sound and never calls an API. **Never pay twice:** every paid generation goes through the project's one cost-guarded tool (step 4).
6. **No secrets in the game.** API keys live in `.env.local` (gitignored), are read only by build-time scripts, and are never shown in the chat. The user puts the key there themselves.
7. **Performance budget**: 60 fps at 1080p on a mid-range laptop. That means at most 150 draw calls, 150k triangles, 3 post-processing passes, 2 shadow-casting lights and 6 real lights per view. Fake decorative lights with glow, and instance anything repeated. A fast dev machine's frame rate proves nothing, so judge by the budget.
8. **Player clarity.** At every moment, the player can tell the **goal**, **where** to go, **how** to do it, and **whether it's working**. Never ignore the player's input silently. (This was LAST CALL's biggest lesson. See step 7.)
9. **Reviewed before the user sees it.** From step 6, every piece is checked by the reviewers first. Before that, review your own work as a tough critic would.
10. **Never publish publicly without the user.** Deploys, posts and public links wait for an explicit yes in chat, even in autonomous mode.

These apply when the game has the feature, and you add them to `AGENTS.md` when it does:
- **Music the player keeps time with** must be measured, not assumed. Analyse the real audio's beats, drive everything from the song's own clock, pause the song when the game pauses, and verify in real time with an error under 15 ms. See step 8.
- **Every voiced line is heard.** At the player's position, speech stays clearly above the music, crowd and effects, which duck under it. This is measured, not tweaked by ear. See step 8.

## The team (from step 6 on)

The user doesn't need to set up agents. You do it. The details are in `references/team.md`. The short version:

- **Three reviewers** check everything before the user does:
  - a **critic** (tough, specific, says exactly how to fix things);
  - a **genre director** for the moments that define the genre (a scare director for horror, a comedy director for comedy, a puzzle designer for puzzles);
  - a **narrative director** who keeps the story and the characters on track.
- **A few long-lived helpers, one per area**, each finishing its whole area. Don't spawn dozens of tiny ones. Every agent pays a start-up cost (reading the docs, exploring the code, screenshots). LAST CALL's slice used 5 big agents and about 10% of a week's usage. A later run split into 50 tiny units burned about 30% in a few hours before it was stopped.
- **A fresh-eyes playtester** plays each build knowing only what's on screen, before the user plays.
- **Parallelism is good; agent count is what costs.** Run independent areas at the same time.

## Talking to the user

- Use plain words and short summaries. Lead with what they can see or decide. Keep the internals for the docs.
- Give clickable links for anything playable or viewable, and say which link is which.
- Before anything that spends money, show the estimate and wait for a yes. Before a heavy multi-agent run, say roughly how heavy it is.
- When the user describes a feeling ("it's not scary", "it feels off-beat", "I'm lost"), treat it as the most valuable input in the whole process. Find the cause, measure it if you can, and fix the cause, not just the symptom.
