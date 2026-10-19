# Step 9: Polish

**Goal:** take the release candidate from "works" to "feels finished". That means the right length, smooth on an ordinary laptop, accessible, atmospheric, well mixed and clear from start to finish.

## Ask first

AskUserQuestion (multiSelect): **what bothers you most right now?** Mood and lighting / knowing what to do / smoothness and performance / sound mix / difficulty / something specific. Their answer sets the order. Everything below still gets checked.

## The polish pass

- **Timing:** a bot plays start to finish. Estimate a first-time player's time (bots are faster, and LAST CALL's bot took about 25 minutes where a first-timer needs about 30). Compare it with the target from step 1, and trim or extend the slowest or emptiest beats.
- **Performance on an ordinary laptop:** capture every beat with the software-GPU run, check the budget in every view (including the worst look angles), and fix the outliers. Never judge by the dev machine's frame rate.
- **Accessibility:** each option must really work, with a capture or test per option:
  - subtitles (size, background, speaker names);
  - reduced intensity or scares, reduced flashing and photosensitivity-safe (no more than 3 full-frame brightness swings over 20% per second in any mode);
  - reduced motion;
  - control remapping (keyboard and gamepad);
  - colour-blind-safe cues;
  - for rhythm, an assist and latency calibration;
  - sensitivity, invert-Y and field of view.
- **Mood:** a focused lighting pass. LAST CALL kept its opening warm on purpose and made everything after a few warm pools of light in a cold, murky dark. It added a small reusable set of light cues (dim, flicker, frost) with flashing limits built in. Prove the goals stay findable by measuring each objective's contrast against its surroundings, before and after.
- **Clarity:** a fresh-eyes playtester that only reads the screen gets from start to finish without the chapter menu.
- **Mix:** rerun the dialogue-audibility check. Music, ambience and effects sit under speech everywhere.
- **Final reviews:** the critic, the genre director and the narrative director (a full-story read in order), then the user plays the final build.

Freeze the polished build as a new snapshot (`snapshots/<milestone>/`), add it to the demos, and update HANDOFF.

**Done when:** the reviewers pass it, the user signs off, and the snapshot is frozen. Next: step 10, deploy.
