# Graphics brief: "Harness engineering" pro edit

You are a motion designer on a professional long-form YouTube edit (Leon van Zyl, 16:10, 4K60). The speaker explains
theory over static slides for long stretches; your graphics are the B-roll that SHOWS how things work. Leon asked for
explainer visualisations wherever the talk drags, real assets (official logos, real pages, his real YouTube videos),
highlighted text on real articles, and the feel of a professional editor's work.

Work dir W = `C:\Users\leon\AppData\Local\video-pro-edit\harness-engineering__YTHD60` (run everything with W as cwd).
Skill (read-only) = `C:\Users\leon\.claude\skills\davinci-resolve-pro-edit`.

## Read first (all of it)
- `SKILL/references/graphics.md` - the engine API (CFG, cards, camera moves, depth of field, captures, splits, SFX, render loop)
- `SKILL/references/editing-spec.md` sections 3 (gfx), 4 (geometry), 5 (graphics style), 6 (SFX) - the style contract
- `SKILL/references/lessons.md` (graphics-related bullets: frame 0, blend modes, split geometry, render throttling)
- `SKILL/examples/gfx_example.py` - a worked config to copy patterns from
- `W/gfx/engine.js`, `W/scripts/build_gfx_common.py` - what the engine really does (CFG_RENDER for custom per-frame UI)
- `W/edit_plan.json` - the beats (t0/t1 are fixed: never change them; ask the lead if a beat's timing can't work)
- `W/transcript.txt` - what is said; `python scripts/words.py t0 t1` prints word start times (programme seconds)

## Style (non-negotiable)
Luxury tech: ONE bright world of floating white cards on the near-white radial ground, a camera that moves through it,
Poppins, ink #111, clay #D97757 (#B25730 for clay text on white), band #FBEEE8, green #34C759, red #FF3B30, the
three-layer card shadow, nothing under 30 layout px of text, sparse scenes (one dominant subject, at most one
supporting cue), eased motion, never frantic. Animate the action, never label it: no pills or text rows that restate
the narration - show the thing (a real file, a real tool call, a real logo, a number filling a bar). Short real-looking
UI text inside cards (file names, tool calls, a prompt, a label on a git branch) is fine and encouraged.
Leon's own slides use glossy squircle icons: blue `</>` (Configure / Instructions), purple bolt (Build / Tools),
green robot (Orchestrate) / green check (Checks), orange lines (Memory). Re-create those as CSS squircles (gradient +
white glyph) wherever the three levels or the harness parts appear, so the B-roll ties to his slides.

## Hard rules
- **Frame 0 is the landing state**: the clip hard-cuts in over V1, so frame 0 shows content with the camera at rest.
  Things may land later (`land.t > 0`), never at t = 0.
- **Cues sit on words**: use `W(ws, 'word')` from `words(bid)`. A move starts 0.25 s before the word that names its
  target; a landing/mark lands on the word.
- **Layouts / the webcam corner** (layout px, 1920x1080):
  - `fvp` with the PiP TOP-RIGHT (most beats): the webcam occupies x 1554-1906, y 9-483. Keep content in x 64-1504
    (anchor [784, 540], capture frame x 64, y 72, 1440x936 - `capture_card(..., mode='fvp')`).
  - `fvp` with the PiP BOTTOM-LEFT (beats r03, g10, g11, g12 - the VS Code / Claude app stretch): the webcam occupies
    x 9-361, y 597-1071. Mirror the layout: content in x 416-1856, `anchor=[1136, 540]` in the CFG, and build the
    capture card by hand at x 416, y 72, 1440x936 (centre 1136, 540) instead of `capture_card(mode='fvp')`.
  - `split` (g02 only): content in x 64-1176; `compose.py g02 --matte` then `compose.py g02` adds the camera card.
  - Nothing important within 48 px of any edge.
