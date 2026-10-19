# Step 10: Deploy

**Goal:** the game live on the host the user picks, checked on the real site, with an optional "making of" page that shows the journey.

**Publishing is the user's call.** Nothing goes public without an explicit yes in chat, even if they asked you to work on your own earlier. **So is spending money:** if they pick a paid host, they buy the plan themselves. Never buy a plan or a domain, create an account, or handle a password for them.

## Pick the host

The game is a static site: HTML, code, images and audio files, with nothing running on a server. So any static host can serve it. Before asking, check what's already set up: a host the user named earlier (HANDOFF's decisions log), a `.hostinger/site.json` or `vercel.json`, a host's plugin or connector in this session, or a host's command-line tool that's already logged in. Recommend the one they already have.

| Host | Good for | Cost | Preview before going live |
|---|---|---|---|
| **Hostinger** web hosting | Their own domain, email and hosting in one place, with the whole deploy done from Claude Code through Hostinger's official connector. LAST CALL went live this way | Paid plan | A separate staging website |
| **Vercel** | Free and quick, with a preview link on every deploy | Free tier | Built in |
| **itch.io** | Being found by players: a big home for indie games, with a game page, comments and optional pay-what-you-want | Free | A draft page |
| **Netlify** or **Cloudflare Pages** | Free and quick, much like Vercel | Free tier | Built in |
| **GitHub Pages** | Free, if the project already lives on GitHub | Free for public repositories | None |
| **Their own web host** | Hosting they already pay for | Their plan | A second site or a subfolder |

Hosts can be combined: for example, the game on a website, plus an itch.io page that points to it.

## Ask first

