# Short 01: "Same model, 10x the score"

- **File:** `final.mp4`, 1080×1920, 60 fps, H.264 High, AAC 48 kHz stereo, 47.133 s (2,828 frames).
- **Stems:** `stems/voice.wav`, `stems/sfx.wav`, `stems/riser.wav` and `stems/music.wav`. All run the full 47.133 s, 48 kHz.
- **Cover (frame 0):** "Same model, / 10x the score", written by me from the hook, since no title was given.
- **CTA:** the "Watch the full video" card (your rule: every short sends viewers to the full video), not a comment keyword.
- **Thumbnail:** `thumbnail.jpg` from 38.033 s (run 7, split): the Terminal Bench 2.0 chart for the same model, GPT-5.2-Codex, 52.8% before and 66.5% after (+13.7), with your head popping out above it and your eyes on the lens. Of all the candidates, the jumping chart says "same model, better score" fastest at feed size. It beat these candidates:
  - 3.183 s (run 0): the 6.7% Grok Code Fast 1 card, but your eyes are down
  - 16.633 s (run 2): the harness diagram, which has no face
  - 21.817 s (run 3): the sharpest face, but the LangChain title card says less than a chart that jumps
  - 43.067 s (run 8): the X post, dense text at feed size, no face
- **Full video:** "Harness Engineering: Make Any Coding Agent 10x Better", https://www.youtube.com/watch?v=z1EaBe9oIME. The URL is the video ID from your stats-for-nerds screenshot. The title is the live YouTube title, checked today (the file name says "The 3 Levels of Harness Engineering (Beginner to Pro)"). The TikTok and Instagram CTA lines use the live title. If you rename the video, update those lines in `PUBLISH.md`.

## 1. Inputs and sync
- **Source:** the finished long-form render, `The 3 Levels of Harness Engineering (Beginner to Pro).mp4`: 3840×2160, 60 fps, 969.8 s. Your webcam is the picture-in-picture at x 3110, y 18, 698×944 (safe area 674×920) throughout.
- **Clean voice:** the render has hook music, a riser and about 210 library SFX under your voice. So the voice comes from the long-form edit's dialogue stem (`voice_stem_YTHD60.wav`), patched in over the whole video with `clean_from_stem.py`.
  - Sync: one piece over 0–969.8 s at a 21.5 ms offset. The fit left out the stretches with loud music under the voice (0–53 s, 131–135 s and 956–966 s).
- **Transcription:** faster-whisper large-v3 with word timestamps and a prompt of the video's names. Every kept line was then force-aligned with wav2vec2 for the word edges.
  - Name fixes: "Bullock" → Bölük, "TARDIS" → "The harness", "scan ban" → Kanban, "cloud" → Claude.
- **Takes:** the source is a finished edit, so every line has one take and no swaps were needed.

## 2. The cut (source timecodes → short)
| Line | Source (s) | Text |
|---|---|---|
| L1 | 572.78–582.23 | He managed to push Grok Code Fast 1 from only 6.7% all the way to almost 70%, simply by changing how the underlying tools work. |
| L2 | 526.53–534.07 | I've seen a few very cool examples where only changing the harness actually took the same model and improved its outputs. |
| L3 | 534.34–539.48 | Like, for example, LangChain did this experiment a while back where they took GPT-5.2, |
| L4 | 539.90–551.62 | and it's exact same model with the same prompt, and they actually managed to get better results out of the model by using their own deep agent CLI tool, their own coding agent harness. |
| L5 | 552.05–557.13 | They were able to get the output from a 53% roundabout to about 66%. |
| L6 | 557.89–563.06 | Then there's this really popular post on X from Can Bölük, sorry if I'm butchering your name, |
| L7 | 568.66–572.38 | The coding harness, as he says here, was the bottleneck. (CTA) |

**Order and editorial trims:**
- **Hook first:** L1 (572.68 s, Grok Code Fast 1 from 6.7% to almost 70%) comes after L7 in the source. It opens the short as the hook, and the story then runs in source order from L2.
- **Dropped** between L6 and L7 (562.5–568.2 s): "but he was able to get really good results, again, just by changing the harness". The very next line says the same thing more sharply.

**Timing rules applied:**
- **Line start:** 40 ms before the first word.
- **Line end:** each line ends at its measured true end, and is cut earlier where the tail stays quiet for more than 150 ms. A 170 ms tail fade never runs past the next sound.
- **J-cut:** the audio leads each picture cut by 50 ms, and each caption chunk leads its word by 60 ms.
- **Pauses and joins:** pauses over about 220 ms inside a line are cut to 120 ms (60 ms kept each side), and every join is placed at 120 ms loud-to-loud.

**Verified on the final voice track:**
- A Whisper re-transcription of `voice.wav` reads the whole script with no clipped or stray syllables (misheard names aside).
- Quiet stretches over 150 ms: 220 ms at 5.94 s (after "70%,", your own pause); 220 ms at 19.59 s (after "back", your own pause); 230 ms at 41.51 s (after "Bölük,", your own pause). The longest is 230 ms. Every one is a pause between phrases inside a line; none is dead air at a join between lines.
- **Voice loudness:** -13.8 LUFS before a -0.2 dB gain, so −14 LUFS integrated, with a -0.3 dBFS peak.
- **END:** 47.133 s. Every layer ends exactly on it.

