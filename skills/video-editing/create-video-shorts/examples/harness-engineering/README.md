# The reference shorts: "Harness Engineering" (5 shorts, 14 October 2026)

Five shorts cut from Leon's finished 16-minute long-form edit ("Harness Engineering: Make Any Coding Agent 10x Better").
Leon's verdict: "You did an incredible job ... Everything is spot on." **This is the bar.** These are the real files that
built it. Copy their patterns (not their content), and look at `look/` to see what finished shorts look like.

| File | What it is |
|---|---|
| `shorts.json` | the plan: 5 shorts, their lines (source times), layouts, word-level camera switches, covers, highlights, music |
| `GFX_BRIEF.md` | the brief the three long-lived graphics agents worked from (the template's newer sections all come from it) |
| `gfx_a.py` + `prep_assets_a.py` | agent A, s1 + s5 (12 compositions): real sources and real footage |
| `gfx_b.py` + `prep_assets_b.py` | agent B, s2 + s3 (13 compositions): concept diagrams at true scale, real CLI / docs |
| `gfx_c.py` + `prep_assets_c.py` | agent C, s4 (6 compositions): one continuous software-factory world |
| `make_reports.py` | how the five `report.md` files were written: numbers from the cut / logs / JSON, judgement per short |
| `report_short-01.md` | one finished report (spec section 8) |
| `make_publish.py`, `PUBLISH.md` | the publishing copy for all five, with its length checks (now `scripts/check_publish.py`) |
| `look/s<N>_sheet.jpg` | the finished shorts, one frame every 2 s (the contact sheet `verify_final.py` makes) |
| `look/thumb_0<N>.jpg` | the five picked thumbnails |

Paths inside the files are that project's (`C:\Users\leon\Videos\Skool\YouTube\Media\Harness Engineering\...`).

## Choosing the moments (3-5 shorts, never more than 5)
| Short | Length | Runs | Hook | Payoff (the outro line) |
|---|---|---|---|---|
| 01 Same model, 10x the score | 47.1 s | 10 | a number jump: "Grok Code Fast 1 from only 6.7% ... almost 70%" | "The coding harness ... was the bottleneck." |
| 02 30,000 tokens before you type | 49.5 s | 8 | a surprising cost: "already taking up over 30,000 tokens" | "everything this model needs only takes 1,400 tokens." |
| 03 What is an AI agent, really? | 43.7 s | 10 | a question everyone has: "what exactly is an agent?" | "an agent is the model plus the harness." |
| 04 20 AI agents, one factory | 38.5 s | 8 | a scale image: "this agent swarm" | "wait until an agent becomes available before allocating the next task." |
| 05 My AI agent swarm in 3D | 45.3 s | 8 | a striking visual: "No one said an agent harness should be boring." | "built, tested, and verified." |

What made these the right five:
- **One self-contained idea each**, understandable with no context from the long video. Five different ideas, no overlap.
- **A hook with something concrete in it:** a number, a cost, a question, a striking image. When the best hook sits later
  in the source, it moves to the front (s1's hook is from 572 s and s2's from 726 s, after the lines that follow them).
- **The speaker's own summary line as the outro,** even from much later in the video (s3's outro is from 208 s, its
  body from 84-134 s). The short closes the loop the hook opened.
- **Things to show:** every short has real pages, UI or footage for most of its lines (articles, docs, the CLI, the 3D
  app). A moment that would only be talking-head plus generic diagrams is a weaker pick.
- **Asides cut, personality kept:** dropped the repeats and side notes ("All represented in 3D space.", the SMOL Coder
  demo detail), kept "sorry if I'm butchering your name".
- **38-50 s,** runs of 2.2-8.2 s, alternating split / full cam / full visual, never the same layout twice in a row.

## Patterns worth copying
- **Real sources wherever something happened** (agent A, `gfx_a.py`):
  - s1_r5 and s1_r8: the real LangChain post and the real X article in the capture frame, with the cited line banded on
    the word.
  - s5: real footage of the 3D app from the RAW recordings via `longform_program.json` (`import_longform.py --at`): the
    inner camera glides over it and pushes onto a monitor that shows `claude-opus-5-5`.
  - Logos land on names (`gchip`), and bands ride on moving footage through `vov()`, a root-level layer that copies the
    video's transform every frame. HyperFrames videos sit above the world viewport, so anything drawn over footage must
    be a root-level layer.
