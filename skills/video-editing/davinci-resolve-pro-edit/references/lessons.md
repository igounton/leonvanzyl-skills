# Lessons (hard-won; read before improvising)

**From the shorts skill, still true here**
- **Word edges:** never cut or cue on raw Whisper times. The foundation cut verifies every cut by re-transcribing
  it; cues for beats use CrisperWhisper's word starts (~30-40 ms), which is plenty for a camera move.
- **Captures:** real pages are 2x PNGs; crops never include the webcam window.
- **Blend modes:** a light highlight band under a `mix-blend-mode:multiply` screenshot vanishes on dark UI. On dark
  UI use a translucent clay wash above the image (`zoom.py` chooses automatically for zoom marks). On a captured
  page, a multiply band inside a card's `overlay` did nothing and simply hid the text: the overlay layer is its own
  stacking context. Set `overlayBlend='multiply'` on the card instead (engine support added after the first test).
- **Frame 0 is the landing state** of every graphic, because it hard-cuts in over V1.
- **Split geometry:** the matte and the card come from the same decoded frames, so the head can't drift from the
  body; erode the matte 1 px; check one full-resolution frame of every split.
- **Windows shells:** in Git Bash, `\n` and `\b` inside a Python heredoc become real characters and break string
  literals and regexes. Write code with a file-writing tool, or patch with a script file.

**Long-form and Resolve**
- **Duplicate, never rebuild.** The first test's clean cut had two transitions (mTuber "Bounce" and "Through
  Screen") and whoosh sounds the user had added after the foundation cut. A rebuild from source ranges would have
  dropped them silently. `timeline duplicate` keeps everything.
- **Transitions change the structure dump:** a clip next to a transition reports its handle in its video source
  range (record 322 frames, source 344), the transition itself is a V1 item with no media, and V1 "overlaps" appear.
  What plays at record frame n is still `source_start + (n - record_start)`. Words said inside a handle are not
  heard; drop them. Never plan a beat across the transition.
- **Frames matter more than seconds:** snap every t0/t1 to the frame grid (`round(t*fps)/fps`); the beat's clip is
  exactly `t1 - t0` frames and lands exactly on `round(t0*fps)`.
- **The webcam PiP is part of the continuity.** Every zoom and every screen-scene graphic pastes the same frame's PiP
  back where V1 has it, with a rounded mask (inset 3 px, radius 5.6% of the width) so none of the screen behind
  its corners comes along. On the white world it also gets the spec shadow.
- **Zooms near the webcam:** the held-still PiP covers part of the zoomed view. Frame the target outside
  `look.py`'s red box. The source PiP area is inpainted once per V1 item so a zoomed view never shows a second face.
  That patch must stay under the held-still PiP, or the smudge shows. For a top-right PiP whose left edge is Xp and
  bottom edge Yp (source px, UHD), a zoom of k centred on fx,fy is safe when fx <= Xp - (Xp - 1920)/k and
  fy >= Yp - (Yp - 1080)/k (openai-dots: Xp 3074, Yp 1171). Outside that, move the target or skip the zoom.
- **Colour exactness:** zoom renders work on the source's own YUV planes and encode with the source's tags - a frame
  at rest is bit-identical to V1, so the cut in is invisible. ffmpeg's default YUV->RGB is bt601: never use it for
  footage that sits next to V1.
- **Windows pipes:** a default subprocess pipe moved raw 4K frames at 4 fps; a 64 MB pipe (`_winapi.CreatePipe`)
  did 16x better. Measure the pipe before blaming the encoder. The shorts skill found the other half of the story:
  Python's *buffered* reader is the slow part (`bufsize=10**8` read at 130 MB/s, the default or an unbuffered
  `readinto` at 1.6 GB/s). `media.py` reads unbuffered; never add `bufsize=` to a frame pipe.
