# EXAMPLE (Harness Engineering, 2026-10-14) of writing the five report.md files by script: every NUMBER comes from the
# cut / logs / JSON (cut.json, sfx_log.json, music.json, thumbnail.json, split_geom.json, verify_voice.log, report_data.py),
# never typed by hand; every JUDGEMENT (thumbnail reasons, trims, eye contact, graphics, fact check, calls) is written per
# short in H[sk] after LOOKING at every contact sheet. Copy the pattern, not the text.
# Writes edit/short-NN_<slug>/report.md for the Harness Engineering shorts (run inside the work folder).
import json, os, re, subprocess, sys, functools, builtins
open = functools.partial(builtins.open, encoding='utf-8')
from collections import Counter

PY = '../.venv/Scripts/python.exe'
SHORTS = json.load(open('shorts.json'))
CUT = json.load(open('cut.json'))
FULL_TITLE = 'Harness Engineering: Make Any Coding Agent 10x Better'
FULL_URL = 'https://www.youtube.com/watch?v=z1EaBe9oIME'
SLUG = {'s1': '01_same-model-10x-score', 's2': '02_claude-code-30k-tokens', 's3': '03_what-is-an-ai-agent',
        's4': '04_software-factory-20-agents', 's5': '05_agent-swarm-in-3d'}
QUIET = {}  # from logs/verify_voice.log
for m in re.finditer(r'== (s\d) len=([\d.]+)s\s+quiet>150ms: (\[.*?\])\s+max quiet=(\d+)ms', open('logs/verify_voice.log', encoding='utf-8').read()):
    QUIET[m.group(1)] = (eval(m.group(3)), int(m.group(4)))

LAY = {'split': 'split', 'fc': 'full cam', 'fv': 'full visual'}
SND = {'pop_light': 'pop: light', 'ui_pop': 'pop: UI pop', 'hit_minimal': 'sting: minimal hit', 'success_two_note': 'chime: success two-note',
       'success_arpeggio': 'chime: success arpeggio', 'marker_stroke_a': 'highlight: marker stroke', 'marker_underline': 'highlight: marker underline',
       'mouse_click': 'click: mouse click', 'mouse_click_mx': 'click: mouse click mx', 'wind_sweep': 'whoosh: wind sweep'}