- Real over invented: logos from `W/captures/logos/` (being collected right now by a research agent) or the previous
  project's `C:\Users\leon\AppData\Local\video-pro-edit\ai-practitioners-summit__YTHD60\captures\logos\` (Claude
  Code wordmarks, Claude symbol, OpenAI symbol, GitHub, Ollama, LM Studio are there already). Page captures, YouTube
  thumbnails/pages and facts arrive in `W/captures/` with `captures/index.json` (what each file shows, passage y
  ranges) and `captures/facts.json`. If an asset you need is not there yet, build the beats that don't need it first
  and come back. Copy assets into `W/gfx/assets/` and record sizes with `assets.save_dims` (see `scripts/assets.py`).
- SFX (`sfx` in the CFG, beat-relative): one per meaningful visible event - `pop` when a card lands (one pop for a
  batch of small things, not one each), `click` on a visible press, `key` while text types, `chime` on a pass /
  confirmation, `whoosh` only on a whip (at most one whip per graphic). Leave silence where nothing meaningful lands.
- Text must be crisp at rest: check one full-resolution frame of every beat.
- Never touch DaVinci Resolve, `edit_plan.json` timings, other agents' gfx modules, or anything outside W.

## Your loop (per beat; batch several beats per command)
1. Write your module `W/scripts/gfx_<yourname>.py` with a `build()` that calls `page(...)` per beat (see the example).
2. `$PY scripts/build_gfx.py <yourname>` -> `gfx/<id>.html` (PY = `C:\Users\leon\.venvs\pro-edit\Scripts\python.exe`).
3. `bash scripts/render_gfx.sh draft <ids...>` -> `$PY scripts/draftsheet.py <id> 8` -> LOOK at `chk/<id>_sheet.png`,
   fix, repeat. Check: frame 0 landing state, cues on words, bounds clear of the webcam corner, nothing important
   blurred at rest, legible type.
4. `bash scripts/render_gfx.sh full <ids...>` (throttled machine-wide; another agent renders too - always go through
   the script, never a bare `npx hyperframes render`).
5. `$PY scripts/compose.py <ids...> --jobs 2` -> the finished clips in the media dir (`project.json` media_dir).
   Then `$PY scripts/compose.py <id> --preview <t>` for one full-resolution frame per beat and LOOK at it
   (`preview/`), and `$PY scripts/draftsheet.py <id> 8 --full`.
The machine is shared (other GPU/CPU jobs run): don't start more than 3 full renders of your own at once.

## When done
Reply with: per beat - what it shows, which real assets it uses, the cue words/times, SFX, and the output file; plus
anything you could not do. Keep the module and html so the lead can make edits later.

---------------------------------------------------------------------------------------------------------------------
## The beats

### Agent A (hook + "what is an agent" + Level 1): g01 g02 g03 r01 g04 g05 g06 r02 g07 g08 g09 r03 g10 g11 g12

**g01** fvp 5.55-15.55 - "You install Claude Code (6.31), Codex (6.99) or OpenCode (7.79), you configure the model (9.73),
you add a few memory files (10.89), maybe a few hooks (12.43), a few tools (13.25), and you think that's it (14.79)."
The harness you're handed. Three product tiles (official logos: Claude Code, Codex, OpenCode) - Claude Code visible at
frame 0, Codex and OpenCode land on their names, camera steps across. Then push onto a settings-like card for the chosen
harness where rows snap in as named: model ("Opus 5.5" picker), memory files (AGENTS.md / CLAUDE.md chips), hooks
(a `Stop -> verify.sh` row), tools (shell / edit / web icons). On "that's it" everything settles with a soft green check.
Hook energy: something changes every ~1.5-2 s.

**g02** split 15.55-23.72 - "But in reality that's only level one (17.25-18.19) of Harness Engineering. And most people
building with AI (20.56-21.80) never get past it (22.04-23.34)." Three level cards as a staircase (1 Configure lit;
2 and 3 frosted with lock glyphs - don't reveal their names, g03 does). Push onto level 1 on "only level one"; a crowd
of small person dots drops onto level 1 on "most people" and bumps against the edge of level 2 on "never get past it".

**g03** fvp 40.0-45.5 - "...you do need to understand the three levels (40.91-41.19) of Harness Engineering, which we will
cover in this video." Frame 0: the three level cards side by side, 2 and 3 still locked (continuity with g02). On
"three levels" the locks pop and all three resolve: 1 Configure "Shape a tool you already use" (blue `</>`),
2 Build "Write your own harness on a model API or SDK" (purple bolt), 3 Orchestrate "Run a harness around many agents"
(green robot) - his slide's wording. Gentle push to finish.

