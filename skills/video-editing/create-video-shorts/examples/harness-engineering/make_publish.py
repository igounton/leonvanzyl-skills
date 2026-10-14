# EXAMPLE (Harness Engineering, 2026-10-14) of writing edit/PUBLISH.md by script, with the full video's LIVE title
# (YouTube oEmbed) in every CTA line. Validate the result with scripts/check_publish.py. Copy the pattern, not the copy.
# Writes shorts/edit/PUBLISH.md (spec 8b) and checks every length rule. Run inside the work folder.
import json
FULL = 'Harness Engineering: Make Any Coding Agent 10x Better'
URL = 'https://www.youtube.com/watch?v=z1EaBe9oIME'
CTA = f'🎬 Watch the full video on YouTube: "{FULL}" (link in bio)'
SKOOL = ('🎁 Get the resources from this video + my free AI builder course: https://skool.com/leonvanzyl\n\n'
         '🚀 Go deeper inside Agentic Labs: AI coding courses, live Q&A, weekly challenges, and direct access to me: https://skool.com/agentic-labs')
P = [
 dict(sk='s1', slug='01_same-model-10x-score', thumb='the Terminal Bench 2.0 chart, the same model going from 52.8% to 66.5%, above your head pop-out',
      title='Same Model, 10x the Score: The Hidden AI Bottleneck',
      desc='Changing only the coding harness took Grok Code Fast 1 from 6.7% to 68.3%, and LangChain lifted GPT-5.2-Codex from 52.8% to 66.5% on Terminal Bench 2.0.',
      yt_tags='#HarnessEngineering #LangChain #AICoding',
      tt_hook='Same AI model, 10x the score. The hidden bottleneck isn\'t what you think.',
      tt_kw='Grok Code Fast 1 went from 6.7% to 68.3% and GPT-5.2-Codex from 52.8% to 66.5% on Terminal Bench 2.0. The model never changed.',
      tt_tags='#HarnessEngineering #LangChain #AICoding #CodingTok',
      ig_hook='Same AI model, 10x the score. The hidden bottleneck isn\'t the model you pick.',
      ig_ideas=['Can Bölük took Grok Code Fast 1 from 6.7% to 68.3% on his coding benchmark, just by changing how its edit tool works.',
                'LangChain kept GPT-5.2-Codex fixed and still climbed from 52.8% to 66.5% on Terminal Bench 2.0 with a better coding agent harness.'],
      ig_tags='#HarnessEngineering #LangChain #AICoding #AIAgents'),
 dict(sk='s2', slug='02_claude-code-30k-tokens', thumb='your real Claude Code /context breakdown with the 36.2K total ringed, above your head pop-out',
      title='The Hidden 30K Tokens Claude Code Uses Before You Type',
      desc='Claude Code\'s harness fills about 30,000 tokens of context before your first message. On a local model with a 32K window, that\'s 94% gone. SMOL Coder needs about 1,400.',
      yt_tags='#ClaudeCode #LocalLLM #ContextWindow',
      tt_hook='Claude Code burns 30,000 tokens before you even type. Here\'s why that kills local models.',
      tt_kw='Local LLMs on Ollama often get a 32K context window. My SMOL Coder harness needs about 1,400 tokens: no MCP, no sub-agents.',
      tt_tags='#ClaudeCode #LocalLLM #Ollama #CodingTok',
      ig_hook='Claude Code uses about 30,000 tokens before you even type. Here\'s why that kills local models.',
      ig_ideas=['Local models on consumer hardware often run with a 32K or 64K context window. Claude Code\'s harness alone would fill a 32K window to 94%.',
                'So I built SMOL Coder, a coding harness for open-weight models: a short system prompt, eight tools, no MCP and no sub-agents. About 1,400 tokens in all.'],
      ig_tags='#ClaudeCode #LocalLLM #Ollama #OpenSource'),
 dict(sk='s3', slug='03_what-is-an-ai-agent', thumb='the "Agent = Model + Harness" equation above your head pop-out',
      title="The Truth About AI Agents (It's Not Just the Model)",
      desc='What an AI agent really is: the model (Claude Opus, Fable, GPT-6) plus the harness around it, with the rules, tools and checks like tests, lint and type checks.',
      yt_tags='#AIAgents #HarnessEngineering #LLM',
      tt_hook='Everyone says "AI agent", but what actually is one? The truth is simpler than you think.',
      tt_kw='An agent is the model (Claude Opus, Fable, GPT-6) plus the harness: the rules, tools and checks that turn an LLM into a coding agent.',
      tt_tags='#AIAgents #HarnessEngineering #LLM #TechTok',
      ig_hook='Everyone says "AI agent". The truth about what one actually is might surprise you.',
      ig_ideas=['The model is the brain: Claude Opus, Fable or GPT-6.',
                'The harness is the environment it works in: the rules it follows, the tools it can use, and the checks it has to pass, like test suites, lint and type checks.'],
      ig_tags='#AIAgents #HarnessEngineering #LLM #AICoding'),
 dict(sk='s4', slug='04_software-factory-20-agents', thumb='the Agent Swarm pool with the Claude Code workers lit, above your head pop-out',
      title='The Secret to Running 20 AI Coding Agents at Once',
      desc='A software factory keeps an agent swarm of 10 or 20 coding agents, from Claude Code and Codex to your own harness, and hands each new task to the next free agent.',
      yt_tags='#SoftwareFactory #ClaudeCode #AIAgents',
      tt_hook='How do you run 20 AI coding agents at once without chaos? The secret is a software factory.',
      tt_kw='Claude Code and Codex agents wait in a swarm. The factory gives each new task to the next free agent, and waits when they\'re all busy.',
      tt_tags='#SoftwareFactory #ClaudeCode #Codex #AIAgents #CodingTok',
      ig_hook='The secret to running 20 AI coding agents at once without chaos.',
      ig_ideas=['A software factory keeps an agent swarm in the background: Claude Code agents, Codex agents, even your own coding harness.',
                'Whenever a project needs a change, the factory hands the task to the next free agent. When every agent is busy, it waits.'],
      ig_tags='#SoftwareFactory #ClaudeCode #Codex #AIAgents'),
 dict(sk='s5', slug='05_agent-swarm-in-3d', thumb='your real 3D office with the Claude Code, Codex and OpenCode logos, above your head pop-out',
      title='My AI Agent Swarm Works in 3D (Insane to Watch)',
      desc='cubefarm turns a coding agent swarm into a 3D office: Claude Code, Codex and OpenCode agents work GitHub issues from a Kanban board and open real pull requests.',
      yt_tags='#AgentSwarm #ClaudeCode #AICoding',
      tt_hook='My AI agent swarm works in a 3D office, and it\'s insane to watch.',
      tt_kw='Every agent runs a real coding harness, Claude Code or Codex, and works GitHub issues from a Kanban board until it\'s built, tested and verified.',
      tt_tags='#AgentSwarm #ClaudeCode #AICoding #CodingTok',
      ig_hook='No one said an agent harness should be boring. My AI agent swarm works in 3D, and it\'s insane to watch.',
      ig_ideas=['Every agent in the office runs a real coding harness: Claude Code, Codex and more. Walk up to a monitor and you can see it running Claude Opus.',
                'The whiteboard is a Kanban board hooked up to real GitHub issues, and every card jumps to its actual pull request.'],
      ig_tags='#AgentSwarm #ClaudeCode #AICoding #AIAgents'),
]
TH = {p['sk']: json.load(open(f"{p['sk']}/thumbnail.json", encoding='utf-8'))['t'] for p in P}
out = ['# Publishing package', '',
       f'The full video every Short links to: **"{FULL}"**, {URL}. It\'s the live YouTube title, checked on 14 October 2026; the file name says "The 3 Levels of Harness Engineering (Beginner to Pro)". If you rename the video, update the 🎬 lines.', '']