AskUserQuestion:
- **Where should it live?** Offer the 3 or 4 hosts that fit what they've told you, each with its "good for" line from the table. Put the one they already have first, marked (Recommended). If nothing points either way, don't force a recommendation: offer Hostinger, Vercel, itch.io and Netlify / Cloudflare Pages, and let the one-line descriptions do the work (the tool's "Other" covers the rest).
- **Go live now?** A preview first, then the live site when you say so (Recommended) / straight to the live site / not yet.
- **A "making of" page?** Yes, linking the art-style mockups, the audition page, the talking-character demo and the snapshots (Recommended: it's a lovely story to share) / no.
- **The address:** a free one from the host, named after the game (Recommended) / their own domain (one they have, or one they buy). Suggest a name from the game's title.

Then read the section for their host, and only that one. Commands change, so check the host's current docs, or use its own skill or plugin, for the exact steps.

## Host notes

### Hostinger

- **What the user sets up:** a Hostinger web hosting plan (they buy it), and Hostinger's plugin for Claude Code, which connects Claude Code to their account through Hostinger's official connector: `/plugin install hostinger@claude-plugins-official`, then they approve the sign-in in their browser. If the connector asks to be authorised again later, they do that too.
- **Deploy from Claude Code** with the plugin's `deploy-to-hosting` skill (and its `connect-domain` skill for their own domain and its SSL). The upload runs from Claude's shell, so a plain chat with the connector can manage domains but can't push the build.
- **The deploy:** zip the build with `index.html` at the root of the archive (`cd dist && zip -r ../site_YYYYMMDD_HHMMSS.zip .`), upload it, and deploy it as a static site. The target is a website on their own domain or on a free `*.hostingersite.com` subdomain.
- **Every deploy replaces the whole site**, and there's no preview or rollback built in. So stage on a **separate website** (a second free subdomain, never a subfolder of the live site, because the live deploy overwrites everything under it), check it, then deploy the same zip to the live site. Keep each zip: redeploying the previous one is the rollback.
- **Caching:** Hostinger's web server (LiteSpeed) reads `.htaccess`. Put one in `public/` so Vite copies it into the build, then check the headers with `curl -sI`, because lines it doesn't understand are skipped silently. After a redeploy, clear the site's cache (the skill knows how). A starting point:

  ```apache
  Options -Indexes
  <IfModule mod_headers.c>
    # hashed code and fonts (safe only while every .js, .css and font name carries a hash)
    <FilesMatch "\.(js|css|woff2?)$">
      Header set Cache-Control "public, max-age=31536000, immutable"
    </FilesMatch>
    # audio and data: an hour, until their URLs carry a content version
    <FilesMatch "\.(mp3|ogg|wav|json)$">
      Header set Cache-Control "public, max-age=3600, must-revalidate"
    </FilesMatch>
    # entry points: always check for a new version
    <FilesMatch "^index\.(html|json)$">
      Header set Cache-Control "no-cache"
    </FilesMatch>
  </IfModule>
  ```

- **Remember the target:** the skill writes `.hostinger/site.json` (the domain and the account), so later redeploys go to the same site.

### Vercel

- Use a `deploy-to-vercel` skill if one is available, or the Vercel CLI. If the user isn't logged in, they log in themselves.
- Every deploy gets a preview link; going live is a separate step (`vercel --prod`).
- **Caching:** `headers` in `vercel.json`.

### itch.io

- **The user** creates the itch.io account and the game page (kind of project: HTML). Keep the page as a **draft** until the live check passes.
- Upload a zip of the build on the page and tick "This file will be played in the browser", or use itch.io's `butler` tool, which the user logs in to themselves (`butler push dist <user>/<game>:html5`). Set the viewport to the game's shape (e.g. 1280 × 720) and turn on the fullscreen button.
- **Limits** (itch.io's HTML5 docs, checked October 2026): at most 1,000 files, 500 MB extracted and 200 MB per file, paths up to 240 characters, and case-sensitive file names. A game with one audio file per line can easily pass the file count. Then either pack the audio into fewer files, or host the game elsewhere and have the itch.io page point to it.
- **Paths must be relative:** the game runs from a subfolder, inside a frame on the page. Check mouse look, fullscreen and sound inside that frame.
- No custom headers.

### Netlify or Cloudflare Pages

- Their command-line tools deploy the `dist/` folder. `netlify deploy --dir=dist` gives a draft link, and adding `--prod` puts it live. Cloudflare's `npx wrangler pages deploy dist` gives a preview link for any branch that isn't the production one. The user logs in themselves.
- **Caching:** a `_headers` file in `public/` (both read it).
- Check their per-file size limit against the largest audio file.

### GitHub Pages

- The project has to be on GitHub. Ask before creating a repository or pushing. Pages is free for public repositories; private ones need a paid GitHub plan.
- Deploy with a GitHub Actions workflow that builds the game and publishes `dist/` (Vite's docs have one).
- Without a custom domain, the game lives at `https://<user>.github.io/<repo>/`, so use relative paths (`base: './'`).
- No custom headers, and no previews.

### Their own web host

- Upload the contents of `dist/` into the site's web root with the host's file manager, FTP or SFTP. The user types their own password or sets up an SSH key; never handle it.
- Apache and LiteSpeed hosts read `.htaccess` (the Hostinger notes have a starting point).

## Before you deploy (every host)

1. A production build of the game (a static site, nothing server-side).
2. **Secrets check:** search the build output for the API key, `ELEVENLABS` and `.env`. Nothing may appear. Audio is static files, and the key never left the build scripts.
3. **The paths match where the game will live.** At the root of a domain or subdomain, root paths (`/audio/x.mp3`, Vite's default `base: '/'`) work. In a subfolder (itch.io, or GitHub Pages without a custom domain) they break: switch to relative paths (`base: './'`), and look for root URLs written into code and data files too, such as an audio index. LAST CALL's paths are root-absolute, so it can only live at a domain root.
4. **Measure the build** and compare it with the host's limits: the file count, the total size, the largest file, and how much a player downloads before the title screen. Games with lots of voice lines are big. LAST CALL is 3,340 files and 115 MB: easy for a web host, but more than three times itch.io's file limit.
5. **Caching headers**, in the host's own format (see its notes):
   - Vite's hashed code and fonts (`/assets/*`): a year, `immutable`;
   - `index.html` and the audio index: always revalidated (`no-cache`);
   - audio files: a long cache only once their URLs carry a content version (`?v=<hash>` or a hashed name), otherwise an hour, so a re-mixed line never plays stale.

   itch.io and GitHub Pages don't let you set headers, but the hashed names still keep updates correct.
6. **The making-of page** (if wanted), at `/making-of`. Copy the demos into the build so they work on the live site, with relative paths and no localhost links. Give each demo a sentence on what it shows.

## Deploy and check the live site

1. **Deploy a preview first** (the host's preview link, a staging website or an itch.io draft) and give the user the link. If the host has no preview at all, say so, and go live only after their yes.
2. **Check the real site yourself:**
   - it loads with 0 console errors, and no file 404s (especially audio);
   - the headers are right (`curl -sI` on `index.html`, a hashed `.js` file and an audio file), where the host lets you set them;
   - sound plays after the first click;
   - New game reaches the first beat;
   - a chapter start works;
   - the making-of links all open.
   - Check it at a laptop size, and at phone size if touch is supported.
3. When the user says go, deploy to the **live site**. On a host that replaces files in place, deploy the exact archive you just checked, not a fresh build. Check it again the same way, and give them the final link.
4. **Write it down.** Update HANDOFF with the host, the live URL, the date, how to redeploy, and "pipeline complete". Add the live links to the demo list. When the host has no rollback of its own, keep the deployed archive.

**Done when:** the live site is checked and the user has the link. The game is shipped.
