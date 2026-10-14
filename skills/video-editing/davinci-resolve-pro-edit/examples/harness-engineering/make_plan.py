"""Writes edit_plan.json for the harness-engineering pro edit (times snapped to the 60 fps grid).
Zoom cams/marks live in zoom_specs.json (filled in after checking frames with look.py) and are merged in here."""
import json, os

FPS = 60
snap = lambda t: round(round(t * FPS) / FPS, 4)

beats = []
def B(id, kind, t0=None, t1=None, note='', **kw):
    b = dict(id=id, kind=kind, note=note, **kw)
    if t0 is not None: b['t0'] = snap(t0); b['t1'] = snap(t1)
    beats.append(b)

# ---------------------------------------------------------------- hook (0 -> 49.80)
B('z01', 'zoom', 0.0, 5.55, 'title slide: push into the code panel (agent = model + harness) as he says "the coding harness that you are given"')
B('w01', 'words', 4.10, 5.50, '"the only one you get" - the claim the video breaks', text='the only one', hl=True, xy=[960, 905])
B('g01', 'gfx', 5.55, 15.55, 'the harness you are given: Claude Code, Codex, OpenCode land as named, then model / memory files / hooks / tools snap into it', layout='fvp')
B('g02', 'gfx', 15.55, 23.72, '"only level one": three levels, 2 and 3 locked; most people pile up on level 1', layout='split')
B('p01', 'punch', note='"Harness Engineering is something I\'m really passionate about" - camera, punch in', items=[4], zoom=1.15)
B('w02', 'words', 26.12, 27.10, '"passionate"', text='passionate', hl=True, xy=[960, 905])
B('z02', 'zoom', 27.15, 40.0, 'title slide: push to the headline, band the subtitle "Building the environment..." on "build their own"')
B('w03', 'words', 35.27, 36.62, '"AI engineer" - the career promise', text='AI engineer', hl=True, xy=[960, 905])
B('g03', 'gfx', 40.0, 45.5, '"the three levels": the locked levels unlock - Configure, Build, Orchestrate (his slide icons)', layout='fvp')
B('p02', 'punch', note='"enough talk, let\'s jump into this" - the last hook line, tighter framing', items=[7], zoom=1.2)

# ---------------------------------------------------------------- body
B('c01', 'cta', 52.2, 57.2, '"consider joining my community at Agentic Labs"', url='skool.com/agentic-labs',
  label='Agentic Labs community', button='Join', type_at=round(54.24 - 52.2, 2), logo='gfx/assets/avatar.png')
B('z03', 'zoom', 55.35, 59.62, 'Agentic Labs classrooms grid')
B('z04', 'zoom', 59.62, 70.57, 'the Harness Engineering, Hooks & AutoForge deep dive in the classroom')
B('z05', 'zoom', 70.57, 76.97, 'the new "Zero to Pro" live series (calendar event)')
B('r01', 'gfx', 77.2, 82.6, '"$100 off your annual plan": the real Agentic Labs page (or a CTA if no price is public)', layout='fvp')

B('z06', 'zoom', 82.87, 96.63, '"what exactly is an agent?": read along the code panel line 1 - agent, model, harness', )
B('g04', 'gfx', 96.63, 107.1, 'the model is the brain: Opus 5.5, Fable 5.1, GPT-6 (real logos) dock into the model socket', layout='fvp')
B('z07', 'zoom', 107.1, 117.2, 'the harness block of the code panel: harness, then "rules": "AGENTS.md"')
B('g05', 'gfx', 117.2, 137.13, 'tools in action (write files, search, browse the web, open the browser) then the checks run (test suites, lint, type check)', layout='fvp')
B('g06', 'gfx', 140.2, 159.27, 'hooks: the agent life cycle events, then a UserPromptSubmit hook masks a secret before the prompt reaches the agent', layout='fvp')
B('r02', 'gfx', 161.9, 172.28, 'resource: Claude Mods (real page) - customise Claude Code, built on hooks', layout='fvp')
B('g07', 'gfx', 175.4, 183.37, 'memory files land as named: AGENTS.md, DESIGN.md, SOUL.md, the docs folder', layout='fvp')
B('z08', 'zoom', 183.37, 186.75, '"sandbox": band the "sandbox": "git worktree" line')
B('g08', 'gfx', 186.75, 197.53, 'sandbox: the agent in its workspace, worktree + feature branch, main branch locked (a push to main is refused)', layout='fvp')
B('z09', 'zoom', 197.53, 208.43, 'recap: the whole harness block of the code panel')

