# Step 2: The visual debugging tool

**Goal:** give yourself eyes. Claude can't play a game, but it can open a page, jump to an exact moment, take screenshots from any camera and measure things. Build this **before any art**, because every later step depends on it.

**Why it matters:** "It looks fine" isn't proof. In LAST CALL, every asset shipped with screenshots and numbers ("the drumstick tip touches the bar within 0.05 mm", "feet on the floor within 2 mm", "148 draw calls"). Clipping, floating props and blown budgets were caught by the tool long before the user saw them.

## Ask first

Usually nothing. This step is technical. Tell the user in one line what it's for and that they'll see a first contact sheet at the end. Check yourself whether Chrome or Edge is installed (the tool drives it headless). Only ask if neither is.

## The page contract: `window.LC`

Every mockup, demo and (later) the game itself exposes this, so the tool can drive any page the same way:

```js
window.LC = {
  ready: false,            // true once the scene is built and assets are loaded
  duration: 6.6,           // loop length in seconds, if animated
  views: ['diorama', 'fp', 'turntable', 'face'],
  setView(name) {},        // switch camera
  seek(t) {},              // jump to time t; the frame must be a pure function of (view, t)
  play() {}, pause() {},
  renderNow() {},          // render one frame synchronously
  getStats() {},           // { drawCalls, triangles, geometries, textures, programs }
  selfTest() {},           // { pass, checks: [{ name, pass, value, limit }] }: numeric correctness
  // later, the game adds goto(beat), camera(pos, look), state(), and more
};
```

**Determinism is the point.** With no unseeded `Math.random`, no `Date.now()` and no frame-time-driven animation, a capture at t = 2.4 s is identical every time, and any moment can be compared before and after a change.

## Build `tools/capture.mjs`

A Node script using `playwright-core` with the installed Chrome or Edge (no browser download needed):

```
node tools/capture.mjs <page.html> --times 0,2.4,5 --views diorama,fp --out captures/<name> [--selftest] [--gpu swiftshader]
```

- Serves the project folder over a local HTTP server and opens the page headless at 1280×720 (or `--size`).
- Waits for `LC.ready`, then for each view and time: `setView`, `seek`, `renderNow`, screenshot.
- Writes the PNG frames, `_contact-sheet.png` (every frame in a labelled grid, so one image shows everything) and `report.json` (renderer stats per view, a short FPS probe, **console errors**, and the `selfTest` results).
- Checks the performance budget (draw calls and triangles per view) and flags every breach.
- `--gpu swiftshader` renders on the CPU, a pessimistic "weak laptop" smoke test.
- Exits non-zero when `selfTest` fails, a budget is broken, or the console has errors, so it can act as a gate.

Add analysis checks later, as the design system defines them (step 3): palette lint, text contrast and size, a colour-blind simulation, and a photosensitivity probe (no more than 3 full-frame brightness swings over 20% in any second). In step 6, extend it to drive the built game: `--url` or `--build`, `--scenario <beat>`, and suites of scenarios per helper.

Add `captures/` to `.gitignore`. Captures are scratch output, except the ones a demo or comparison page shows, which get copied somewhere permanent.

## Prove it works

1. Make a tiny test scene (`tools/testscene.html`): a floor, a box resting on it and a stick leaning on the box, with `window.LC` and a `selfTest` that measures box-to-floor and stick-to-box contact (pass if ≤ 1 mm).
2. Capture it. The contact sheet should look right, `selfTest` should pass and the console should be clean.
3. **Plant an error** (lift the box 5 cm) and capture again. The tool must fail loudly. Then put it back.
4. Show the user the contact sheet and the one-line result.

**Done when:** the test scene passes, the planted error is caught, and HANDOFF lists the tool and its usage. Next: step 3, the art style.