- **HyperFrames workers are tabs of one Chrome by default** (`PRODUCER_ENABLE_BROWSER_POOL=true`), and that browser's
  single GPU process encodes every screenshot: more `--workers` barely helps. `render_gfx.sh` exports
  `PRODUCER_ENABLE_BROWSER_POOL=false` (one Chrome per worker) and captures lossless PNG frames
  (`--format png-sequence`); the MP4 path captures JPEG at quality 95, which measured 48.6 dB against the lossless
  frame on the cubefarm g03 beat (no right-edge strip at 3840 px, unlike the shorts' 1080 px). At 4K the PNG encode
  inside each Chrome is the cost: 8 workers captured g03 (1,349 frames) in 70 s, 12 in 62 s, 16 in 80 s, so 12 is
  the default and the script throttles to RENDER_SLOTS x HF_WORKERS browsers machine-wide. The old MP4 path took
  88 s in total and JPEG capture with 16 separate browsers 100 s: lossless is also fastest. The tmix output is NVENC
  lossless when an NVIDIA encoder exists (11 s vs 16 s for x264 crf 10 slow on g03, zero generation loss, same
  decode speed).
- **The matte on the GPU:** `hyperframes remove-background --device cuda` can't use CUDA on Windows (its
  onnxruntime-node build lacks it) and runs the CPU at 2-3 fps. `matte_gpu.py` runs the same cached u2net model on
  onnxruntime-gpu with the shorts' speaker-only cleanup (a horizontal opening drops thin strips that touch the
  head, then the largest blob is kept - the guitar-headstock case from the first test), lossless FFV1 out.
  `compose.py --matte` uses it and falls back to the CLI by itself.
- **Frames are pure functions of a small state.** The keyword pop and CTA overlays are drawn once per distinct
  state (landing progress, typed characters, caret, press) and written into a persistent transparent 4K frame as
  their own box; the split blend runs only on the columns right of the card's shadow. Both are pixel-identical to
  the per-frame code they replaced. Previews seek straight to the wanted frames instead of decoding the beat up to
  them - except the source footage, which `media.decode_at` decodes from the start of its contiguous run: a time
  seek to a single frame of an OBS recording (millisecond timestamps) lands one frame late, so a seeked still is
  not the frame the render uses. (`look.py` and `assets.py still` keep the direct seek: they are for looking and
  for assets, not frame-locked.) The PiP inpaint patch of a zoom is made from the beat's first zoomed frame of the
  V1 item, in renders and previews alike; with one process per beat, two beats on the same item no longer share
  whichever patch came first.
- **NVENC for intermediates:** Resolve re-encodes on delivery, so zoom and graphic clips use NVENC (cq 15) when
  available. x264 `-preset fast -crf 12` is the fallback.
- **GPU decode per seek is slower:** one CUDA context per short seek (scene sampling) cost more than it saved. Use
  it only for long sequential decodes, if at all.
- **Scenes:** OBS recordings switch between a full-frame camera and screen + PiP inside one file. Classify per item
  from 3+ samples (big centred face = camera). The PiP window edge scan can run off on some files; a consensus
  across files fixes it.
- **Punch-in framing:** YuNet face boxes put the eyes ~32% down the box. Put them on ~36% of the frame height.
  Resolve: zoom about the centre, Pan +right, Tilt +up, timeline pixels (measured).
- **Split scale:** a portrait webcam (the PiP) is narrower than the camera card. Scale it to cover the card when the
  whole face still fits (chin above y 1000) instead of filling strips with blur; limit the pop-out above the card to
  a band around the head.
- **Matting limits:** the salient-object matte can include an object touching the hair (a guitar headstock). Check
  the full-resolution split frame; choose a different beat for the split if it's distracting.
- **Mark rects:** `box` and `band` add 8 layout px of padding around the rect. Leave room, or the band grazes the
  next row (it did on the first benchmark zoom).
- **CTA URLs:** a long URL ran under the CTA button. `overlay.py` now shrinks the URL font (44 down to 30 px) until
  the whole URL fits left of the button.
- **Captions:** convert "five point five" to "5.5" and apply phrase fixes on the WORDS before cutting cues, or a
  number splits across two cues. Hotword mishearings ("agent-decoding", "Gentic Labs") go in `caption_fixes`.
- **Markers:** one per frame. A duplicated clean cut brings its own review markers (frame 0 was taken).
- **Levels:** the user's voice sat at -25.7 LUFS. The added layers are levelled against the voice, so the final
  -14 LUFS is one normalisation on delivery; don't touch A1.
- **The machine is shared:** the user may be rendering something else (a shorts session was compositing during the
  first test). Timings vary; keep parallelism reasonable and never touch processes you didn't start.