## 3. Eye contact
- **Calibration:** I calibrated on the outro. In this video your on-lens pose is the frontal one, so a head turned to the side means you are reading the screen.
- **Where the camera hides:** Runs 2, 5 and 8 are full visuals: there you read the LangChain post and the X article off the screen. The camera is back for the numbers you say to the lens: the hook ("6.7%" in a split, "almost 70%" full cam), "GPT-5.2", "exact same model with the same prompt", the 53% to 66% result, and the outro.

## 4. Layout plan (runs tiling [0, END])
| Run | Layout | Time (s) | Dur | Text |
|---|---|---|---|---|
| 0 | split (hook) | 0.000–4.100 | 4.10 | He managed to push Grok Code Fast 1 from only 6.7% |
| 1 | full cam | 4.100–9.500 | 5.40 | all the way to almost 70%, simply by changing how the underlying tools work. |
| 2 | full visual | 9.500–16.850 | 7.35 | I've seen a few very cool examples where only changing the harness actually took the same model and improved its outputs. Like, |
| 3 | split | 16.850–21.967 | 5.12 | for example, LangChain did this experiment a while back where they took GPT-5.2, |
| 4 | full cam | 21.967–24.600 | 2.63 | and it's exact same model with the same prompt, |
| 5 | full visual | 24.600–28.017 | 3.42 | and they actually managed to get better results out of the model |
| 6 | full cam | 28.017–33.067 | 5.05 | by using their own deep agent CLI tool, their own coding agent harness. They |
| 7 | split | 33.067–38.250 | 5.18 | were able to get the output from a 53% roundabout to about 66%. Then |
| 8 | full visual | 38.250–43.500 | 5.25 | there's this really popular post on X from Can Bölük, sorry if I'm butchering your name, |
| 9 | full cam (outro + CTA) | 43.500–47.133 | 3.63 | The coding harness, as he says here, was the bottleneck. |

**Camera geometry:** your webcam is a 674×920 picture-in-picture safe area, so:
- **Full cam:** the PiP is cover-fitted at about 2.08×, with light sharpening.
- **Split:** the webcam is scaled 1.29× from your measured hair top (webcam y 30–38) and lowest chin, so your whole face sits in the card and your hair pops about 95 px above its top edge.
  - The head above the card is cut out with Robust Video Matting (rvm_resnet50 on the GPU), from the same frame-exact clip as the card, so the two can't drift apart.
  - Split runs: 0, 3, 7.

## 5. Graphics (6 HyperFrames compositions, the brand "stage" theme)
All were rendered at 240 fps with per-frame directional motion blur, blended down to 60 fps, and checked on 10 fps draft contact sheets first. The look is graphite glass, Figtree / Geist Mono, azure / ember / mint accents and the horizon wave, with real captures in the white capture frame.

- **s1_r0 (split, hook):** a Grok Code Fast 1 pass-rate card from the edit benchmark. The true-scale bar lands at 6.7% in ember on "6.7%", with the "edit tool: patch" label. The top stays clear on frame 0 for the cover.
- **s1_r2 (full visual):** "Same model, better harness": one model tile in a harness ring with four tool tiles. The output meter sits low in ember, the harness lights up on "changing the harness", and the meter jumps to mint on "improved its outputs".
- **s1_r3 (split):** the LangChain logo and the real LangChain blog card, "Improving Deep Agents with harness engineering" (langchain.com/blog), landing on "LangChain". The "GPT-5.2-Codex" model chip lands on "GPT-5.2".
- **s1_r5 (full visual):** the real LangChain post in the capture frame. The inner camera moves onto the line about deepagents-cli going from 52.8 to 66.5 on Terminal Bench 2.0 with the model kept fixed (gpt-5.2-codex), with an azure band, then onto the leaderboard.
- **s1_r7 (split):** Terminal Bench 2.0 bars for GPT-5.2-Codex: 52.8% before (grey, Top 30) and 66.5% after (azure, Top 5), with a +13.7 mono label.
- **s1_r8 (full visual):** Can Bölük's real X article, "I improved 15 LLMs at coding in one afternoon. Only the harness changed.", with its cover image "The Harness Is the Bottleneck". The band lands on the cover just before you say "was the bottleneck".

## 6. Cover, captions and CTA
- **Cover:** frame 0 only, a graphite glass card with the title in white Figtree and an azure underline.
- **Captions:**
  - Burned in from the final voice track's aligned word timings, 1–3 words per chunk, white Figtree with a dark stroke.
  - Positions: in the split, between the card and your head; in full cam and full visual, the lower third; in the outro, centred at y 1250 so they clear your chin.
  - Highlights are glass keyword chips with an azure underline (never the old yellow serif): *Grok Code Fast 1*, *almost 70%*, *same model*, *LangChain*, *same prompt*, *66%*, *Can Bölük*, *bottleneck*.
