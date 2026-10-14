# Graphics brief (shared by every graphics subagent)

You build HyperFrames compositions for five vertical shorts (1080x1920, 60 fps) cut from Leon van Zyl's finished long-form
video "The 3 Levels of Harness Engineering (Beginner to Pro)" (AI coding agents: Claude Code, Codex, OpenCode, LangChain's
deep-agents CLI, Grok Code Fast 1, SMOL Coder, software factories, his 3D agent swarm "cubefarm"). This is the FIRST real
run of the upgraded skill: the graphics must match the long-form edit Leon called "a massive step up ... energetic, things
move, constantly showing examples and B-roll ... the software factory slides and animations are absolutely spot on".
Work autonomously; make every judgement call yourself and report it.

## Paths
- Work folder (run every command from here): `C:\Users\leon\Videos\Skool\YouTube\Media\Harness Engineering\shorts\work-The 3 Levels of Harness Engineering (Beginner to Pro)`
  (Git Bash: `/c/Users/leon/Videos/Skool/YouTube/Media/Harness Engineering/shorts/work-The 3 Levels of Harness Engineering (Beginner to Pro)` - QUOTE IT, it has spaces and parentheses)
- Python: `../.venv/Scripts/python.exe` (`$PY`). Bash is Git Bash on Windows: write longer code with a file tool, not heredocs
  (a `\n` inside a heredoc string becomes a real newline).
- Skill references (READ FIRST, all of them): `C:\Users\leon\.claude\skills\create-video-shorts\references\graphics.md` (start with
  "Theme"), `...\references\editing-spec.md` sections 4-6, `...\references\lessons.md` (HyperFrames + finished-edit + brand sections),
  `...\examples\gfx_s1.py`, `...\examples\prep_assets.py`, and `scripts/build_gfx_common.py` + `gfx/engine.js` here.
- THE QUALITY BAR, read it: the long-form edit's graphics code, `C:\Users\leon\.claude\skills\davinci-resolve-pro-edit\examples\harness-engineering\README.md`
  and its `gfx_a.py` / `gfx_b.py` (16:9; same engine and theme, re-lay the patterns out for 9:16). Their helpers (tiles,
  `win_head`, `chip`, `ring`, `mint_check`, `gh_label`, line icons, `CFG_RENDER` per-frame UI, the continuous `factory()` world)
  are yours to copy into your own module.
- `cut.json` (runs, word times) and `shorts.json` (the plan) are READ-ONLY for you.

## The source and what to grab from where
- The short's camera/voice come from the FINAL video `../The 3 Levels of Harness Engineering (Beginner to Pro).mp4` (3840x2160,
  60 fps, 969.8 s). It is a finished edit: most of its body is covered by the long-form edit's zooms and graphics, keyword
  pops, CTA cards. Do NOT grab UI stills/clips from it.
- Clean, unzoomed screen footage: the RAW recordings `C:\Users\leon\Videos\Skool\YouTube\Media\Harness Engineering\{2,4,5,6,7,8}.mkv`
  (3840x2160, 60 fps). `longform_program.json` maps the final video's time to them: `items[]` with `t0, t1` (final-video s),
  `file`, `src0, src1` (source FRAMES at 60 fps). Source time of final time t inside an item = `(src0 + (t - t0) * 60) / 60`.
  Key stretches (final-video time -> raw): the LangChain blog + leaderboard ~9:05-9:12 and the X post 9:17-9:32 (6.mkv items
  73-80), SMOL Coder CLI demo 11:21-12:02 and Claude Code `/context` 12:02-12:19 (6.mkv items 93-102), the cubefarm 3D swarm
  14:52-15:55 (8.mkv items 117-124: the 3D office, running to a monitor showing Claude Opus, the Kanban whiteboard, a GitHub PR).
- The raw recordings show Leon's webcam picture-in-picture TOP-RIGHT at x 3110, y 18, 698x944 (source px): never show it
  in a graphic. Crop UI away from it. LOOK at a frame before choosing a crop: `ffmpeg -ss <t-1> -i <raw.mkv> -ss 1 -frames:v 1 x.png`.
  Keep crops even-sized; re-encode clips with dense keyframes (`-g 12`) for HyperFrames.