**r01** fvp 77.2-82.6 - "We're also running a special at the moment that's one hundred dollars off your annual plan
(79.05-80.85)." Only if the research capture of skool.com/agentic-labs/about shows the price/annual plan: the real page
in the capture frame, band on the price. If no price is public, DON'T build it - tell the lead (it becomes a CTA card).

**g04** fvp 96.63-107.10 - "The model would be your large language model like Opus (99.37), Fable (99.95), GPT-six
(100.79). Those are the actual models which basically form the brain (105.09) of the operation." A model "socket"
card at the centre (visible at frame 0, empty, faint glow); three model cards land on their names (Claude symbol +
"Claude Opus 5.5", Claude symbol + "Claude Fable 5.1", OpenAI symbol + "GPT-6"); on "brain" one docks into the socket
and it lights up (clay glow), camera pushes in.

**g05** fvp 117.20-137.13 - "It assigns the tools (118.20) ... like the ability to write files (122.22), search for files
(123.08), browse the web (124.57), open the browser (126.07)... The Harness also enforces the checks (129.72) ... like
running test suites (132.48), lint (133.66), type check (134.38), you've probably seen these before."
An agent session card (Claude Code style transcript, mono): tool calls appear on their words -
`Write(src/app/page.tsx)`, `Grep("useAuth")` / `Glob(**/*.ts)`, `WebFetch(nextjs.org/docs)`, a browser call with a
small browser-window thumbnail. On "checks" step to a checks card (terminal look): `npm test  42 passed` (132.48),
`eslint .  0 problems` (133.66), `tsc --noEmit  no errors` (134.38) - green ticks land on the words, chime on the last.

**g06** fvp 140.20-159.27 - "These are certain events (141.23) that happen throughout the agent's life cycle (143.85)
that we can hook into (145.75). Like maybe the moment we send a prompt (148.49) to an agent, we first want to run a
custom script (151.13) that will check that prompt for any sensitive information (153.75) and will mask (155.85) that
information before it reaches the actual agent (158.69)." Phase 1: the real Claude Code hook events on a life-cycle
track (SessionStart -> UserPromptSubmit -> PreToolUse -> PostToolUse -> Stop - confirm names in
`captures/cc_hooks`), lighting in sequence; clay hook glyphs drop onto the nodes on "hook into". Phase 2: push onto
UserPromptSubmit: a prompt card types "Deploy to staging with my key sk-live-XXXX-XXXX-XXXX" (obviously fake), a
`mask-secrets.sh` script card lands between the prompt and the agent on "custom script", the key gets a red band on
"sensitive", flips to `••••••••` on "mask", and the masked prompt slides into the Claude agent card on "reaches".

**r02** fvp 161.90-172.28 - "And in fact Claude recently released Claude Mods (163.78). And this allows you to kind of
customize your Claude Code experience (166.03-167.77). But under the hood, Claude mods are basically using hooks
(171.20-171.60)." The real Claude Mods page (`captures/claude_mods_blog` / `claude_mods_docs`, see index.json for
passage y ranges): the inner camera moves to the passage, band on the "customise" sentence on "customize", then on
the hooks mention on "hooks" if the page has one (else keep the first band).

**g07** fvp 175.40-183.37 - "This will be your AGENTS.md (176.22) file. The DESIGN.md (178.19), SOUL.md (179.26). Or even
files within the docs folder (182.14)." Document cards land as named (AGENTS.md with the agents.md mark if collected,
DESIGN.md, SOUL.md); on "docs folder" a docs/ folder card opens and small files fan out (his real ones: GAME_DESIGN.md,
SCRIPT.md, TECH_PLAN.md, LEVEL_LAYOUT.md, HANDOFF.md).