- **CTA:** the "Watch the full video" card in the outro (box 43, 1344, 994×276). It has graphite glass, your azure play tile, the text typed in white Figtree 600 with a blinking azure caret, and an azure arrow button pointing down at the full-video link, pressed once the text is typed.

## 7. Audio
Levels are peaks relative to your voice peak. All sounds are from the skill's royalty-free library (CC0 and Mixkit; no attribution needed). No sound plays on layout cuts.

| Time (s) | Sound | Level | Source |
|---|---|---|---|
| 2.611 | pop: light | -14 dB | s1_r0 |
| 4.100 | sting: minimal hit | -10 dB | hook |
| 12.315 | pop: UI pop | -14 dB | s1_r2 |
| 15.646 | chime: success two-note | -12 dB | s1_r2 |
| 20.289 | pop: light | -14 dB | s1_r3 |
| 26.282 | highlight: marker stroke | -16 dB | s1_r5 |
| 27.423 | highlight: marker underline | -16 dB | s1_r5 |
| 37.376 | chime: success arpeggio | -12 dB | s1_r7 |
| 39.049 | highlight: marker stroke | -16 dB | s1_r8 |
| 40.511 | highlight: marker underline | -16 dB | s1_r8 |
| 41.734 | highlight: marker stroke | -16 dB | s1_r8 |
| 43.620 | pop: UI pop | -14 dB | cta |
| 45.650 | click: mouse click | -14 dB | cta |
| 43.950–45.138 | typing (the CTA text): 17 single real key strokes (key_laptop, key_mech_a, key_mech_b) | −20 to −22 dB | cta |

- **Riser:** "cinematic build" from the library, with its loudest moment exactly on the hook join at 4.100 s, at −12 dB. A minimal hit (sting) lands on the same frame.
- **Music:** the long-form hook track you picked, **cand_3** (ACE-Step 1.5 XL, seed 3307, uplifting cinematic, 105 bpm, D major). It starts 1.31 s into the track, so its lift lands on the hook join. You rejected s1's generated take 2 ("terrible"). Takes 1 and 3 are still in `music_takes/` to compare, and `cand_3 (in the short).mp3` is the track that's used.
  - Level: 15 LU under your voice (about −29 LUFS), sidechain-ducked about 5 dB more while you speak, with a 0.8 s fade-in and a fade-out that ends exactly on END.
- **Mix:** -13.9 LUFS integrated, -1.2 dBFS true peak.

## 8. Fact check (2+ sources each; the long-form research in `captures/facts.json`)
- **"Grok Code Fast 1 from only 6.7% all the way to almost 70%":** correct. Can Bölük's article reports 6.7% to 68.3% on his edit benchmark, by changing only the edit tool. Sources: x.com/_can1357/status/2021828033640911196, blog.can.ac/2026/02/12/the-harness-problem and stencil.so/blog/the-harness-problem.
- **The title's "10x":** 68.3 / 6.7 = 10.2x. True.
- **LangChain, "GPT-5.2 ... exact same model with the same prompt ... from 53% to about 66%":** slightly off. deepagents-cli went from 52.8% to 66.5% on Terminal Bench 2.0 (Top 30 to Top 5), with the model fixed at GPT-5.2-Codex, not plain GPT-5.2. The system prompt was one of the harness changes they made, so it wasn't quite "the same prompt". The captions keep your words; the graphics show the true model name and numbers. Sources: langchain.com/blog/improving-deep-agents-with-harness-engineering (Vivek Trivedy, 17 Feb 2026), zenml.io and startuphub.ai.
- **Can Bölük's post:** confirmed. It's an X Article (@_can1357, 12 Feb 2026) titled "I improved 15 LLMs at coding in one afternoon. Only the harness changed.", with the cover image "The Harness Is the Bottleneck". Its benchmark covers 16 models.

## 9. Judgement calls
- **How many shorts:** five, the most you allowed. Each is a self-contained idea from the video: the score jump, the 30K-token harness, what an agent is, the software factory and the 3D swarm.
- **Music:** you called s1's generated take 2 "terrible", so s1 uses the long-form hook track you picked, cand_3, instead of any generated take. Its lift is moved onto the hook join (details under Audio).
- **Caption fix (found while writing this report):** the "Can Bölük" chip at 41 s first rendered as "Can BÃ¶lÃ¼k". The pipeline scripts read the plan with Windows' default text encoding. I fixed the skill (every script now reads UTF-8, and the stage scripts run Python in UTF-8 mode), repaired the text in place without re-cutting, and re-rendered s1.
- **The hook** is the Grok result rather than the LangChain one: "6.7% to almost 70%" is the bigger, simpler jump, and it earns the title.
- **Captures:** the real pages are reused from the long-form research (captured fresh at 2x), and your UIs come from the raw recordings, never from the finished render, so none of the long-form edit's zooms or overlays show.