- Real pages, already captured as 2x PNGs by the long-form research (reuse them, don't re-capture): `captures/` - see
  `captures/index.json` (file -> url, what it shows) and `captures/facts.json` (the fact check). E.g. `langchain_harness/`,
  `can_boluk_x/`, `can_boluk_blog/`, `systima_tokens/`, `ollama_ctx/`, `smol/`, `cubefarm/`, `software_factory_skill/`,
  `opus55/`, `fable51/`, `gpt6_models/`, `yt_watch_smol/`, `yt_watch_factory/`, `logos/` (official logos: claude_symbol, claude_code
  wordmark, openai / codex icons, cursor, deepseek, github, github_actions, ...).
- Prepared long-form assets (logos cut out, avatars, YouTube thumbnails, SMOL logo, Ollama, GitHub, Codex icon, OpenCode
  logos): `longform_assets/`. Copy what you use into `gfx/assets/` with YOUR tag prefix.
- Fact check notes that matter here: LangChain = deepagents-cli on Terminal Bench 2.0, GPT-5.2-Codex, 52.8% -> 66.5%
  (Top 30 -> Top 5). Can Bölük (@_can1357) X article "I improved 15 LLMs at coding in one afternoon. Only the harness
  changed." cover "The Harness Is the Bottleneck"; Grok Code Fast 1 6.7% -> 68.3%. Claude Code's harness ~30-33K tokens
  before the first message (Systima measured ~33K). SMOL Coder's whole harness ~1.4K tokens. Ollama's default context by
  VRAM: <24 GiB 4k, 24-48 GiB 32k. Show the TRUE numbers when a number is drawn; captions say what he says.
- NEVER Upstash (an earlier video's sponsor, not this one's): no Upstash name, logo or "Box". The software factory's worker
  pool is the "Agent Swarm" (Leon's own wording; the long-form used his mint Orchestrate robot tile for it).

## Your files (never edit anyone else's)
- `scripts/prep_assets_<tag>.py`: cuts your stills/clips into `gfx/assets/` with file names prefixed `<tag>_`, copies the
  captures/logos you use into `gfx/assets/`, writes `gfx/asset_dims_<tag>.json` (build_gfx_common merges them all).
- `scripts/gfx_<tag>.py` with a `build()` that writes your compositions with the exact ids given (e.g. `s1_r0`), using
  `build_gfx_common` (`words`, `W`, `page`, `capture_card`, `tile_html`, ...). Build with `$PY scripts/build_gfx.py <tag>`.
- Render only with `bash scripts/render_draft.sh <ids...>` (10 fps draft + `chk/<id>_sheet.png`: LOOK at it) and, after
  fixing, `bash scripts/render_full.sh <ids...>` (throttles itself machine-wide; wait for a `done <id>` line each).
  Never run prep.sh, finish.sh or compose.py.
- Check one full-resolution frame of anything with text (`ffmpeg -ss <t> -i gfx/out60/<id>.mp4 -frames:v 1 chk/<id>_t.png`)
  and the right-edge columns 1072-1079 against 1064-1071.

## Rules that matter most (the spec has the rest)
- Duration = the run exactly (`r['dur']` from `words(sk, ri)`); cue every move/landing with `W(ws, 'word')` (steps 0.25 s
  before the word). Times below are run-relative word starts from cut.json.
- Frame 0 is the composed landing state: sharp, camera at rest, the hero ALREADY ON SCREEN. Supporting cards land later.
- `split`: content in y 40-900 (main element's bottom edge at 880-900); world fades out from y 900 (built in). The caption
  band (941-1114) and the camera card (from 1200, Leon's head pops out above it) are drawn later: keep clear.
- `fv`: content above y 1230 (bottom edge 1200-1230); captions go in 1290-1560 below it. Real captures in the fixed capture
  frame (`capture_card`, x 24, y 200, 1032x1040) on the washed backdrop; the frame never moves, the footage pans/zooms inside.
- `*_r0` of every short is also the COVER frame: at frame 0 keep everything below y 620 (the glass title card sits at
  y ~262-603), then step/land so the hero's bottom edge ends at 880-900.
- The brand theme (default `stage`): graphite stage, glass panels for diagrams (`kind:'glass'`, `highlight:True` on the one
  that matters), white window/paper for real UI and pages, his glossy icon tiles, Figtree 600 + Geist Mono labels, azure
  accent (ember for limits/costs/"busy", mint for passes). Nothing under 30 px, including captured UI text the viewer must read.
  Highlight bands on real pages: class `band` (azure wash) under a `mix-blend-mode:multiply` screenshot, revealed with a
  `scaleX` reveal ON the word (audio adds a marker swish automatically).
- Animate the action, never label it. A product is its REAL UI doing the thing; anything that happened is its REAL page with
  the cited line highlighted. One dominant subject per scene, at most one supporting cue.
- Camera: glide / step / push (to ~1.6x) / pull, at most ONE whip per composition (whoosh at `t+0.45`). Never blur a word to be read.
- SFX on the CFG (run-relative): `pop` landing, `click` real press, `key` typing (one per keystroke burst), `chime`
  answer/success, `whoosh` whip only. Highlight swishes come automatically from `scaleX` reveals.
- Thumbnail moments: `thumb=[[a, b]]` on the CFG where the most eye-catching state is landed and still (one or two per
  composition worth a thumbnail, none on the rest). Every short needs at least one strong candidate (a split with his head
  under a bold real element is best).

## Compositions (run id, layout, duration, the words with run-relative start times, and the idea)

### Short s1 "Same model, 10x the score" (cover "Same model, / 10x the score")
- `s1_r0` split 4.10 s: He@0.07 managed@0.23 to@0.53 push@0.65 Grok@0.89 Code@1.21 Fast@1.49 1@1.99 from@2.15 only@2.47 6.7%@2.73
  Idea: the real chart from Can Bölük's article (captures/can_boluk_blog or can_boluk_x) or a true-scale bar: Grok Code Fast 1
  at 6.7% (ember), the bar starting to climb as he says "6.7%" (it reaches 68.3% in the fc run after, unseen - so land
  6.7% clearly). Cover-safe frame 0.
- `s1_r2` fv 7.35 s: I've@0 seen@0.16 ... examples@1.18 where@1.96 only@2.42 changing@2.77 the@3.32 harness@3.53 actually@4.31 took@4.61 the@4.85 same@5.10 model@5.41 and@5.92 improved@6.10 its@6.52 outputs.@6.78
  Idea: one model core (glossy tile / chip "same model") in harness A with a low score meter -> on "changing the harness" the
  harness ring swaps (glass panel morph) -> on "improved its outputs" the meter jumps (mint). The idea Leon's slide said:
  "Same model, better harness".
- `s1_r3` split 5.12 s: Like@-0.04 for@0.11 example@0.23 LangChain@0.75 did@1.23 this@1.39 experiment@1.61 a while back where@3.08 they took@3.38 GPT-5.2@3.56
  Idea: LangChain's real blog post (captures/langchain_harness) title card / logo landing on "LangChain", then the model chip
  "GPT-5.2-Codex" landing on "GPT-5.2".
- `s1_r5` fv 3.42 s: and@0 they@0.10 actually@0.32 managed@0.72 to get@1.48 better@1.76 results@2.14 out of the model@2.94
  Idea: the real LangChain blog capture (or the raw 6.mkv footage of it, ~9:05-9:12) in the capture frame, inner camera onto
  the deepagents-cli result line, band on "better results".
- `s1_r7` split 5.18 s: They were able to get the output from@1.27 a@1.41 53%@1.55 roundabout@2.75 to@3.37 about@3.55 66%.@4.23
  Idea: Terminal Bench 2.0 bars, same model: 52.8% (rest grey) -> 66.5% (azure, glowing), "Top 30 -> Top 5" as a mono label.
- `s1_r8` fv 5.25 s: Then there's this really popular@0.75 post@1.17 on X@1.69 from Can@2.21 Bölük@2.75 sorry if I'm butchering your name@4.78
  Idea: the real X post (captures/can_boluk_x or the raw 6.mkv footage of it ~9:17-9:28) in the capture frame; band on "The
  Harness Is the Bottleneck" (the very next line, in full cam, says "the coding harness ... was the bottleneck").

### Short s2 "30,000 tokens before you type" (cover "30,000 tokens / before you type")
- `s2_r0` split 7.05 s: Before@0.04 I've sent a single message@1.03 to Claude@1.52 it's already taking up over@3.46 30,000@3.78 tokens@4.88 of my context@6.02 window@6.54
  Idea: the REAL Claude Code `/context` screen from 6.mkv (~12:04-12:19 final time) in a window card (Claude Code is the
  Claude desktop app's Code tab or the CLI he actually shows - use what the footage shows), push onto the ~30K/36.2K usage
  on "30,000". Cover-safe frame 0.
- `s2_r1` fv 6.47 s: Typically your local@0.79 models@1.13 have a very tiny@2.21 context window@3.09 especially on consumer grade hardware@5.75
  Idea: a small local-model context window (Ollama logo + a short track/box labelled 32K, or the real Ollama context-length
  doc table from captures/ollama_ctx with a band on the VRAM rows).
- `s2_r2` split 5.50 s: If your entire context window@1.26 is only like 32,000@2.18 tokens or 64,000@3.67 tokens@4.67
  Idea: two true-scale context windows, 32K then 64K, as glass tracks.
- `s2_r3` fv 5.00 s: you cannot afford@1.10 to inject@1.92 Claude Code's@2.70 30,000@3.25 tokens@4.23
  Idea: the Claude Code harness block (~30K) drops into the 32K window: 94% full, ember warning; the long-form g15 did this in 16:9.
- `s2_r5` fv 7.05 s: So I decided to create this SMOL@1.41 Coder@1.75 harness@2.18 which strips@3.00 away@3.47 anything an open weight model will never need@6.65
  Idea: SMOL Coder's logo + real CLI (6.mkv ~11:21-11:44) then the strip: big system prompt, long tool list, MCP, sub-agents
  fall away (the long-form g16).
- `s2_r6` split 7.88 s: Open-weight models that run on your own hardware@1.79 will never need to run things like MCP@4.80 tools@5.32 or sub-agents@6.73
  Idea: a local machine / Ollama tile, then MCP tools and sub-agents cards struck off as he names them.

### Short s3 "What an AI agent actually is" (cover "What is an / AI agent, really?")
- `s3_r0` split 5.07 s: You've probably heard the word agent@1.53 so many times. But what exactly@3.65 is an agent?@4.64 Well,@5.02
  Idea: the word "agent" echoing (chips everywhere / a stack of real headlines using "agent") resolving to one question card. Cover-safe.
- `s3_r2` split 3.40 s: like your large language model@0.73 and your harness@2.59
  Idea: the equation on glass: Agent = Model + Harness (tiles: a brain/sparkle tile for the model, a code/shield tile for
  the harness - his slide icons), "model" landing on "model", "harness" on "harness".
- `s3_r3` fv 5.05 s: The model would be your large language model like@2.11 Opus@2.55 Fable@3.19 GPT-6@3.85
  Idea: real logos land on their names: Claude Opus 5.5, Claude Fable 5.1, GPT-6 (captures/logos, opus55, fable51, gpt6_models).
- `s3_r4` split 4.85 s: Those are the actual models@1.38 which basically form the brain@2.94 of the operation@3.96
  Idea: the model chip docks into the agent as its "brain" (the long-form g04 model socket).
- `s3_r5` fv 4.83 s: The harness@0.42 is the environment@1.84 in which that LLM functions@4.01
  Idea: the model sits inside a harness frame/environment (glass layers around it: rules, tools, checks, memory slots appear).
- `s3_r7` fv 3.10 s: It assigns the tools@0.76 that the agent should have access@2.39 to
  Idea: tool cards (write files, search, browse the web, open the browser) snap into the harness.
- `s3_r8` split 6.43 s: The harness also enforces the checks@1.80 that need to be executed like running test@4.14 suites@4.49 lint@5.19 type@5.75 check@6.05
  Idea: a checks terminal (paper/window) ticking: test suites ✓ lint ✓ type check ✓ (mint) on each word.

### Short s4 "20 AI agents, one factory" (cover "20 AI agents, / one factory")
ONE continuous world across all six compositions (copy the long-form `factory()` idea from gfx_b.py: one time function of
"factory time", each composition renders its own window), re-laid out for 9:16: GitHub repos/issues at the top, the Factory
(GitHub Actions) in the middle, the Agent Swarm pool (4x5 workers: Claude Code / Codex / own-harness icons) below.
- `s4_r0` split 3.83 s: A software@0.25 factory@0.71 is basically where you've got this agent@2.61 swarm@3.01 - cover-safe; the swarm pool is the hero.
- `s4_r2` fv 3.55 s: all sitting in the background@0.62 And these agents could be a mix@2.73 of agents@3.22 - workers idle/paused, then mixed icons.
- `s4_r3` split 6.60 s: You might have Codex@0.61 agents, you could have Claude@2.43 Code@2.75 agents, maybe even your own coding harness@5.85 - the Codex / Claude Code / own-harness workers light up on their names.
- `s4_r4` fv 7.38 s: These agents are just kind of waiting@1.12 for work@1.76 And what the software factory@3.27 will do is whenever you need to make a change@5.59 to any of your projects@6.71 - an issue gets the `ready` label and flies to the factory.
- `s4_r5` split 5.17 s: the software factory will allocate@1.57 that task to one of your available@3.34 coding agents@4.55 - the factory claims a free worker (azure flash), the issue docks into it (busy).
- `s4_r6` fv 2.17 s: If all of the agents in your swarm@1.18 are busy@1.68 - the pool fills to 20/20 busy; the next issue waits (ember).
(The next run is full cam: "the software factory will deal with it. It will actually wait until an agent becomes available...")

### Short s5 "My AI agent swarm in 3D" (cover "My AI agent swarm / in 3D")
Mostly REAL footage of cubefarm from 8.mkv (final-video 14:52-15:35 = items 117-121), plus the real repo/PR.
- `s5_r0` split 2.68 s: No one said an agent@1.01 harness@1.29 should be boring@2.12 - the most striking still/clip of the 3D office in a
  window card (cubefarm logo or the real README hero from captures/cubefarm as support). Cover-safe.
- `s5_r1` fv 7.58 s: This is my coding agent swarm@1.66 represented in 3D@3.27 space@3.79 And these guys are working on an actual project@6.98 - real footage in the capture frame, the inner camera gliding over the agents.
- `s5_r2` split 3.12 s: Each of these agents are running a coding harness@2.44 - a row of real logos (Claude Code, Codex, OpenCode) landing over a still of the office.
- `s5_r3` fv 8.23 s: So this could be Claude@0.84 Code it could be Codex@2.10 If I run to any of these monitors@4.12 I can actually see like this guy is actually running Claude@7.32 Opus@7.72 - the real footage of him walking to a monitor (8.mkv, final ~15:04-15:13), inner camera pushes onto the monitor showing Claude Opus.
- `s5_r5` fv 6.17 s: And this also uses the Kanban@1.37 board@1.97 And these are hooked up to actual GitHub@4.81 issues@5.43 - the real Kanban whiteboard footage (final ~15:22-15:30).
- `s5_r6` split 6.08 s: So when I click on any of these@1.63 we can actually jump to the actual pull@3.79 request@4.07 sitting on GitHub@5.57 - the real GitHub PR (from the footage ~15:30-15:35 or captures/cubefarm) in a window card above his head.

## Assignment
- Agent A (tag `a`): s1 (6) + s5 (6) - real sources and footage.
- Agent B (tag `b`): s2 (6) + s3 (7) - concept diagrams.
- Agent C (tag `c`): s4 (6) - the continuous software-factory world.

## Report back (short)
Per composition: what it shows, which real sources / frames (times) it uses, camera moves and whips, SFX events
(run-relative), thumbnail windows (and what is on screen in them), judgement calls, and that `render_full.sh` printed `done`
(with the contact sheet you checked). Render the drafts of ALL your compositions first, check them, then the full renders.