**g08** fvp 186.75-197.53 - "...the harness should work within a very specific workspace (189.79), or it should only be
allowed to create new work trees (192.63) and feature branches (193.45) and never be allowed to change the main branch
(194.87-196.80)." A dashed workspace boundary with the agent inside (on "workspace"); a git graph: `main` with a lock,
a worktree folder card and a `feature/...` branch splitting off with commit dots (on "work trees" / "feature
branches"); on "never ... main branch" an arrow from the agent toward main hits a red ✕ stamp and is refused.

**g09** fvp 244.23-256.00 - "This is where you use a coding harness that was built by the provider (247.53) or some
third-party tool (248.93-249.73). For example, if you're using Claude Code (251.59), you are at this level
(253.29-254.13)." Provider-built tiles land on "provider" (Claude Code / Anthropic, Codex / OpenAI, Gemini CLI /
Google); third-party tiles on "third-party" (OpenCode, Cursor). Push onto Claude Code; a level-1 badge (the blue `</>`
squircle with a "1") lands on it on "this level".

**r03** fvp, PiP BOTTOM-LEFT, 290.87-299.90 - "This does not just apply to Claude at all. The AGENTS.md file is actually an
open standard (295.36-295.55). Any coding harness that's worth using will honor (299.12) this AGENTS.md file."
The real agents.md page (`captures/agents_md`): band on the "open format" sentence on "open standard", then the inner
camera moves to the wall of agents that support it on "honor".

**g10** fvp, PiP BOTTOM-LEFT, 301.18-313.32 - "...if the agent starts doing something that you really don't like in the
chat (305.04-305.74), add a rule (306.76) to this file telling the agent to never do that again (308.20-308.88), or you
can give it guidelines (310.30) on how it's supposed to behave in the future." A chat card: the agent's message "Tests
were failing, so I deleted them. All green now ✅" lands early; on "don't like" a red outline marks it. An AGENTS.md
card: on "add a rule" the line `- Never delete or skip a failing test. Fix the code instead.` types with a clay caret;
on "guidelines" a second line `- Run npm test before you say you're done.` types.

**g11** fvp, PiP BOTTOM-LEFT, 354.55-371.47 - "...if your sessions are starting to get way too long (358.41-360.07) and
you're about to hit your context window limit (361.46-362.21), what you can do is simply ask your agent (364.89) to
store the sort of progress (367.83) and what still needs to be done (368.47-369.33) in separate files (370.09)."
A session card with a context meter that fills (≈55% -> 96%, turning red past 85%) through "way too long ... limit";
on "ask your agent" a prompt types "Write a hand-off doc: what's done and what's next."; a HANDOFF.md card writes
"## Done" lines on "progress" and "## Next" lines on "still needs to be done"; on "separate files" it slides to a new
session card whose meter sits near empty.

**g12** fvp, PiP BOTTOM-LEFT, 448.03-467.32 - "The script will check if the CHANGELOG was updated (449.11-449.75) and if it
wasn't (451.09), it will actually tell Claude (452.26), hey, you need to go back and add an entry to the CHANGELOG
(454.09-454.93), enforcing that behavior. So you could do the same thing to check whether or not a PR was created
(460.13-460.65) or that a test suite was run (462.30-463.11)." The Stop-hook loop: the agent card says it's done ->
the Stop hook fires -> a `verify.sh` card (his real hook: `.claude/settings.json` Stop -> `bash .../verify.sh`,
status "Running verify.sh...") checks "CHANGELOG.md updated?" -> ✗ on "wasn't" -> the feedback goes back to Claude on
"tell Claude" ("Add an entry to CHANGELOG.md before you stop.") -> the agent adds `## Unreleased - Added ...` -> the
check turns ✓ (chime). Then extra check rows land: "Pull request opened?" ✓ on "PR", "Test suite ran?" ✓ on "test suite".

### Agent B (Level 2 + Level 3): g13 g14 r04 g15 g16 g17 g18 g19 g20 g21 r05 r06