**Censoring private details** (openai-dots, 2026-10-01: a chat message with private business details, on screen
for two minutes while the chat scrolled)
- **Match words, trace the block.** Templates of the sensitive words, cut from one full-resolution reference frame
  and matched at half resolution (normalised cross-correlation), followed the message through reflowed lines,
  scrolling and dimming. The blur shape is a flood of the bubble's own flat colour from each hit, so it hugs the
  bubble, and a popup drawn over it (its own colour and border) stays sharp.
- **No pre-roll before the first detection.** The block fades in where the chat has just jumped, so a mask held back
  from later frames blurred the wrong bubbles. The faintest first frame is already detected; bridge gaps only
  between detections inside one V1 item.
- **Zooms carry their own blur.** An overlay can't follow a camera move, so `zoom.py` bakes the censor into the
  source planes before the move (from `censor/<id>_track.json`), and `censor.py render` leaves the overlay clear
  over zoom clips. Track before rendering any zoom inside the beat.
- **Transitions can't be followed from the source.** Render the transition's frames out of Resolve and let
  `censor.py transition` register each one against the last clean frame (ECC, affine), warp the mask onto it and
  widen it by the frame's motion. Check the incoming side by eye.
- **Scan the whole programme.** The same words can show up outside the beat (a notification, a later scroll back).
  `censor.py scan --gpu` decodes on NVDEC: CPU decoding of 4K for a full scan would starve the renders beside it.
- **Reference frames:** `censor.py ref` is frame-exact. The first reference was cut with a direct seek and came out
  one frame late (see "Frames are pure functions" above); harmless for matching, but measure boxes on the exact frame.