- **Concept diagrams at true scale** (agent B, `gfx_b.py`):
  - s2_r2 / s2_r3: context windows where one cell = 1K tokens. Claude Code's ~30K drops into a 32K window: 94% full, with
    "2K free" in ember. True numbers in the graphic; the captions keep the speaker's words.
  - s2_r5: the real SMOL Coder CLI, then a harness stack stripped down (`stack_blocks`).
  - s3: the equation tiles (Agent = Model + Harness), real launch pages landing on the model names, a checks terminal
    ticking mint on "test suites", "lint" and "type check".
  - The keyframe library (FX tracks as pure functions of t) makes every render seek-safe.
- **One continuous world across a whole short** (agent C, `gfx_c.py`):
  - `world()` is a pure function of the short's own time F, and every composition renders its own window of it. The
    story carries across the cuts, even over the full-cam run between r0 and r2.
  - The layout, top to bottom: repos as white GitHub windows, then the Factory on glass, then the Agent Swarm pool of 20
    workers. Issues fly as paper chips, workers light up on their names, and the pool fills 20/20 on "busy".
- **The brand everywhere:**
  - glass for explanations; white window / paper for real UI and pages
  - his glossy icon tiles (`tile()`, `robot()`, `harness_tiles()`)
  - Figtree 600 and Geist Mono
  - azure for the subject, ember for limits and costs, mint for passes
  - the glass caption chips, cover and "Watch the full video" CTA card
- **Sound:**
  - 12-17 library SFX per short plus the CTA typing (single real key strokes), one hit on the hook join, and a riser
    peaking on it.
  - Music generated per short in a style that fits the topic (cinematic, electro_pop for the tool demo, indie for the
    playful 3D office), 15 LU under the voice.
  - s1 uses the long-form's hook track (cand_3) after Leon rejected its generated take.

## Thumbnails (`look/thumb_0N.jpg`)
- **Best:** a split, with his head popping out above the one element that tells the story:
  - s1: the 52.8% → 66.5% chart (a chart that jumps beats a title card)
  - s2: the real `/context` screen with 36.2K circled
  - s3: the "Agent = Model + Harness" equation (mouth closed, eyes on the lens)
  - s4: the swarm with the Claude Code workers lit
  - s5: the 3D office with the harness logos
- **Rejected:**
  - frames without his face (unless nothing else exists)
  - dense text pages, which read as texture at feed size
  - eyes down or mid-blink
  - title cards that say less than a result

## Process and time (RTX 5090; graphics on 3 agents in parallel)
- **Setup and ingest:** setup 10 min (first-time installs), `analyze.sh` 2 min (123 s for the 16-minute 4K master), `import_longform.py` about 1 s
  (here it was done by hand).
- **Plan and cut:** the plan and cut for 5 shorts, then `brief_runs.py` for the brief.
- **Graphics:** 3 long-lived agents, 31 compositions, about an hour each, all in parallel. Each rendered drafts of all
  its compositions first, checked the contact sheets, then ran the full 240 fps renders. Never one agent per few
  compositions (Leon: few long-lived agents).
- **Meanwhile:**
  - `music_takes.py` for all five shorts: 3 takes each, one model load.
  - `prep.sh` for all five: 29 camera clips in 29 s, then 16 RVM mattes in 4.6 min (slowed by GPU contention with the
    music generation; much faster on an idle GPU).
- **Finish:** `finish.sh` about 70 s per short, then the thumbnail pick, the reports and `PUBLISH.md`.

## What went wrong and is now fixed in the skill (details in `references/lessons.md`)
- **On-lens pose:** here the frontal pose was the lens, the opposite of an older note. Calibrate on frames.
- **Camera switch times** snapped a word early from the batched transcript; they now come from the ALIGNED words.
- **One-word caption flashes** at line starts; now there's a 60 ms J-cut lead.
- **The outro caption** sat on his chin; it moves to y 1250.
- **"Bölük" turned into "BÃ¶lÃ¼k"** in a caption chip (Windows cp1252). The scripts now read UTF-8, and
  `check_text.py` stops `finish.sh` on garbled text.
- **The full video's live title** differed from the file name. Read it with YouTube oEmbed (spec 8b).
- **A rejected music take:** play a given track (`music.file` + `file_offset`), not a regenerated take.
- **No sponsor** that isn't this video's sponsor (no Upstash anywhere).