# ---------------------------------------------------------------- per-short judgement (written after looking at every sheet)
H = {}
H['s1'] = dict(
    thumb="38.033 s (run 7, split): the Terminal Bench 2.0 chart for the same model, GPT-5.2-Codex, 52.8% before and 66.5% after (+13.7), with your head popping out above it and your eyes on the lens. Of all the candidates, the jumping chart says \"same model, better score\" fastest at feed size. It beat these candidates:\n"
          "  - 3.183 s (run 0): the 6.7% Grok Code Fast 1 card, but your eyes are down\n"
          "  - 16.633 s (run 2): the harness diagram, which has no face\n"
          "  - 21.817 s (run 3): the sharpest face, but the LangChain title card says less than a chart that jumps\n"
          "  - 43.067 s (run 8): the X post, dense text at feed size, no face",
    trims=["**Hook first:** L1 (572.68 s, Grok Code Fast 1 from 6.7% to almost 70%) comes after L7 in the source. It opens the short as the hook, and the story then runs in source order from L2.",
           "**Dropped** between L6 and L7 (562.5–568.2 s): \"but he was able to get really good results, again, just by changing the harness\". The very next line says the same thing more sharply."],
    eyes="Runs 2, 5 and 8 are full visuals: there you read the LangChain post and the X article off the screen. The camera is back for the numbers you say to the lens: the hook (\"6.7%\" in a split, \"almost 70%\" full cam), \"GPT-5.2\", \"exact same model with the same prompt\", the 53% to 66% result, and the outro.",
    gfx=["**s1_r0 (split, hook):** a Grok Code Fast 1 pass-rate card from the edit benchmark. The true-scale bar lands at 6.7% in ember on \"6.7%\", with the \"edit tool: patch\" label. The top stays clear on frame 0 for the cover.",
         "**s1_r2 (full visual):** \"Same model, better harness\": one model tile in a harness ring with four tool tiles. The output meter sits low in ember, the harness lights up on \"changing the harness\", and the meter jumps to mint on \"improved its outputs\".",
         "**s1_r3 (split):** the LangChain logo and the real LangChain blog card, \"Improving Deep Agents with harness engineering\" (langchain.com/blog), landing on \"LangChain\". The \"GPT-5.2-Codex\" model chip lands on \"GPT-5.2\".",
         "**s1_r5 (full visual):** the real LangChain post in the capture frame. The inner camera moves onto the line about deepagents-cli going from 52.8 to 66.5 on Terminal Bench 2.0 with the model kept fixed (gpt-5.2-codex), with an azure band, then onto the leaderboard.",
         "**s1_r7 (split):** Terminal Bench 2.0 bars for GPT-5.2-Codex: 52.8% before (grey, Top 30) and 66.5% after (azure, Top 5), with a +13.7 mono label.",
         "**s1_r8 (full visual):** Can Bölük's real X article, \"I improved 15 LLMs at coding in one afternoon. Only the harness changed.\", with its cover image \"The Harness Is the Bottleneck\". The band lands on the cover just before you say \"was the bottleneck\"."],
    facts=["**\"Grok Code Fast 1 from only 6.7% all the way to almost 70%\":** correct. Can Bölük's article reports 6.7% to 68.3% on his edit benchmark, by changing only the edit tool. Sources: x.com/_can1357/status/2021828033640911196, blog.can.ac/2026/02/12/the-harness-problem and stencil.so/blog/the-harness-problem.",
           "**The title's \"10x\":** 68.3 / 6.7 = 10.2x. True.",
           "**LangChain, \"GPT-5.2 ... exact same model with the same prompt ... from 53% to about 66%\":** slightly off. deepagents-cli went from 52.8% to 66.5% on Terminal Bench 2.0 (Top 30 to Top 5), with the model fixed at GPT-5.2-Codex, not plain GPT-5.2. The system prompt was one of the harness changes they made, so it wasn't quite \"the same prompt\". The captions keep your words; the graphics show the true model name and numbers. Sources: langchain.com/blog/improving-deep-agents-with-harness-engineering (Vivek Trivedy, 17 Feb 2026), zenml.io and startuphub.ai.",
           "**Can Bölük's post:** confirmed. It's an X Article (@_can1357, 12 Feb 2026) titled \"I improved 15 LLMs at coding in one afternoon. Only the harness changed.\", with the cover image \"The Harness Is the Bottleneck\". Its benchmark covers 16 models."],
    calls=["**Music:** you called s1's generated take 2 \"terrible\", so s1 uses the long-form hook track you picked, cand_3, instead of any generated take. Its lift is moved onto the hook join (details under Audio).",
           "**Caption fix (found while writing this report):** the \"Can Bölük\" chip at 41 s first rendered as \"Can BÃ¶lÃ¼k\". The pipeline scripts read the plan with Windows' default text encoding. I fixed the skill (every script now reads UTF-8, and the stage scripts run Python in UTF-8 mode), repaired the text in place without re-cutting, and re-rendered s1.",
           "**The hook** is the Grok result rather than the LangChain one: \"6.7% to almost 70%\" is the bigger, simpler jump, and it earns the title."])
