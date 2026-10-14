# Graphics agent C (short s4 "20 AI agents, one factory"): copies the official logos the software-factory world uses
# into gfx/assets/ under the c_ prefix (downscaled, alpha kept) and writes gfx/asset_dims_c.json.
# Sources: longform_assets/ (the long-form edit's cut-out logos; originals in captures/logos, see sources.json).
# No stills or clips from the recordings: the factory world is a diagram (glass + white GitHub windows), no real UI.
import json, os
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
A = 'gfx/assets'; os.makedirs(A, exist_ok=True)

LOGOS = {
    'c_claude.png': 'longform_assets/b_claude_symbol.png',      # Claude spark (Claude Code uses it; no separate mark)
    'c_codex.png': 'longform_assets/b_codex.png',               # Codex icon (OpenAI blossom on black)
    'c_gh_actions.png': 'longform_assets/b_gh_actions_dark.png',  # GitHub Actions mark, white (for glass)
    'c_github.png': 'longform_assets/b_github.png',             # GitHub invertocat, black (for white windows)
}
dims = {}
for out, src in LOGOS.items():
    im = Image.open(src).convert('RGBA')
    im.thumbnail((256, 256), Image.LANCZOS)
    im.save(f'{A}/{out}')
    dims[out] = im.size
json.dump(dims, open('gfx/asset_dims_c.json', 'w'), indent=1)
print(json.dumps(dims))