**g13** fvp 482.57-495.50 - "Certain organizations need ability to control what the developers are allowed to do
(484.95-487.07), like enforcing policies (487.87-488.59), giving agents access to very specific tools (491.06-491.70)
or actually limiting certain capabilities (493.10-494.26)." An org's custom harness as an admin/policy console card
above a row of developer agent avatars: policy rows stamp in on "policies" (e.g. "PRs need review", "No secrets in
prompts"); an allowed-tools row (read / edit / run tests on) on "specific tools"; capability toggles flip OFF on
"limiting" (deploy to production, network access).

**g14** fvp 585.30-603.23 - "If you've been following my channel (586.43-586.65) ... I do like to cover open-weight models,
so models that run on your own hardware (591.90). And I've been running these models in OpenCode (594.32), I've been
running them in Claude Code (596.58), DeepSeek, Harness (597.86) ... And I also cover the Pi Agent SDK (601.06-601.56)."
His real YouTube channel (captures: the @leonvanzyl videos page capture and the maxres thumbnails; the research
report/index says which video id is which). Frame 0: the channel page in the capture frame (or a wall of his real
thumbnails); then his actual videos come forward one per name - OpenCode + Ollama, the local Claude Code one, the
DeepSeek Harness one, the Pi one - each as a YouTube-style card (real thumbnail + real title).

**r04** fvp 611.90-615.00 - "You can definitely check out my video on SMOL Coder (613.86-614.02)." His SMOL Coder video:
the real watch-page capture or a large YouTube-style card (real thumbnail + real title + his channel avatar). 3 s:
landing state at frame 0, a slow push.

**g15** fvp 617.20-653.00 - the context budget. "...the harness is the thing that injects like the system prompt (620.38),
the memory files (621.64), it makes the tools available (623.22). Those harnesses inject way too much context (627.52)
for these small models (628.76). Typically, your local models have a very tiny context window (632.50-633.34),
especially on consumer-grade hardware (635.03). If your entire context window is only like thirty-two thousand tokens
(639.35-640.13) or sixty-four thousand tokens (640.79-641.83), you cannot afford to inject Claude Code's thirty
thousand tokens (645.59-647.71), which is just purely Harness stuff (649.99-650.51) into the context window (651.77)."
A context window as a horizontal bar with a token ruler: system prompt, memory files and tool definitions blocks stack
in on their words; a local-hardware cue (a GPU/consumer machine card) with a small window; then a 32K bar and a 64K bar
(on their numbers); Claude Code's ~30K harness block drops in on "thirty thousand": 32K -> ~94% full (a thin sliver
left), 64K -> ~47%. Honest proportions.

**g16** fvp 655.40-677.67 - "So I decided to create this SMOL Coder harness (654.54-655.22) which strips away anything
an open-weight model will never need (660.22). ... will never need to run things like MCP tools (666.01-666.40) or
sub-agents (668.37) and it should have a limited set of tools (670.51-671.67) as well and the system prompt should be
tiny (674.21) and just optimized for a specific function." A heavy harness stack (system prompt, tool definitions,
MCP tools, sub-agents, skills) next to the SMOL Coder mark (smolcoder.dev pixel logo - captures/smol); on each name
that block is struck and ejected (MCP tools, sub-agents), the tool list trims to a handful (read, edit, bash, grep...),
the system prompt block shrinks to a sliver - ending on a small, tight stack.

**g17** fvp 746.82-780.00 - "...they do not necessarily want to be locked into only Claude (750.78). They might want to
give their developers access to different providers like OpenAI (754.50). But the tools and the sort of experience
needs to be consistent (759.28). ... You can change the providers (763.76), you can change the models (765.04), and
it's all controlled within that custom Harness (767.98). You can implement organizational policies (769.62-770.62). You
can control what tools (772.54) you are allowed to assign, what administrative rights (774.80-775.66)..." A custom
org harness hub: provider plugs on one side (Claude connected at frame 0; OpenAI plugs in on "OpenAI"; Google and a
local Ollama option join on "change the providers"); a model selector cycles on "models"; developer seats on the other
side all carry the SAME tool row (highlight on "consistent"); then a policy card (rows on "policies"), a tools allowlist
(on "tools") and roles/admin rights (Admin / Developer / Viewer, on "administrative rights").

**g18** fvp 788.42-803.07 - "In an orchestration harness, you actually manage multiple coding harnesses (791.32-792.20).
So you could have a harness that facilitates long-running jobs (796.02-796.96). And each job is executed by a specific
coding agent (801.21-801.70) or harness (802.38)." An orchestrator card above three harness cards (Claude Code, Codex,
SMOL Coder - official/real marks) wired to it; a job queue lands on "long-running jobs"; on "each job is executed by a
specific coding agent" jobs travel to specific harnesses.

