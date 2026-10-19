# Step 7: The user plays the slice

**Goal:** the user plays the slice in a real browser, says what feels off, and you fix the causes until it feels right. **Don't build the rest of the game until it does.** This is the most important review in the whole process.

**Why it matters:** only playing reveals feel. LAST CALL's first playtest produced about 19 notes. These included:
- "Everything looks blurred": the tilt-shift depth of field.
- "Can you actually leave the bathroom?": a door locked during a scripted moment looked broken.
- "What exactly is the gameplay mechanic here?": the core mechanic was never taught.
- "The beat from the jukebox isn't that loud": a rhythm cue was too quiet to play along with.
- "Is there a way to reset the game?": there was no New game or Restart.
- "The creature reveal could be scarier": that note created the scare director.

Four of these became project-wide rules (player clarity, no gameplay blur, never ignore the player's input, a fresh-eyes playtest every milestone).

## How to run it

1. **Open it for them:** give the link, the controls, roughly how long it takes, and one sentence on what they're testing ("does it feel good, is it clear, does the scare land"). Don't explain the puzzles. Their confusion is the data.
2. **Log every note** in `docs/BACKLOG.md`: an id, their words, the cause once you know it, and the status. Notes given mid-build get folded into the current pass, not saved for later.
3. **Ask when a note is ambiguous**, with options. ("Too dark: the whole room, or just finding the door?")
4. **Find causes, not symptoms.** LAST CALL examples:
   - "The crowd is gone after the cutscene" turned out to be a crowd never added to the room.
   - "Off-beat" was the bar's lights pulsing at a different tempo and a game clock slowly slipping away from the music.
5. **When a feeling is hard to pin down, measure it.** Build a readout the user can switch on (e.g. `?synclog=1`, with every tap's early/late offset and a Copy-log button) and ask them to play and paste the log. In LAST CALL, one log showed the cause at once: the character's drum hits started *on* the player's tap, so they were heard late, and the player kept chasing them.
6. **Fix in one focused pass**, with one helper per theme (clarity, look, audio) rather than per note. Then the reviewers and the fresh-eyes playtester run again, then the user replays.
7. **Turn general lessons into rules.** If a note would apply to every future scene ("the player didn't know what to do"), add it to `AGENTS.md` and the design docs so the rest of the game is born with the fix.

## When it feels right

- **Freeze a copy:** build the slice and copy the static output to `snapshots/m1-slice/`, served on its own port (add it to `.claude/launch.json`). It's never rebuilt or edited. The live game will change under the user while helpers work, and the frozen copy stays playable for comparison and for showing progress.
- Add the snapshot to HANDOFF's demos, and mark step 7 done with the user's sign-off.

**Done when:** the user says the slice feels right and the snapshot is frozen. Next: step 8, the rest of the game.