**Slide-deck talks** (ai-practitioners-summit, 2026-10-06: a 37-minute conference talk, 383 V1 items, mostly the
speaker's own dark slides plus GitHub/VS Code screens, webcam PiP top-right)
- **Check the PiP window by eye when scenes.py says "consensus".** Every file's edge scan ran off and the consensus
  came out 702x1008, but the real webcam was 704x950 (a one-column scan down x 3500 shows the PiP's bottom edge as a
  step to the flat background at y 957). A window that is too tall pastes a strip of unzoomed screen under the
  webcam in every zoom. Patch `files.*.pip` and `items.*.pip` in scenes.json before rendering anything.
- **A zoom can stay in one 'screen' scene and still cross a content change.** A V1 cut from a slide to a GitHub page
  is "screen -> screen", so the scene check passes. Look at a frame just after every V1 cut inside a beat
  (`look.py`) - four beats here ran onto a different page (a slide -> the repo listing, an agent panel closing, a
  "custom harnesses" slide -> a terminal). End the beat on the cut, or plan it on the new page.
- **An instant punch-in on a cut is `cam0`, not a `dur: 0` move at t 0.** The move version motion-blurs frame 0
  (the shutter samples the k = 1 state before it). `cam0: {fx, fy, k}` starts the clip at the tighter framing.
- **Read along with the slide.** On a talk built from the speaker's own slides, the strongest body beat is a zoom
  that follows the narration through the slide's rows - a box on each card or row as it is named, a band on the line
  being read - then pulls back before the next V1 item continues the same slide. 62 such zooms in 37 minutes read as
  calm, not busy, because each one only moves on a cue word.
- **Don't add a CTA card for something already on screen.** When the speaker says "install it with npx cubefarm" over
  the README's Get started block, zoom on the real line instead of typing the same command into a card.
- **Resources that criticise:** when the speaker is critical of a site ("the same one or two names, for the silliest
  of things"), show the site but crop it so no person's or publisher's name is readable.
- **Numbers in caption fixes:** the "five point five" -> "5.5" merge runs in the same pass as `caption_fixes`, so a
  phrase fix must use the spoken words ("Opus five point five": "Opus 5.5") to keep the name and number in one cue.
- **Removed beats leave event files behind.** `audio.py` now places SFX only for beats in the plan; before that fix, a
  CTA replaced by a zoom still got its pop, key ticks and click.
- **The user's own markers:** a duplicated timeline may carry the editor's markers on chapter-like frames; `place.py
  ids --existing-markers` nudges chapter markers one frame off them. Leave the user's markers alone.

**Explainer-heavy talks** (harness-engineering, 2026-10-13: a 16-minute theory video, 128 V1 items, slides + a VS Code
demo + browser sources, webcam PiP that MOVES between OBS scenes inside one file)
- **The PiP can change corners inside one file.** 5.mkv had the webcam top-right on the slides and bottom-left in the VS
  Code scene; `scenes.py` keeps one window per file, so its edge scan failed and the consensus was wrong for 24 items.
  Detect the corner per item (colourfulness of the two corner patches over 2 fps samples) and store `items.<v1>.pip`;
  the work-dir copies of zoom.py / compose.py / look.py were patched to prefer the item's window. Graphics on those
  items mirror the fvp layout (anchor [1136, 540], capture frame at x 416).
- **Scan the cut for flash frames.** The user's cut ended an item on 22 frames of another app window (a 0.37 s flash).
  A head/tail scan of every item (96x54 grey, frame diffs > 12) plus a frame-exact look found it; `patch_flash.py` holds
  the last clean screen and pastes the live PiP back each frame on PE Graphics - V1 stays untouched.
- **Overlapping SFX need more lanes.** Typing runs and pops from busy graphics overlap; one SFX track silently drops
  the later clip in Resolve. place.py spreads SFX greedily over "PE SFX", "PE SFX 2" and "PE SFX 3" (with the
  library's auto highlights and dings, two lanes still dropped 2 of 210 sounds; three dropped none).
- **Write edit_plan.json atomically.** A plan rewrite while overlay.py read it failed one beat (StopIteration).
- **Two long-lived graphics agents beat many small ones** (the user's preference: small agents burn tokens). One per
  half of the video, each with a written brief (beats, cue words with times, real assets to use, the PiP rules) and
  its own `gfx_<name>.py`; research findings are relayed to them by message as they land.
- **Explainers that worked:** a continuous "world" split over two beats (the software-factory swarm, g20 -> g21, one
  timeline function with an offset - the cut between them is invisible); true-scale bars for token budgets; the
  speaker's own slide icons rebuilt in CSS so the B-roll matches the slides; real watch pages / thumbnails for every
  "check out my video on ...".
- **Fact check feeds the graphics.** "A hook masks the prompt" is not what Claude Code settings hooks can do (block or
  add context only); the graphic showed a mod-style handler instead. Relay accuracy notes to graphics agents early.
- **Chrome (outside the Claude app) can't write into the app's virtualised AppData.** Re-capturing a page with the
  system Chrome needed a temp folder next to the media, then a copy into `captures/`.

- **Match the channel brand, not a generic style.** Leon's slides are built from his "Leon YouTube" design system
  (bundled in references/design-system/: tokens/colors.css, typography.css, elevation.css, radii.css and the
  component prompts). Overlays that sit on his footage (keyword pops; next: CTA cards, zoom marks) take its graphite
  glass, Figtree / Geist Mono and azure/ember accents. The keyword pop design is locked in editing-spec.md section 3.
- **Split mattes: RVM, not u2net.** u2net's salient-object matte is a soft low-res blob that swallowed the guitar behind
  his head on and off (flicker at the ear). Robust Video Matting (matte_rvm.py, ResNet-50 ONNX, ratio 0.4, warmed-up
  recurrent state) follows hair strands and leaves objects touching the head in the background. A guided filter and a
  background-plate difference key were tried first and failed (a light ghost of the guitar edge; the plate never saw
  the wall behind the hair). On Windows, onnxruntime-gpu needs the nvidia-*-cu12 wheels' bin dirs added to the DLL
  path (matte_gpu.py and matte_rvm.py do it) or cuDNN fails to load.

- **Restyle by re-rendering, then swap in bulk.** The brand pass re-rendered 34 zooms and 27 graphics under `--tag brand`
  and swapped all 61 with one `script_plugin run_inline` (Python: walk the media pool, `ReplaceClip(path)` on each id
  from import_result.json, `SaveProject()`) - seconds instead of 61 MCP round trips. Keep the old renders until the
  user signs off.
- **A rebuilt audio layer goes on new tracks.** Library SFX, auto highlight/ding/whoosh/sting events and a new music
  file move and change every sound, so replace_clip can't do it: `place_audio_swap.py` plans "PE SFX v2" ... tracks,
  one append_to_timeline of 212 rows (the reply overflowed the tool output and was saved to a file - parse it), then
  the old PE audio tracks are disabled and renamed "(old)". If only the music changes (same length), re-render it under
  a new tag and replace_clip the one music clip.
- **Generated hook music: the level matters as much as the track.** ACE-Step 1.5 XL (music_gen.py, MIT, ~15 s a
  90 s take on the 5090 once loaded) wrote four "inspirational" candidates; the pick sat 18 LU under the hook's voice
  and ducked another ~5 dB under speech - barely there. 15 LU under (`music.under_voice_lu: 15`) let the lift read.
  Generate 60-90 s, cut where the lift lands (`file_offset`), keep the alternatives for the user.
- **`timeline_frame capture` can hang.** One call blocked for 30 minutes (Resolve on the Edit page with a long
  timeline). Prefer a review render through the scripting API (`run_inline`: LoadRenderPreset 'YouTube - 1080p',
  SetCurrentRenderFormatAndCodec('mp4', 'H264_NVIDIA'), SetRenderSettings TargetDir/CustomName/FormatWidth/Height,
  AddRenderJob, StartRendering - it returns at once; poll GetRenderJobStatus) and decode frames from the file.
  SetRenderSettings returns False if any one key is rejected ('VideoQuality' as a number was) but applies the rest -
  read the job back with GetRenderJobList. Frame captures also reset the Deliver page's format to JPEG.

- **No sponsor that isn't this video's sponsor.** The swarm graphic named the worker pool "Upstash Box" with its
  logo, because the speaker's software-factory skill runs on it; Upstash had sponsored an earlier video, not this one,
  and Leon had it replaced with "Agent Swarm" before release. Brand names in explainers only when the speaker names
  them; a sandbox / hosting / tooling vendor he doesn't mention stays generic. Captured pages (watch pages, READMEs)
  may carry sponsor lines in descriptions: crop or frame them out.

**Scripted sponsor reads** (tripleten-midroll, 2026-10-15: a 94 s sponsor midroll read from a script, OBS screen + PiP)
- **When the speaker is reading the script, drop the webcam.** Items where V1 shows the script itself (a Google Doc) were
  recorded with Leon looking down at it, expecting full-screen text. He asked for g04 (planned as a split) and then g03
  (fvp) to be full-frame `fv` with no PiP: "you should not show my webcam there at all... it was like that in the script
  as well." Check the PiP on every item that shows the script / notes; plan those beats `fv`.
- **Cover any frame that shows the script.** Look for the script doc in scenes (it was 9 s of the hook here).
- **Fact-check the sponsor's claims too.** "Around two hundred practicing engineers" was on no TripleTen page; the graphic
  showed the community without a number and the report flagged it. A line the script had but the recording lacked
  (instructor employers) was true for one instructor only - show it on the one it's true for.
- **A lower third the script asks for** works as a body keyword chip with a label; place it clear of the page's own
  headline (the homepage headline sat bottom-left, so the chip moved right to xy 1450,905).
- **Long chip eyebrows:** a label wider than the words overflowed the chip - overlay.py now sizes the chip to the wider
  of the two.
- **Split from a PiP:** compose.py's automatic scale (card width only) left a fill band at the bottom; the agent set the
  scale in `split/<id>_geom.json` (2.2). geometry() should check bottom coverage too.
- **music_gen.py can fail with "Insufficient KV cache"** when another app holds GPU memory (LM Studio / ComfyUI were open).
  Check `nvidia-smi`, wait, retry - never touch the other processes.
- **AppData is virtualised for the app** (`...\Packages\Claude_...\LocalCache\Local\...`): W lives there; M must stay
  next to the sources so Resolve sees the files.
- **A midroll's publishing copy** is a sponsor block for the host video (the program and audit links), not a title or
  chapters; chapters on a midroll are section markers only.

## User feedback log
Add the user's reactions to each edit here so the rules keep improving.
- 2026-09-30, Sonnet 5.5 vs Opus 5.5 vs Fable 5.1 (test build "YTHD60 - Pro Edit TEST", hook + two body beats):
  the brief - music only under the hook and faded out right after it; the body restrained but with zooms,
  highlights, real sources and SFX. After watching the first 40 s in Resolve: "the edit was really good" - keep
  this hook treatment (two screen zooms with marks, a punch-in with one keyword pop, an fvp graphic, a split, the
  riser into the join). Body pacing not reviewed yet (only two sample beats were built).
- 2026-10-06, AI Practitioners Summit talk ("YTHD60 - Pro Edit v1", 37 min): the brief - "the video has already been
  cut, so do not cut it any further; the length is perfect ... make this look a bit more polished, as if a
  professional video editor worked on this." Reused the current timeline as the clean cut (no foundation cut, no
  re-cut, nothing on V1/A1 changed but one punch-in). Reaction to the result: not given yet.
- 2026-10-13, Harness Engineering ("YTHD60 - Pro Edit v1", 16 min): the brief - lots of theory without on-screen
  visuals, so "think like a professional video editor and add B-roll" wherever it drags: visualisations of how things
  work (the software factory swarm, task ingestion and allocation), real articles with highlighted text, screenshots
  of his own YouTube videos, official logos; don't re-cut. Built with 27 graphics and 34 zooms (far denser than the
  default body). Mid-run feedback: "doing a really good job so far"; prefers few long-lived subagents over many small
  ones; fixed the Skool page's wrong weekday after the fact check flagged it. Reaction to the finished timeline: not
  given yet.
  Follow-up the same day: the split's head pop-out "glitchy around my ear" (u2net grabbing the guitar) -> RVM matte;
  hook music "very boring, go for something more inspirational" -> a generated track (music_gen.py); SFX "bland and
  generic" -> a royalty-free sample library with highlight swishes, dings, whooshes and stings; keyword pops: the
  yellow serif "not professional for a tech channel", a white chip "not sure it matches the channel brand", then the
  graphite-glass chip from his design system: "Now that looks cool. Lock in that design."
  After the brand pass, the RVM split, the library SFX and the generated hook music (ACE-Step cand_1, 15 LU under the
  voice), watching the 1080p review render: "Wow, this looks next level. The masking around my hair is fixed. Editing
  seems polished, sound effects seem better and the music sounds cool." - this is the baseline for the next edit.
  Then, listening to all four music takes on their own, he swapped my pick (cand_1, indie electronic with guitar and
  marimba) for **cand_3, uplifting cinematic piano + staccato strings + steady drums**: "That's the one!" - now the
  default hook style in editing-spec.md section 6. Send the user every take as MP3s, not just the pick.
  Final verdict on this edit: "really, really professional-looking ... a massive step up from the types of edits you
  did with the same skill previously. The sound effects, the zooms, and the styles ... very cool." What made the
  difference, keep doing it: everything styled from the channel's own design system, B-roll wherever theory drags,
  real recorded SFX placed on every visual event, generated music chosen by the user, RVM for the head pop-out.
- 2026-10-15, TripleTen sponsor midroll ("YTHD60 - Pro Edit v1", 1:34): the brief - "make this look way more polished"
  after approving the clean cut ("you did a really good job"). Mid-run: "Please do not include music. No, wait. Ignore
  that. Add music" (kept hook music); no webcam on the script-reading lines (g03, g04 -> fv). Built with 9 zooms, 8
  graphics, 4 chips, 2 punch-ins, 59 SFX. Reaction to the finished timeline: not given yet.
- 2026-10-16, Harness Engineering, after release: retention "higher than my previous videos by a long shot", but a
  viewer wrote "the new sounds effects get annoying fast - ding, scribble, ding, ding, ding". Measured on the edit:
  12.6 sounds a minute in the body with no music under it, 35 dings (every box mark) and 31 scribbles (every
  highlight), 25 stretches with 4+ of them in 20 s, 97% landing on words. Peak-based levels put chimes ~2 LU and
  dings / pops / scribbles ~8 LU under the voice after the bus (the main-bus compressor lifted the effects ~4.5 dB;
  my earlier note that it kept the balance was wrong). An A/B/C on two 90 s stretches, with the bus emulated from the
  upload (0.98 correlation): B (8.2 a minute, dings 11, pops 31, quieter) "overcorrected slightly - I would have
  expected sound effects on some of those animations"; C (10.5 a minute, every animation keeps its pops, 20 dings
  15 s apart, scribbles quieter and tamed) "way better ... not too distracting ... not too dense". C is the default
  now (sfxlib LONGFORM_RULES / LONGFORM_TARGET). The lesson: trim the repeated accents, never the animation sounds;
  and measure what the viewer hears (after the bus), not what the files say.