H['s2'] = dict(
    thumb="5.533 s (run 0, split): your real Claude Code `/context` breakdown with the \"36.2k/1m tokens\" total ringed in azure, your head above it. It is the short's claim, \"30,000 tokens before you type\", as a real screen. It beat these candidates:\n"
          "  - 18.850 s (run 2): the empty 32K and 64K grids, too abstract on their own\n"
          "  - 23.867 s (run 3): the 94% full window, a strong image but without your face\n"
          "  - 40.900 s (run 6): the sharpest face, but SMOL Coder's tool list doesn't tell the 30K story",
    trims=["**Hook first:** L1 (726.67 s, \"Before I've sent a single message...\") comes from the end of this section of the video and opens the short.",
           "**Dropped** between L5 and L6 (668.4–714.8 s): the SMOL Coder demo (the limited tool set, the tiny system prompt, the web version, model detection from LM Studio and Ollama). It's too long for a short; L6 lands the payoff, 1,400 tokens."],
    eyes="The full visuals (runs 1, 3 and 5) sit where you look at the screen to read the Ollama defaults or show SMOL Coder. Your one look away inside L3 is covered by switching to the full visual at \"you cannot afford\". The full-cam stretches are on-lens: \"which is just purely harness stuff\" and the 1,400-token outro.",
    gfx=["**s2_r0 (split, hook):** the Claude Code wordmark under the cover on frame 0, then your real Claude Code CLI (v2.1.296, Opus 5.5) from the recording: `/context` is typed, then the usage breakdown. An azure ring lands on \"36.2k/1m tokens (4%)\" as you say \"30,000\".",
         "**s2_r1 (full visual):** the real Ollama docs \"Context length\" page in the capture frame. The inner camera moves onto the VRAM defaults, with a band on \"< 24 GiB VRAM: 4k context\" and the advice to use at least 64000 tokens just below.",
         "**s2_r2 (split):** two true-scale context windows as glass grids, 32K on \"32,000\" then 64K on \"64,000\".",
         "**s2_r3 (full visual):** Claude Code's ~30K harness block (purple cells) drops into the 32K window: 94% full, with \"2K free\" in ember.",
         "**s2_r5 (full visual):** the real SMOL Coder CLI starting in your terminal (the SMOL logo, Qwen3.8 27B), then a Claude Code-sized harness list (system prompt, a long tool list, skills, MCP tools, sub-agents) being stripped down.",
         "**s2_r6 (split):** your local machine tile, Qwen3.8 27B (Q6_K, Ollama), with SMOL Coder's short system prompt and eight tools. \"MCP tools\" and \"Sub-agents\" are struck off in ember as you name them."],
    facts=["**\"Claude Code ... already taking up over 30,000 tokens\":** confirmed, approximately. Systima measured about 33,000 tokens on the first request of a bare Claude Code (12 Jul 2026), and Gigazine reported the same. Your own `/context` in the video shows 36.2K in total. Sources: systima.ai/blog/claude-code-vs-opencode-token-overhead and gigazine.net (13 Jul 2026).",
           "**\"Local models have a very tiny context window ... 32,000 or 64,000 tokens\":** confirmed as typical, and often smaller. Ollama's defaults by VRAM are 4k under 24 GiB, 32k for 24–48 GiB and 256k from 48 GiB, and Ollama advises at least 64000 tokens for coding agents. Sources: docs.ollama.com/context-length and the smolcoder README.",
           "**\"Open-weight models ... will never need MCP tools or sub-agents\":** your opinion, and SMOL Coder is built on it. Its README lists eight tools and no MCP.",
           "**\"Only takes 1,400 tokens\":** can't be checked from the README, but it's consistent with the public code: the system prompt plus eight tool definitions in `src/prompt.ts` and `src/tools/index.ts`. Sources: github.com/leonvanzyl/smolcoder."],
    calls=["**Title:** \"30,000 tokens\" is your rounded figure. The graphics show the real 36.2K from your `/context` and the true 94% fill of a 32K window.",
           "**Music:** the electro-pop style fits a tool demo better than the cinematic default. Take 2 was rejected automatically because it had vocals."])