errs = []
for p in P:
    n = p['slug'].split('_')[0]; t = TH[p['sk']]
    if len(p['title']) > 54: errs.append(f"{n} title {len(p['title'])}")
    if len(p['tt_hook']) >= 100: errs.append(f"{n} tiktok hook {len(p['tt_hook'])}")
    if len(p['ig_hook']) >= 125: errs.append(f"{n} ig hook {len(p['ig_hook'])}")
    if len(p['yt_tags'].split()) != 3: errs.append(f'{n} yt tags')
    if not 3 <= len(p['ig_tags'].split()) <= 5 or not 3 <= len(p['tt_tags'].split()) <= 5: errs.append(f'{n} tags')
    if len(p['desc']) > 200: errs.append(f"{n} desc {len(p['desc'])}")
    tt = f"{p['tt_hook']}\n{p['tt_kw']}\n\n{CTA}\n\n{p['tt_tags']}"
    ig = '\n\n'.join([p['ig_hook'], *p['ig_ideas'], CTA, p['ig_tags']])
    print(f"{n}: title {len(p['title'])}, tt hook {len(p['tt_hook'])}, tiktok {len(tt)}, ig hook {len(p['ig_hook'])}, desc {len(p['desc'])}")
    out += [f"## Short {n}: {p['slug'].split('_', 1)[1]}  (file: edit/short-{p['slug']}/final.mp4)",
            f"**Thumbnail** (short-{p['slug']}/thumbnail.jpg, from {t:.3f} s: {p['thumb']}). The YouTube thumbnail and the Instagram cover; on TikTok, upload it as the cover or pick the frame at {t:.3f} s.", '',
            f"![Short {n} thumbnail](short-{p['slug']}/thumbnail.jpg)", '',
            '### YouTube Shorts', '**Title**', '```', p['title'], '```', '', '**Description**', '```', p['desc'], '', SKOOL, '', p['yt_tags'], '```',
            f'**Related video:** "{FULL}" ({URL})', '',
            '### TikTok', '**Caption**', '```', tt, '```', '',
            '### Instagram Reels', '**Caption**', '```', ig, '```', '']
assert not errs, errs
open('../edit/PUBLISH.md', 'w', encoding='utf-8').write('\n'.join(out))
print('wrote ../edit/PUBLISH.md')