B('z10', 'zoom', 208.43, 226.5, 'his slide: Agent = model + harness, then Instructions / Tools / Checks / Memory as named')
B('z11', 'zoom', 226.5, 244.23, 'three levels slide: title, then the Configure card on "the first level is configuration"')
B('g09', 'gfx', 244.23, 256.0, 'harnesses built by the provider (Claude Code, Codex, Gemini CLI) or a third party (OpenCode, Cursor) - Claude Code = level 1', layout='fvp')
B('z12', 'zoom', 256.0, 268.8, 'Configure card: band "AGENTS.MD" on "update the agents.md file"')

B('z13', 'zoom', 268.8, 276.2, 'the Claude app session for the cozy-horror game: AGENTS.md in the file tree')
B('z13b', 'zoom', 276.2, 290.87, 'the real AGENTS.md open: "memory file", the rules a new session follows')
B('r03', 'gfx', 290.87, 299.9, 'resource: agents.md - "an open format", the agents that honour it (PiP bottom-left layout)', layout='fvp')
B('g10', 'gfx', 301.18, 313.32, 'rule of thumb: the agent does something you don\'t like in the chat -> a "never do that again" rule is typed into AGENTS.md, then a guideline (PiP bottom-left layout)', layout='fvp')
B('z14', 'zoom', 313.32, 337.17, 'composable rules: the docs folder in the file tree')
B('z15', 'zoom', 337.17, 354.55, 'the index table in AGENTS.md that links to the docs files')
B('g11', 'gfx', 354.55, 371.47, 'context window filling up -> the agent writes progress and next steps to a hand-off file -> a fresh session reads it (PiP bottom-left layout)', layout='fvp')
B('z16', 'zoom', 371.47, 390.73, 'the real HANDOFF.md: "Read this first in any new session"')
B('z18', 'zoom', 396.92, 425.22, 'the demo app and its CHANGELOG.md')
B('z19', 'zoom', 425.22, 448.03, 'settings.json: the hooks key, then the Stop hook and its verify.sh command')
B('g12', 'gfx', 448.03, 467.32, 'Stop hook loop: agent says done -> verify script finds no CHANGELOG entry -> blocks and tells Claude -> entry added -> passes; then PR created? tests run? (PiP bottom-left layout)', layout='fvp')

B('z21', 'zoom', 471.22, 478.33, 'three levels slide: Configure -> Build on "level two"')
B('p03', 'punch', note='"Trust me, building your own harness is in high demand right now." - straight to camera', items=[65], zoom=1.15)
B('g13', 'gfx', 482.57, 495.5, 'organisations control what developers may do: a custom harness with policies, allowed tools and limited capabilities', layout='fvp')
B('c02', 'cta', 516.0, 522.0, '"a free course in my free community that teaches you how to build your own coding harness"', url='skool.com/leonvanzyl',
  label='Free course: build your own harness', button='Join', type_at=round(516.84 - 516.0, 2), logo='gfx/assets/avatar.png')