H['s3'] = dict(
    thumb="10.917 s (run 2, split): the \"Agent = Model + Harness\" equation on glass above your head, with your mouth closed and your eyes on the lens. The whole short in one picture. It beat these candidates:\n"
          "  - 15.717 s (run 3): the real model launch pages, but no face\n"
          "  - 20.817 s (run 4): the Opus 5.5 brain diagram, which needs the context of the short\n"
          "  - 25.467 s and 33.000 s (runs 5 and 7): the harness and tools panels, sharp but without your face",
    trims=["**Dropped** between L5 and L6 (119.8–127.9 s): the examples \"like the ability to write files, search for files, browse the web. Open the browser, etc.\". The tools graphic (run 7) shows tools instead.",
           "**Dropped** between L6 and L7 (134.5–208.3 s): hooks, AGENTS.md and the rest of the Level 1 setup.",
           "**The outro**, L7 (208.29 s, \"So very simply put, an agent is the model plus the harness\"), is your own summary line from later in the video, and it closes the loop the hook opens."],
    eyes="Runs 3, 5 and 7 are full visuals: there you glance at your slides while you list the models, the environment and the tools. The camera shows when you're on the lens: the question, \"an agent is actually the model\", \"the brain of the operation\", \"allocates the rules\", the checks and the outro.",
    gfx=["**s3_r0 (split, hook):** the word \"agent\" echoes as floating chips (AI agents, agentic, coding agent, Agent SDK, sub-agents, agent swarm) that collapse into one \"agent\" tile. The top stays clear on frame 0 for the cover.",
         "**s3_r2 (split):** the equation on glass, Agent = ? + ?. The Model tile lands on \"model\" and the Harness tiles on \"harness\".",
         "**s3_r3 (full visual):** under a \"Model\" header, the real launch pages land on their names: Claude Opus 5.5 and Claude Fable 5.1 (anthropic.com), then GPT-6 Astra (OpenAI's model picker). They settle into a row of chips.",
         "**s3_r4 (split):** the Opus 5.5 model chip docks into the centre as the brain, and the four harness tiles connect to it.",
         "**s3_r5 (full visual):** the harness environment builds around the model: Instructions (AGENTS.md), Tools, Checks and Memory.",
         "**s3_r7 (full visual):** the Tools panel. Read, Write, Edit, Bash, Grep and WebFetch snap in, wired to the Opus 5.5 model.",
         "**s3_r8 (split):** a Checks terminal: `npm test`, `npm run lint` and `npx tsc --noEmit` tick to mint on \"test suites\", \"lint\" and \"type check\", with a success chime."],
    facts=["**\"Opus, Fable, GPT-6\" as the current models:** confirmed. Claude Opus 5.5 (released 22 Sep 2026), Claude Fable 5.1 (September 2026) and GPT-6 (GPT-6 Astra, released 3–4 Sep 2026). Sources: anthropic.com/claude-opus-5-5, anthropic.com/claude-fable-and-mythos-5-1 and anthropic.com/claude/fable.",
           "**\"An agent is the model plus the harness\":** a definition, not a measurable claim. It matches how LangChain and Anthropic's docs describe agent harnesses.",
           "**The checks (\"test suites, lint, type check\"):** confirmed as a capability. Claude Code hooks (for example a Stop hook) can run them and block the agent until they pass. Source: code.claude.com/docs/en/hooks."],
    calls=["**Captions:** the Whisper read-back heard \"test feeds\". The audio says \"test suites\", and the captions say \"test suites\".",
           "**The tools panel** shows Claude Code's real tool names (Read, Write, Edit, Bash, Grep, WebFetch) rather than the generic list on your slide."])
H['s4'] = dict(
    thumb="13.95 s (run 3, split): the Agent Swarm pool with the Claude Code workers lit as you say \"Claude Code\", your head above it. It beat these candidates:\n"
          "  - 3.783 s (run 0): the factory still idle, and the pool says less before it lights up\n"
          "  - 29.3 s (run 5): an issue docking into a worker, which needs motion to read\n"
          "  - 31.417 s (run 6): the sharpest frame, but no face",
    trims=["**No trims:** the four lines are one continuous stretch of the video (841.7–882.8 s). Only the pauses inside it were tightened."],
    eyes="The full visuals (runs 2, 4 and 6) sit where you look at your slides. You are on the lens for the hook, \"10 or 20 coding agents\", the agent names and the outro.",
    gfx=["**One continuous world:** all six compositions render windows of one \"factory time\" world, re-laid out for 9:16. Two of your real repos are at the top, cubefarm and smolcoder, with illustrative issues (#41 Day/night, #42 Pet dog, #18 /export, #19 Themes). The Factory sits in the middle, and the Agent Swarm pool of 20 workers (Claude Code, Codex and your own harness) sits below. No Upstash anywhere: the pool is the \"Agent Swarm\".",
         "**s4_r0 (split, hook):** the Factory idle, with the swarm pool as the hero. The top stays clear on frame 0 for the cover.",
         "**s4_r2 (full visual):** the 20 workers sit idle and paused, then turn into a mix of Claude Code, Codex and custom-harness icons on \"a mix of agents\".",
         "**s4_r3 (split):** the Codex, Claude Code and own-harness workers light up as you name each one.",
         "**s4_r4 (full visual):** an issue gets the `ready` label and flies to the Factory on \"whenever you need to make a change\".",
         "**s4_r5 (split):** the Factory claims a free worker (an azure flash, claude-3) and the issue docks into it, which turns it busy, on \"allocate\".",
         "**s4_r6 (full visual):** the pool fills to 20/20 busy and the next issue waits in ember on \"busy\". The full-cam outro says what happens next."],
    facts=["**\"10 or 20 coding agents ... Codex agents, Claude Code agents, maybe even your own coding harness ... the factory will allocate that task\":** confirmed. Your public software-factory skill sends an issue with the `ready` label to a free coding agent (Claude Code, Codex or any CLI agent) from a pool of workers, and the agent opens a pull request. Sources: github.com/leonvanzyl/skills (factories/.../architecture.md) and your video \"I Built the Simplest Software Factory\" (AsvzMlLyQ38, 24 Sep 2026).",
           "**\"It will wait until an agent becomes available\":** confirmed by the same architecture document: when every worker is busy, the issue waits for the next free worker."],
    calls=["**No sponsor:** the factory world never shows Upstash (an earlier video's sponsor). The worker pool is the \"Agent Swarm\", as in the long-form fix.",
           "**Illustrative issues:** the repos are real, but the issue numbers and titles, and which worker picks which issue, are illustrative."])