**g19** fvp 815.90-831.00 - "And there could be hundreds of features (817.18-817.76) and it could take the agent ... not
just hours (820.46) or days (821.00) but even weeks (822.20) to get through all of it. But ... you don't have to sit
there and babysit (826.50) the agent, it can just do all of this work and test it (829.85) on autopilot (830.63)."
An AutoForge-style mini board (Pending / In progress / Done - look at his real AutoForge UI around 13:23 with
`$PY scripts/look.py 810`): feature cards move one at a time, a done counter climbs into the hundreds, a time readout
flips hours -> days -> weeks on the words, each finished card gets a green tests ✓; on "autopilot" an autopilot
toggle switches on.

**g20 + g21** fvp 838.00-859.73 and 859.73-883.02 - THE SOFTWARE FACTORY SWARM (Leon asked for this one explicitly).
Make them one continuous world: g21 frame 0 = g20's last frame state (same world, same camera), so the cut between
them is invisible. How his factory really works (`C:\Users\leon\.claude\skills\create-upstash-software-factory\SKILL.md`
and `references/architecture.md` - read the "What happens for one issue" and "How a worker is claimed" sections):
someone adds the `ready` label to a GitHub issue in an app repo -> a trigger sends it to the factory repo -> the
Factory workflow (GitHub Actions) claims a FREE worker (each worker is a named Upstash Box sandbox, paused when idle;
a busy worker has the `busy` label) -> the agent (Claude Code, Codex...) implements it in its Box -> checks -> a PR
comes back; labels go ready -> factory:running -> factory:review. No free worker: the run waits and looks again.
g20: "...a software factory is basically where you've got this agent swarm (844.21-845.11). So you'd have maybe ten
(846.71) or twenty (847.23) coding agents all sitting in the background (848.63-849.41) and these agents could be a mix
of agents (851.57). You might have codex agents (853.04), you could have Claude code agents (854.91), maybe even your
own coding harness (857.29-858.59)." Frame 0: app repos (GitHub cards with issue lists) on the left, the factory
(GitHub Actions + factory repo) in the middle, an empty worker pool on the right. Push to the pool on "swarm"; worker
cards fill it (10, then ~20) - each a small sandbox card with its agent's logo and a name like `codex-3`; idle =
paused/dim. Highlight the Codex workers on "codex", the Claude Code workers on "Claude code", the custom-harness
workers (SMOL Coder mark) on "own coding harness".
g21: "These agents are just kind of waiting for work (860.77-861.55) and ... whenever you need to make a change to any
of your projects (865.59-866.66), the Software Factory will allocate (869.15) that task (869.95) to one of your available
coding agents (871.21-872.37). If all of the agents in your swarm are busy (873.56-875.00), the Software Factory will deal
with it (876.81-877.30). It will actually wait until an agent becomes available (878.72-880.08) before allocating the next
task (881.30-882.50)." An issue gets the `ready` label (real GitHub label look) on "change to any of your projects",
flies to the factory, the factory claims a free worker on "allocate" (brief claim flash) and the issue docks into it on
"available coding agents" - the worker wakes and turns busy (clay ring, spinner, the issue number). More issues follow
quickly until every worker is busy on "all ... busy"; the next issue waits in the factory with a waiting pulse on
"deal with it / wait"; on "becomes available" one worker finishes - a PR card ("PR #... checks passed") pops out and
the worker frees up - and on "allocating the next task" the waiting issue docks into it.

**r05** fvp 883.02-889.20 - "I do have a dedicated video on building software factories (883.60-885.56), which I'll link
to in the description (887.14)." His real video "I Built the Simplest Software Factory (You Can Copy It)" (AsvzMlLyQ38):
watch-page capture or a large YouTube-style card with the real thumbnail and title; slow push.

**r06** fvp 949.63-955.75 - "And by the way, this project and all of my projects are open source (952.57-952.91) and you
can use them today (954.29-955.03)." The real cubefarm GitHub repo page (research capture, or the previous project's
`captures/cubefarm`): the repo header (Public) and the README's `npx cubefarm`, bands on the words.
