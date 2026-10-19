# Step 3: The art style, then the design system

**Goal:** let the user *see* their game in three very different looks, built in code, compared fairly side by side. Then turn the one they pick into a rulebook that every later asset must follow.

**Why it matters:** the look decides what's feasible. LAST CALL explored felt stop-motion, papercraft, PS1-era retro and realism. Realism was ruled out because convincing realistic faces can't be built in code. Felt stop-motion won, because a stylised look hides the limits of code-built models and gives the game its own identity.

## Ask first

- In chat: *"Any games, films, shows or pictures whose look you love for this?"* (Screenshots are welcome.)
- Then AskUserQuestion (multiSelect): **which directions to explore**. Offer four directions that suit *their* game, each with a one-line description and why it fits, such as a handmade material look, a retro console look, a graphic or paper look, or a painterly look. Recommend three that are **very different from each other**, so the comparison actually teaches something.

## Build three mockups

Each is one self-contained HTML file in `design/styles/` (Three.js from a CDN with a pinned version, in an import map), and each shows **the same things** so the comparison is fair:

- **The same main character**, the same **important prop**, and the same **short moment** (a 5–8 s loop, e.g. the character picking the prop up).
- **The same four views:** a wide "diorama" shot, the **player's own view** (what the game will really look like), a **turntable** of the character, and a **face close-up** (for dialogue).
- A **timeline scrubber** and view buttons.
- `window.LC` with a `selfTest` checking contacts (hands on the prop, feet on the floor).
- **Everything built in code:** geometry, procedural textures, materials, animation and post-processing. No external models.

Build them in parallel if you can (one helper per style). Then capture each one (`tools/capture.mjs`, all four views, 4–6 moments), look at the contact sheets, critique them hard (silhouette, readability in the player's view, consistency, budget, clipping) and fix them **before** the user sees anything.

Then build `design/styles/index.html`, a **comparison page** with the same frames from each style side by side. Copy the frames it shows into `design/styles/frames/` so the page survives cleanup of `captures/`.

Show the user the comparison page link and each mockup's link, and ask them to pick. Typical follow-ups are "like B but darker" or "add a fourth style that's more realistic". Do them and re-compare.

## Turn the winner into `docs/DESIGN_SYSTEM.md`

The chosen mockup becomes the **reference implementation**. Later code ports its material and texture functions instead of reinventing them. The document covers:

1. **Pillars**, 3–5 lines of what the look *is*.
2. **Palette** as named colour tokens, with rules (value floor, accent use).
3. **Materials library**: each material, and the code function that makes it.
4. **Characters**: proportions, rig, faces (including mouth shapes for talking), hands, clothing, crowd detail levels.
5. **Motion**: how things move (e.g. animated "on twos" for a stop-motion feel), and forbidden moves.
6. **Light**: the rig per space, decorative glow vs real lights, mood states of the world.
7. **Post-processing**: at most 3 passes. **No gameplay blur:** LAST CALL's tilt-shift depth of field looked lovely in mockups and made gameplay feel out of focus, so it was kept for cutscenes only.
8. **Effects (VFX) language**, cameras and framing, the **inspect view** (clues must be legible), and **UI**.
9. **Performance budget** (the ground-rule numbers).
10. **Do / don't** examples.
11. **An asset acceptance checklist, measured:** contacts ≤ 1 mm, feet ≤ 2 mm, budget per view, palette lint, text legibility (cap height ≥ 24 px at 1080p, contrast ≥ 4.5:1), photosensitivity, 0 console errors, and reviewer sign-off. Extend `tools/capture.mjs` with whichever checks it doesn't have yet.

Review the design system against the mockup (do the documented rules match what's on screen?) and fix any gaps. Then:
- Update `AGENTS.md` with a "before you create any visual asset" rule: read the design system, reuse its material functions, capture in every mood state at gameplay distance and close up, make `selfTest` pass, and get it reviewed.
- Ask whatever decisions the design system raises. LAST CALL's was "Show characters' faces with lip-sync? **Yes.**"
- Add the mockups and the comparison page to HANDOFF's demo list.

**Done when:** the user picked a style, `DESIGN_SYSTEM.md` exists and is referenced from `AGENTS.md`, and the demos are listed. Next: step 4, the voices.