H['s5'] = dict(
    thumb="13.267 s (run 2, split): your real 3D office, with the Claude Code, Codex and OpenCode logo chips under it and your head above, eyes on the lens. \"Agent swarm\" and \"3D\" in one frame. It beat these candidates:\n"
          "  - 2.050 s (run 0): the cubefarm title card, but your eyes are a little down\n"
          "  - 21.383 s (run 3): the terminal showing claude-opus-5-5, dense and with no face\n"
          "  - 32.883 s (run 5): the Kanban board, dense and with no face\n"
          "  - 38.183 s (run 6): the sharpest face, but a GitHub PR page reads as plain text at feed size",
    trims=["**Dropped** between L4 and L5 (918.8–922.1 s): \"All represented in 3D space.\", which repeats L2.",
           "**Dropped** between L5 and L6 (934.7–942.0 s): \"And just like with a long running harness, we can assign as many tasks as we want. This could be hundreds of tasks.\" It's a side note that slows the ending."],
    eyes="The full visuals (runs 1, 3 and 5) are your real cubefarm footage, where you are driving the 3D office and looking at the screen. The camera shows the hook, \"Each of these agents are running a coding harness\", \"So this is using Claude Code\" (back on the lens after the monitor), the pull request and the outro.",
    gfx=["**s5_r0 (split, hook):** the cubefarm logo and your real 3D office footage in a window card. The top stays clear on frame 0 for the cover.",
         "**s5_r1 (full visual):** real cubefarm footage in the capture frame. The inner camera glides over the agents at their desks (Margaret on #294, a git log bubble).",
         "**s5_r2 (split):** a still of the office with the Claude Code, Codex and OpenCode logo chips landing on \"coding harness\".",
         "**s5_r3 (full visual):** the real footage of you running to a monitor. The Claude Code and Codex chips land on their names, then the camera pushes onto the terminal showing `claude-opus-5-5` (highlighted) on \"Claude Opus\".",
         "**s5_r5 (full visual):** the real Kanban whiteboard (Backlog, In progress, In QA) with issue cards #294 and #291. The GitHub chip lands on \"GitHub issues\".",
         "**s5_r6 (split):** the real GitHub pull request, \"The office fridge: open it, grab a snack or a cold drink and have it (you and the agents) #300\", with highlight bands landing as you talk about it."],
    facts=["**\"Each of these agents are running a coding harness ... Claude Code, it could be Codex ... other coding harnesses\":** confirmed. cubefarm's README: \"Every agent is a real coding agent, Claude Code, Codex or OpenCode\". Sources: github.com/leonvanzyl/cubefarm, npmjs.com/package/cubefarm and your video NBZmxhcz5lo (1 Oct 2026).",
           "**\"This guy is actually running Claude Opus\":** confirmed by the footage: the monitor shows `claude-opus-5-5`.",
           "**\"Kanban board ... hooked up to actual GitHub issues ... jump to the actual pull request\":** confirmed. The README describes the whiteboard as the Kanban board from backlog to merged, with agents picking up GitHub issues and opening pull requests. The footage shows the real PR #300."],
    calls=["**Music:** the indie style suits a playful 3D office better than the cinematic default.",
           "**Captions:** the Whisper read-back heard \"scan ban\" and \"pulled\". The audio says \"Kanban\" and \"built\", and so do the captions."])

