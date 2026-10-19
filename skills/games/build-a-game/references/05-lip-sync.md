# Step 5: The talking-character demo

**Goal:** a close-up of a character speaking their recorded lines, with the mouth moving in time with the voice. It proves the character, the voices and the lip-sync work together before the slice depends on them, and it's a lovely demo to show.

**Skip it** if the game has no voiced characters on screen (the free audio route, or a voice-only narrator). Mark the step "skipped" in HANDOFF, with the reason.

## Ask first

AskUserQuestion:
- **Which character:** the main character (Recommended: the one players see most) / another speaker with the most lines.
- **Mouth movement:** smooth / snapping between mouth shapes like stop-motion (Recommended if the art style is stop-motion or puppet-like) / a toggle to compare both.

## Build `demo/lipsync.html`

- Reuse the character exactly as the design system defines it. **Build it into the game's source** (e.g. `src/characters/`), not as a one-off copy, so the slice uses the same rig and face. LAST CALL's demo used the game's own character code.
- **A face close-up** in the game's lighting.
- **A button per line** with the subtitle shown, plus a "Click to begin" gate (browsers block sound until the user clicks).
- **Mouth shapes from the timing data** saved in step 4. Map the characters' timestamps to a small set of mouth shapes (closed, open, wide, round, teeth on lip, and so on), with a slight lead so the mouth opens just before the sound.
- **Little life between lines:** blinks, a breath and small head motion, following the design system's motion rules.
- `window.LC` with `seek` and a `selfTest` that checks the mouth timing against the audio onsets (within one animation frame) and that no face parts clip.

Capture it at a few vowel peaks and the closed-mouth moments, check the frames, play it yourself, then give the user the link.

**Done when:** the user has watched it and the mouth clearly matches the voice. Add it to HANDOFF's demos. Next: step 6, the vertical slice.