B('z22', 'zoom', 526.35, 534.15, 'slide: Same model, better harness - "only the harness changed"')
B('z23', 'zoom', 545.0, 551.87, 'the real LangChain post: 52.8 -> 66.5, then the leaderboard row')
B('z24', 'zoom', 551.87, 557.68, 'slide: 52.8 -> 66.5%')
B('z25', 'zoom', 557.68, 568.48, 'the real X post by Can Bölük: title, then "The Harness Is the Bottleneck"')
B('f01', 'fix', 34334 / 60, 34356 / 60, 'the last 22 frames of V1 item 79 flash a Claude Design window: the X post screen held from frame 34333, live webcam pasted back (scripts/patch_flash.py)')
B('z26', 'zoom', 572.6, 582.53, 'slide: Grok Code Fast 1, 6.7 -> 68.3%')
B('g14', 'gfx', 585.3, 603.23, 'his own videos on open-weight models (real thumbnails): OpenCode, Claude Code, DeepSeek Harness, Pi', layout='fvp')
B('r04', 'gfx', 611.9, 615.0, 'his SMOL Coder video (real YouTube page/thumbnail)', layout='fvp')
B('g15', 'gfx', 617.2, 653.0, 'context budget: system prompt + memory files + tools fill a context window; a 32K local window vs Claude Code\'s ~30K of harness', layout='fvp')
B('g16', 'gfx', 655.4, 677.67, 'SMOL Coder strips the harness: MCP tools, sub-agents, the long tool list and the big system prompt fall away', layout='fvp')
B('z27', 'zoom', 686.17, 704.75, 'SMOL CLI: the /models picker with the Ollama / LM Studio models')
B('z28', 'zoom', 712.32, 722.2, 'SMOL CLI status line: 1.4k tokens (1%)')
B('z29', 'zoom', 726.62, 739.13, 'Claude Code /context: 36.2k tokens before the first message')
B('z30', 'zoom', 739.13, 746.82, 'three levels slide: Build card')
B('g17', 'gfx', 746.82, 780.0, 'a custom org harness: swap providers and models (Anthropic, OpenAI, Google, local) behind one consistent harness, policies, tools, admin rights', layout='fvp')

B('z31', 'zoom', 780.73, 788.42, 'three levels slide: Orchestrate card')
B('g18', 'gfx', 788.42, 803.07, 'an orchestration harness manages several coding harnesses: long-running jobs, each run by a specific agent', layout='fvp')
B('z32', 'zoom', 803.07, 815.9, 'AutoForge: logo, then the to-do board columns')
B('g19', 'gfx', 815.9, 831.0, 'long-running: hundreds of features, hours -> days -> weeks, one at a time on autopilot', layout='fvp')
B('z33', 'zoom', 831.58, 838.0, 'GitHub: the software-factory repo')
B('g20', 'gfx', 838.0, 859.73, 'the software factory swarm: issues -> factory -> a pool of 10-20 agents (Codex, Claude Code, own harness) waiting for work', layout='fvp')
B('g21', 'gfx', 859.73, 883.02, 'ingestion + allocation: a ready issue -> claimed by a free agent; all busy -> the task waits until an agent frees up', layout='fvp')
B('r05', 'gfx', 883.02, 889.2, 'his dedicated software factory video (real YouTube page/thumbnail)', layout='fvp')
B('z34', 'zoom', 908.9, 913.4, 'cubefarm: the monitor shows Claude Code running Claude Opus')
B('z35', 'zoom', 925.6, 935.6, 'cubefarm: the Kanban board wired to GitHub issues and PRs')
B('r06', 'gfx', 949.63, 955.75, 'resource: the open-source cubefarm repo on GitHub', layout='fvp')
B('c03', 'cta', 955.95, 961.6, '"hit the like button and subscribe"', url='youtube.com/@leonvanzyl', label='More agentic coding videos',
  button='Subscribe', type_at=round(958.61 - 955.95 - 1.2, 2), logo='gfx/assets/avatar.png')
B('c04', 'cta', 961.68, 966.07, '"join Agentic Labs ... the live sessions"', url='skool.com/agentic-labs', label='Agentic Labs live sessions',
  button='Join', type_at=round(962.94 - 961.68, 2), logo='gfx/assets/avatar.png')

specs = json.load(open('zoom_specs.json', encoding='utf-8')) if os.path.exists('zoom_specs.json') else {}
for b in beats:
    if b['id'] in specs: b.update(specs[b['id']])