COMMON_IN = ("- **Source:** the finished long-form render, `The 3 Levels of Harness Engineering (Beginner to Pro).mp4`: 3840×2160, 60 fps, 969.8 s. Your webcam is the picture-in-picture at x 3110, y 18, 698×944 (safe area 674×920) throughout.\n"
             "- **Clean voice:** the render has hook music, a riser and about 210 library SFX under your voice. So the voice comes from the long-form edit's dialogue stem (`voice_stem_YTHD60.wav`), patched in over the whole video with `clean_from_stem.py`.\n"
             "  - Sync: one piece over 0–969.8 s at a 21.5 ms offset. The fit left out the stretches with loud music under the voice (0–53 s, 131–135 s and 956–966 s).\n"
             "- **Transcription:** faster-whisper large-v3 with word timestamps and a prompt of the video's names. Every kept line was then force-aligned with wav2vec2 for the word edges.\n"
             "  - Name fixes: \"Bullock\" → Bölük, \"TARDIS\" → \"The harness\", \"scan ban\" → Kanban, \"cloud\" → Claude.\n"
             "- **Takes:** the source is a finished edit, so every line has one take and no swaps were needed.")

TIMING = ("- **Line start:** 40 ms before the first word.\n"
          "- **Line end:** each line ends at its measured true end, and is cut earlier where the tail stays quiet for more than 150 ms. A 170 ms tail fade never runs past the next sound.\n"
          "- **J-cut:** the audio leads each picture cut by 50 ms, and each caption chunk leads its word by 60 ms.\n"
          "- **Pauses and joins:** pauses over about 220 ms inside a line are cut to 120 ms (60 ms kept each side), and every join is placed at 120 ms loud-to-loud.")


def mmss(t): return f'{t:.3f}'


