# Step 1: Story, characters and locations, locked in

**Goal:** turn a few sentences of idea into a design the user has signed off, a full dialogue script, and the project memory that every later step and helper reads.

**Why it matters:** this is the cheapest place to change anything. In LAST CALL, a tough review of the first design found a sequence-break (the player could skip a key beat), contradictions between story rules, and a 35-minute runtime that had to be trimmed to 25. The main character's gender was also changed at the user's request. Each of these took minutes here and would have taken days later.

## Ask first

If the user hasn't given their idea, ask in plain chat: *"Tell me your game idea in a few sentences: where it happens, who you are, and what's going on."* Encourage a small setting. One building or one night is plenty.

Then ask about the frame with AskUserQuestion (skip anything they already answered):

- **Camera:** first-person 3D (Recommended: you only build the hands, it's great for atmosphere, and it's the quickest to polish) / third-person 3D / top-down or isometric / 2D side-on.
- **Length:** about 10–15 minutes / about 20–30 minutes (Recommended: room for a story arc and still small enough to polish) / 45 minutes or more.
- **Controls:** keyboard and mouse / keyboard and mouse plus gamepad (Recommended) / also touch screens and phones.
- **Tone or intensity**, phrased for their genre. For horror, for example: cozy and moderate (Recommended for a wide audience) / properly scary / very gentle.

If the idea leaves the mystery or twist open, also ask in plain chat whether they already know what's really going on, or would like you to draft options.

## Start the memory straight away

As soon as the frame is answered, create `docs/HANDOFF.md` from `assets/templates/HANDOFF.md`. Mark step 1 as in progress and record the frame answers in the decisions log. Also create `CLAUDE.md` containing `@AGENTS.md`, plus a first `AGENTS.md` from its template (title, pitch, rules). If the session ends mid-step, the next one can resume from there. Keep both updated as the design evolves.

## Draft, then ask about the draft

Write `docs/GAME_DESIGN.md`. Use these sections and keep each one tight:

1. **The pitch:** a paragraph, the tone, and the theme (what the game is *about* underneath).
2. **Characters:** name, role, want, voice in one line, and look in one line.
3. **The truth (spoilers):** what's really going on, plus the 2–3 **story rules** the world obeys. Later steps check everything against these rules.
4. **Core mechanics:** one **signature mechanic**, fun in its first 10 seconds and taught on purpose, plus the supporting verbs (explore, inspect, and so on).
5. **Locations / level map:** each space, what happens there, and how the spaces connect.
6. **Progression and gating chain:** who has what, and when. Audit it for soft-locks and sequence-breaks.
7. **Beat sheet** with target minutes for a *first-time* player, including puzzle-solving time.
8. **Set pieces for the genre:** the moments that define it. Horror has scares (each uses a different trick and is followed by a warm beat). Mystery has clues and deductions (each one fair, findable and legible). Comedy has gags, and action has encounters. Note which **genre director** will own them (scare director, puzzle or mystery designer, comedy director, encounter designer). It's created in step 6, but the design should already be written with it in mind.
9. **Cutscenes**, **key dialogue** (samples) and **endings**.
10. **Production principles:** everything visual built in code, all audio as static files, and the accessibility options.
11. **Decisions:** a log of what the user decided and when.

Before showing it, review it as a tough critic would. Look for plot holes, contradictions with the story rules, setups without payoffs, soft-locks, unrealistic minutes per beat, and anything too hard to build in code (offer a cheaper equivalent that keeps the magic). Fix what you find.

Then show a **short summary**: the story in 5 lines, the characters, the mechanic, the set pieces and the ending. Ask about everything still open, with options and a recommendation. Typical questions:
- Is the main character voiced: fully, a few key lines, or silent?
- Which of two possible twists or endings?
- Real-world flavour, such as where it's set (LAST CALL chose an American bar over a British pub, which gave it its title).

**Loop until the user explicitly says it's locked.** Don't move on before that.

## Once it's locked

1. **Write `docs/SCRIPT.md`**: every spoken and on-screen line in story order (template: `assets/templates/SCRIPT.md`). Each line has a stable id, the speaker, the line, a delivery note, a type (spoken, thought, hint, readable, UI) and a **status**: ✅ recorded / ⏳ not recorded / — not voiced. The status column is what stops anyone paying to record a line twice.
2. **Finish the project memory** from `assets/templates/` (read each template as you write its file):
   - `AGENTS.md`: the index of every doc, plus the ground rules, with the game's specifics filled in. **If the signature mechanic involves timing to sound or music** (rhythm, morse code, knock patterns, call and answer), add the music-sync rule now. Add the "every voiced line is heard" rule if characters speak. It's far cheaper to build these in from the start than to retrofit them.
   - `docs/HANDOFF.md`: the pipeline table (step 1 ✅), the decisions log and the demo list.
   - `docs/BACKLOG.md`: empty for now. Feedback arrives in step 7.
3. **Ask whether to use git** (Recommended: yes, with a commit after every step, so there's always a way back). If yes, `git init`, add a `.gitignore` (with `node_modules`, `.env.local`, `dist`, `captures`) and commit.
4. **Test the handoff (optional, but cheap):** a fresh helper that reads only `AGENTS.md` should be able to say what the game is, what's decided, what's done, and what's next. Fill any gaps it finds.

**Done when:** the user said "locked", `SCRIPT.md` exists, and HANDOFF shows step 1 done. Next: step 2, the visual debugging tool.