plan = dict(
    source_timeline='YTHD60', new_timeline='YTHD60 - Pro Edit v1', hook_end=49.8,
    sfx_prefer={'sting': ['hit_minimal'], 'riser': ['cinematic_build']},
    # generated with ACE-Step 1.5 XL (music_gen.py, seed 4403, 112 bpm A major, indie plucks/marimba/Rhodes/pads,
    # drums + bass land on 5.4 s); the synthesized chillhop bed was 'very boring' (user, 2026-10-13)
    music=dict(style='chillhop', mood='warm', fade_out=2.5, drop=5.4, file='music/cand_3.wav', file_offset=0.0, bpm=105, under_voice_lu=15),
    beats=beats,
    chapters=[dict(t=0.0, title='Harness engineering: the three levels'),
              dict(t=82.87, title='What is an agent? Model + harness'),
              dict(t=226.5, title='The three levels of harness engineering'),
              dict(t=261.07, title='Level 1: configure (AGENTS.md and memory files)'),
              dict(t=390.73, title='Hooks: enforce behaviour with a Stop hook'),
              dict(t=471.22, title='Level 2: build your own harness'),
              dict(t=526.35, title='Same model, better harness (LangChain, Can Bölük)'),
              dict(t=582.53, title='SMOL Coder: a harness for local models'),
              dict(t=739.13, title='Custom harnesses for organisations'),
              dict(t=780.73, title='Level 3: orchestration harnesses'),
              dict(t=831.58, title='Software factories and agent swarms'),
              dict(t=889.2, title='A coding agent swarm in 3D (cubefarm)')],
    caption_fixes={  # matched case- and punctuation-insensitively, longest phrases first; a fix that starts a sentence is capitalised
        'Claude Code Codex or OpenCode': 'Claude Code, Codex or OpenCode', 'browse the web open the browser et': 'browse the web, open the browser, etc',
        'The DESIGN.md SOUL.md': 'The DESIGN.md, SOUL.md', 'GPT-five point two': 'GPT-5.2', 'AGENTS life cycle': "agent's life cycle",
        'zero to Euro': 'zero to pro', 'guiding harnesses': 'coding harnesses', 'cutting harness': 'coding harness',
        'scan-band board': 'Kanban board', 'Can Bullock': 'Can Bölük', 'sign-off document': 'hand-off document',
        'memory falls': 'memory files', 'DeepSeek, Harness': 'DeepSeek Harness', 'deep-agent CLI': 'deepagents-cli',
        'join in Agentic Labs': 'join Agentic Labs', 'AGENTIC coding': 'agentic coding', 'Open Code': 'OpenCode',
        'change log': 'changelog', 'work trees': 'worktrees', 'stop hook': 'Stop hook', 'codex agents': 'Codex agents',
        'Claude code agents': 'Claude Code agents', 'go to context': 'go to /context', 'Software Factory': 'software factory',
        'one thousand four hundred': '1,400', 'thirty-two thousand': '32,000', 'sixty-four thousand': '64,000',
        'thirty thousand': '30,000', 'fifty-three percent': '53%', 'sixty-six percent': '66%', 'Context window': 'context window',
        'Harness Engineering': 'Harness Engineering',
        'GPT-six': 'GPT-6', 'threeD': '3D', 'AGENT': 'agent', 'Harness': 'harness'},
    publish=dict(title='Harness Engineering: The 3 Levels Every AI Engineer Needs',
                 description=('Harness engineering explained: why an AI coding agent is the model plus its harness, and the three levels '
                              'of working with one. Configure Claude Code or Codex with AGENTS.md, memory files and hooks, build a custom '
                              'harness like SMOL Coder for local models, then orchestrate long-running jobs and agent swarms with a software factory.')),
)
json.dump(plan, open('edit_plan.json.tmp', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
os.replace('edit_plan.json.tmp', 'edit_plan.json')   # atomic: renders read the plan concurrently
print(len(beats), 'beats:', {k: sum(1 for b in beats if b['kind'] == k) for k in ('zoom', 'gfx', 'words', 'cta', 'punch')})