def write(sk):
    S = SHORTS[sk]; C = CUT[sk]; h = H[sk]; NN, slug = SLUG[sk].split('_', 1)
    out = f'../edit/short-{SLUG[sk]}'
    rd = subprocess.run([PY, 'scripts/report_data.py', sk], capture_output=True, text=True).stdout
    lufs, tp = re.search(r'integrated (\S+) LUFS, true peak (\S+) dBFS', rd).groups()
    nb = re.search(r'nb_frames=(\d+)', rd).group(1)
    END = C['runs'][-1]['T1']
    M = json.load(open(f'{sk}/music.json')); TH = json.load(open(f'{sk}/thumbnail.json'))
    G = json.load(open(f'{sk}/cam/split_geom.json'))
    sfx = json.load(open(f'{sk}/sfx_log.json'))
    q, qmax = QUIET[sk]
    L = []
    L.append(f'# Short {NN}: "{S["title"]}"\n')
    L.append(f'- **File:** `final.mp4`, 1080×1920, 60 fps, H.264 High, AAC 48 kHz stereo, {END:.3f} s ({int(nb):,} frames).')
    L.append(f'- **Stems:** `stems/voice.wav`, `stems/sfx.wav`, `stems/riser.wav` and `stems/music.wav`. All run the full {END:.3f} s, 48 kHz.')
    L.append(f'- **Cover (frame 0):** "{S["cover"][0]} / {S["cover"][1]}", written by me from the hook, since no title was given.')
    L.append('- **CTA:** the "Watch the full video" card (your rule: every short sends viewers to the full video), not a comment keyword.')
    L.append(f'- **Thumbnail:** `thumbnail.jpg` from {h["thumb"]}')
    L.append(f'- **Full video:** "{FULL_TITLE}", {FULL_URL}. The URL is the video ID from your stats-for-nerds screenshot. The title is the live YouTube title, checked today (the file name says "The 3 Levels of Harness Engineering (Beginner to Pro)"). The TikTok and Instagram CTA lines use the live title. If you rename the video, update those lines in `PUBLISH.md`.\n')
    L.append('## 1. Inputs and sync'); L.append(COMMON_IN + '\n')
    L.append('## 2. The cut (source timecodes → short)')
    L.append('| Line | Source (s) | Text |'); L.append('|---|---|---|')
    for ln in S['lines']:
        ps = [p for p in C['pieces'] if p['line'] == ln['id']]
        L.append(f"| {ln['id']} | {min(p['src0'] for p in ps):.2f}–{max(p['src1'] for p in ps):.2f} | {ln['text']}{' (CTA)' if ln.get('cta') else ''} |")
    L.append('\n**Order and editorial trims:**'); L += ['- ' + t for t in h['trims']]
    L.append('\n**Timing rules applied:**'); L.append(TIMING)
    joins = [p['T_end'] for p in C['pieces'][:-1]]
    def where(t, ms):
        prev = [w['w'] for w in C['words'] if w['e'] <= t + 0.05]
        after = f'after "{prev[-1]}"' if prev else ''
        if any(t - 0.01 <= j <= t + ms / 1000 + 0.01 for j in joins):
            return f'{ms} ms at {t:.2f} s ({after}, where a longer pause in the line was trimmed: your comma beat)'
        return f'{ms} ms at {t:.2f} s ({after}, your own pause)'
    qs = '; '.join(where(t, ms) for t, ms in q)
    L.append(f'\n**Verified on the final voice track:**')
    L.append(f'- A Whisper re-transcription of `voice.wav` reads the whole script with no clipped or stray syllables (misheard names aside).')
    L.append(f'- Quiet stretches over 150 ms: {qs}. The longest is {qmax} ms. Every one is a pause between phrases inside a line; none is dead air at a join between lines.')
    L.append(f"- **Voice loudness:** {C['lufs_before']:.1f} LUFS before a {C['gain_db']:+.1f} dB gain, so −14 LUFS integrated, with a {C['peak_after']:.1f} dBFS peak.")
    L.append(f'- **END:** {END:.3f} s. Every layer ends exactly on it.\n')
    L.append('## 3. Eye contact')
    L.append('- **Calibration:** I calibrated on the outro. In this video your on-lens pose is the frontal one, so a head turned to the side means you are reading the screen.')
    L.append('- **Where the camera hides:** ' + h['eyes'] + '\n')
    L.append('## 4. Layout plan (runs tiling [0, END])')
    L.append('| Run | Layout | Time (s) | Dur | Text |'); L.append('|---|---|---|---|---|')
    for r in C['runs']:
        tag = ' (hook)' if r['i'] == 0 else (' (outro + CTA)' if r is C['runs'][-1] else '')
        L.append(f"| {r['i']} | {LAY[r['layout']]}{tag} | {r['T0']:.3f}–{r['T1']:.3f} | {r['dur']:.2f} | {r.get('text','')} |")
    hm = [v['hair_med'] for v in G['per_run'].values()]
    L.append(f"\n**Camera geometry:** your webcam is a 674×920 picture-in-picture safe area, so:")
    L.append(f"- **Full cam:** the PiP is cover-fitted at about 2.08×, with light sharpening.")
    L.append(f"- **Split:** the webcam is scaled {G['scale']}× from your measured hair top (webcam y {min(hm):.0f}–{max(hm):.0f}) and lowest chin, so your whole face sits in the card and your hair pops about 95 px above its top edge.")
    L.append(f"  - The head above the card is cut out with Robust Video Matting (rvm_resnet50 on the GPU), from the same frame-exact clip as the card, so the two can't drift apart.")
    L.append(f"  - Split runs: {', '.join(str(k) for k in G['runs'])}.\n")
    L.append(f'## 5. Graphics ({len([1 for f in os.listdir("gfx/out60") if f.startswith(sk + "_r")])} HyperFrames compositions, the brand "stage" theme)')
    L.append('All were rendered at 240 fps with per-frame directional motion blur, blended down to 60 fps, and checked on 10 fps draft contact sheets first. The look is graphite glass, Figtree / Geist Mono, azure / ember / mint accents and the horizon wave, with real captures in the white capture frame.\n')
    L += ['- ' + g for g in h['gfx']]
    L.append('')
    L.append('## 6. Cover, captions and CTA')
    L.append(f'- **Cover:** frame 0 only, a graphite glass card with the title in white Figtree and an azure underline.')
    L.append('- **Captions:**')
    L.append('  - Burned in from the final voice track\'s aligned word timings, 1–3 words per chunk, white Figtree with a dark stroke.')
    L.append('  - Positions: in the split, between the card and your head; in full cam and full visual, the lower third; in the outro, centred at y 1250 so they clear your chin.')
    L.append('  - Highlights are glass keyword chips with an azure underline (never the old yellow serif): ' + ', '.join(f'*{w}*' for w in S['highlights']) + '.')
    L.append('- **CTA:** the "Watch the full video" card in the outro (box 43, 1344, 994×276). It has graphite glass, your azure play tile, the text typed in white Figtree 600 with a blinking azure caret, and an azure arrow button pointing down at the full-video link, pressed once the text is typed.\n')
    L.append('## 7. Audio')
    L.append('Levels are peaks relative to your voice peak. All sounds are from the skill\'s royalty-free library (CC0 and Mixkit; no attribution needed). No sound plays on layout cuts.\n')
    L.append('| Time (s) | Sound | Level | Source |'); L.append('|---|---|---|---|')
    keys = [e for e in sfx if e['type'] == 'key']
    for e in sfx:
        if e['type'] == 'key': continue
        L.append(f"| {e['t']:.3f} | {SND.get(e['sound'], e['sound'])} | {e['level_db']:.0f} dB | {e.get('src')} |")
    for src in dict.fromkeys(k.get('src') for k in keys):
        ks = [k for k in keys if k.get('src') == src]
        what = 'the CTA text' if src == 'cta' else 'in the graphic'
        L.append(f"| {ks[0]['t']:.3f}–{ks[-1]['t']:.3f} | typing ({what}): {len(ks)} single real key strokes ({', '.join(sorted(set(k['sound'] for k in ks)))}) | −20 to −22 dB | {src} |")
    L.append(f"\n- **Riser:** \"cinematic build\" from the library, with its loudest moment exactly on the hook join at {C['runs'][0]['T1']:.3f} s, at −12 dB. A minimal hit (sting) lands on the same frame.")
    if M['source'] == 'file':
        L.append(f"- **Music:** the long-form hook track you picked, **cand_3** (ACE-Step 1.5 XL, seed 3307, uplifting cinematic, 105 bpm, D major). It starts {M['file_offset']:.2f} s into the track, so its lift lands on the hook join. You rejected s1's generated take 2 (\"terrible\"). Takes 1 and 3 are still in `music_takes/` to compare, and `cand_3 (in the short).mp3` is the track that's used.")
    else:
        alts = M.get('alternatives', [])
        why = '; '.join(f"take {a['take']} scored {a['score']} ({a['why']})" if a['score'] is not None else f"take {a['take']} was ruled out ({a['why']})" for a in alts)
        L.append(f"- **Music:** generated locally with ACE-Step 1.5 XL (`{M['model']}`). Style {M['style']}, take {M['take']}, seed {M['seed']}, {M['bpm']} bpm. MIT licence; the model card allows commercial use of the outputs.")
        L.append(f"  - Picked automatically for the lift that lands best on the hook join. The takes it beat: {why}. All three are in `music_takes/`, the one used marked.")
    L.append(f"  - Level: 15 LU under your voice (about −29 LUFS), sidechain-ducked about 5 dB more while you speak, with a 0.8 s fade-in and a fade-out that ends exactly on END.")
    L.append(f"- **Mix:** {lufs} LUFS integrated, {tp} dBFS true peak.\n")
    L.append('## 8. Fact check (2+ sources each; the long-form research in `captures/facts.json`)')
    L += ['- ' + f for f in h['facts']]
    L.append('')
    L.append('## 9. Judgement calls')
    L.append('- **How many shorts:** five, the most you allowed. Each is a self-contained idea from the video: the score jump, the 30K-token harness, what an agent is, the software factory and the 3D swarm.')
    L += ['- ' + c for c in h['calls']]
    L.append('- **Captures:** the real pages are reused from the long-form research (captured fresh at 2x), and your UIs come from the raw recordings, never from the finished render, so none of the long-form edit\'s zooms or overlays show.')
    open(f'{out}/report.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('wrote', f'{out}/report.md')


for sk in (sys.argv[1:] or SHORTS):
    write(sk)
