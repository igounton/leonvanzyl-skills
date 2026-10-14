/* @ds-bundle: {"format":4,"namespace":"LeonYouTube_792a19","components":[{"name":"Cursor","sourcePath":"components/core/Cursor.jsx"},{"name":"IconTile","sourcePath":"components/core/IconTile.jsx"},{"name":"MonoLabel","sourcePath":"components/core/MonoLabel.jsx"},{"name":"BarRow","sourcePath":"components/data/BarRow.jsx"},{"name":"Stat","sourcePath":"components/data/Stat.jsx"},{"name":"Track","sourcePath":"components/data/Track.jsx"},{"name":"DataTable","sourcePath":"components/lists/DataTable.jsx"},{"name":"SpecRow","sourcePath":"components/lists/SpecRow.jsx"},{"name":"StepList","sourcePath":"components/lists/StepList.jsx"},{"name":"ChatBubble","sourcePath":"components/paper/ChatBubble.jsx"},{"name":"Pill","sourcePath":"components/paper/Pill.jsx"},{"name":"ProductWindow","sourcePath":"components/paper/ProductWindow.jsx"},{"name":"TaskCard","sourcePath":"components/paper/TaskCard.jsx"},{"name":"SlideTitle","sourcePath":"components/slide/SlideTitle.jsx"},{"name":"Stage","sourcePath":"components/slide/Stage.jsx"},{"name":"CodePanel","sourcePath":"components/surfaces/CodePanel.jsx"},{"name":"GlassPanel","sourcePath":"components/surfaces/GlassPanel.jsx"}],"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.LeonYouTube_792a19 = window.LeonYouTube_792a19 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Cursor.jsx
try { (() => {
/* The glowing pointer in the slide accent, with a thick white outline. */
function Cursor({ size = 84, className, style }) {
  const s = Number(size) || 84;
  return React.createElement("svg", {
    className: ["ly-cursor", className].filter(Boolean).join(" "),
    style: style,
    width: s,
    height: s,
    viewBox: "0 0 40 40",
    "aria-hidden": true
  }, React.createElement("path", { d: "M7 6 L34 16.5 L21.5 20.5 L16.5 33 Z" }));
}
Object.assign(__ds_scope, { Cursor });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Cursor.jsx", error: String((e && e.message) || e) }); }

// components/core/IconTile.jsx
try { (() => {
/* A glossy, slightly tilted 3D tile with a white glyph: the personality of a slide. */

const GLYPHS = {
  code: { stroke: "M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5M13.2 5.5l-2.4 13" },
  arrow: { stroke: "M5 12h13M13 6.5l5.5 5.5-5.5 5.5" },
  check: { stroke: "M5 12.5l4.5 4.5L19 7.5" },
  shield: { stroke: "M12 3.2 19 6v5.6c0 4.3-2.9 7.9-7 9.2-4.1-1.3-7-4.9-7-9.2V6z", fill: "M12 8.2l1 2.6 2.6 1-2.6 1-1 2.6-1-2.6-2.6-1 2.6-1z", width: 2.2 },
  sparkle: { fill: "M11 4l1.9 5.1L18 11l-5.1 1.9L11 18l-1.9-5.1L4 11l5.1-1.9zM18.5 14.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z" },
  bolt: { fill: "M13.5 2.5 5 13.5h6l-1.5 8 9-11.5h-6z" },
  bars: { fill: "M6.6 5.5h10.8a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 10.4h6.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 15.3h2.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2z" },
  eyes: { fill: "M8.4 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2zM15.6 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2z" }
};
const COLORS = ["azure", "iris", "ember", "mint"];

function IconTile({ color = "azure", glyph = "code", size = 116, tilt = -8, antenna, float = false, label, className, style }) {
  const s = Number(size) || 116;
  const c = COLORS.indexOf(color) >= 0 ? color : "azure";
  const name = GLYPHS[glyph] ? glyph : "code";
  const g = GLYPHS[name];
  const hasAntenna = antenna == null ? name === "eyes" : !!antenna;
  const t = Number(tilt) || 0;
  const stick = Math.max(4, Math.round(s * 0.075));
  const ball = Math.round(s * 0.18);
  const icon = Math.round(s * 0.5);
  const tile = React.createElement("div", {
    className: ["ly-tile", "ly-tile--" + c, s < 72 && "ly-tile--sm"].filter(Boolean).join(" "),
    style: { width: s + "px", height: s + "px", borderRadius: Math.round(s * 0.285) + "px", transform: t ? "rotate(" + t + "deg)" : undefined }
  },
    hasAntenna ? React.createElement("span", { className: "ly-tile__stick", style: { width: stick + "px", height: Math.round(s * 0.2) + "px", top: -Math.round(s * 0.18) + "px", marginLeft: -stick / 2 + "px" } }) : null,
    hasAntenna ? React.createElement("span", { className: "ly-tile__ball", style: { width: ball + "px", height: ball + "px", top: -Math.round(s * 0.3) + "px", marginLeft: -ball / 2 + "px" } }) : null,
    React.createElement("span", { className: "ly-tile__gloss" }),
    React.createElement("svg", { className: "ly-glyph", width: icon, height: icon, viewBox: "0 0 24 24", "aria-hidden": true },
      g.stroke ? React.createElement("path", { d: g.stroke, fill: "none", stroke: "#FFFFFF", strokeWidth: g.width || 2.6, strokeLinecap: "round", strokeLinejoin: "round" }) : null,
      g.fill ? React.createElement("path", { d: g.fill, fill: "#FFFFFF" }) : null));
  return React.createElement("div", {
    className: ["ly-tile-wrap", float && "ly-float", className].filter(Boolean).join(" "),
    style: style,
    role: label ? "img" : undefined,
    "aria-label": label || undefined,
    "aria-hidden": label ? undefined : true
  }, tile);
}
Object.assign(__ds_scope, { IconTile });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconTile.jsx", error: String((e && e.message) || e) }); }

// components/core/MonoLabel.jsx
try { (() => {
/* The uppercase Geist Mono eyebrow: names a panel, a figure or an axis. */
function MonoLabel({ tone = "muted", size, className, style, children }) {
  const cls = ["ly-label", tone !== "muted" && "ly-label--" + tone, className].filter(Boolean).join(" ");
  const s = size ? Object.assign({ fontSize: typeof size === "number" ? size + "px" : size }, style) : style;
  return React.createElement("div", { className: cls, style: s }, children);
}
Object.assign(__ds_scope, { MonoLabel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/MonoLabel.jsx", error: String((e && e.message) || e) }); }

// components/data/BarRow.jsx
try { (() => {
/* One row of a horizontal bar chart: mono label, bar, value.
   highlight = the one row the slide is about, in the accent with a glow. */
function BarRow({ label, value, fraction = 0, highlight = false, className, style }) {
  const f = Math.max(0, Math.min(1, Number(fraction) || 0));
  return React.createElement("div", {
    className: ["ly-bar", highlight && "ly-bar--highlight", className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("span", { className: "ly-bar__label" }, label),
    React.createElement("div", { className: "ly-bar__track" },
      React.createElement("div", { className: "ly-bar__fill", style: { width: f * 100 + "%" } })),
    React.createElement("span", { className: "ly-bar__value" }, value));
}
Object.assign(__ds_scope, { BarRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/BarRow.jsx", error: String((e && e.message) || e) }); }

// components/data/Stat.jsx
try { (() => {
/* A big figure with tabular numerals and its mono label underneath.
   tone: white (default), secondary for the losing side, accent for the winner.
   fit (default on) shrinks the figure to its column so "4,000+" never overflows. */
function Stat({ value, label, tone = "white", size, fit = true, className, style }) {
  const ref = React.useRef(null);
  const base = size ? (typeof size === "number" ? size + "px" : size) : "";
  React.useEffect(() => {
    const el = ref.current;
    if (!el || !fit) return undefined;
    let lastW = -1;
    const measure = () => {
      el.style.fontSize = base;
      const avail = el.clientWidth;
      if (!avail) return;
      lastW = avail;
      const need = el.scrollWidth;
      if (need > avail + 1) {
        const px = parseFloat(getComputedStyle(el).fontSize) * avail / need;
        el.style.fontSize = Math.floor(px) + "px";
      }
    };
    measure();
    const ro = typeof ResizeObserver !== "undefined"
      ? new ResizeObserver((entries) => { const w = Math.round(entries[0].contentRect.width); if (w !== lastW) measure(); })
      : null;
    if (ro && el.parentElement) ro.observe(el.parentElement);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    return () => { if (ro) ro.disconnect(); };
  }, [value, base, fit]);
  return React.createElement("div", {
    className: ["ly-stat", tone !== "white" && "ly-stat--" + tone, className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("div", { ref: ref, className: "ly-stat__value", style: base ? { fontSize: base } : undefined }, value),
    label ? React.createElement("div", { className: "ly-label" }, label) : null);
}
Object.assign(__ds_scope, { Stat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Stat.jsx", error: String((e && e.message) || e) }); }

// components/data/Track.jsx
try { (() => {
/* A thin channel with a travelling dot that shows speed. Use in pairs:
   a slow grey one against a fast, glowing accent one (highlight). */
function Track({ highlight = false, duration, className, style }) {
  const sec = Number(duration) || (highlight ? 0.9 : 6);
  return React.createElement("div", {
    className: ["ly-track", highlight && "ly-track--highlight", className].filter(Boolean).join(" "),
    style: style,
    "aria-hidden": true
  }, React.createElement("span", { className: "ly-track__dot", style: { animationDuration: sec + "s" } }));
}
Object.assign(__ds_scope, { Track });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Track.jsx", error: String((e && e.message) || e) }); }

// components/lists/DataTable.jsx
try { (() => {
/* A compact comparison or pricing table for a GlassPanel.
   columns: header labels. rows: arrays of cells, or { cells, tone: "dim" | "accent" }.
   highlightColumn: index of the column the slide is about (accent header, white bold cells).
   rowHeader: "strong" (first column bold white, default) or "label" (first column mono muted).
   template: optional grid-template-columns; default gives the first column a little more room.
   Keep it to 6 rows and 5 columns, with every cell one short line. */
function DataTable({ columns = [], rows = [], highlightColumn, rowHeader = "strong", template, className, style }) {
  const n = Math.max(columns.length, rows.reduce((m, r) => Math.max(m, (Array.isArray(r) ? r : (r && r.cells) || []).length), 0));
  const grid = template || ("minmax(0, 1.25fr) repeat(" + Math.max(n - 1, 1) + ", minmax(0, 1fr))");
  const cellClass = (ci) => {
    if (ci === 0) return "ly-table__cell ly-table__cell--head ly-table__cell--" + rowHeader;
    return ci === highlightColumn ? "ly-table__cell ly-table__cell--hl" : "ly-table__cell";
  };
  return React.createElement("div", { className: ["ly-table", className].filter(Boolean).join(" "), style: style, role: "table" },
    columns.length
      ? React.createElement("div", { className: "ly-table__row ly-table__row--header", style: { gridTemplateColumns: grid }, role: "row" },
        columns.map((c, ci) => React.createElement("span", { key: ci, role: "columnheader", className: ci === highlightColumn ? "ly-table__th ly-table__th--hl" : "ly-table__th" }, c)))
      : null,
    rows.map((r, ri) => {
      const cells = Array.isArray(r) ? r : (r && r.cells) || [];
      const tone = !Array.isArray(r) && r ? r.tone : null;
      return React.createElement("div", { key: ri, role: "row", className: ["ly-table__row", tone && "ly-table__row--" + tone].filter(Boolean).join(" "), style: { gridTemplateColumns: grid } },
        cells.map((c, ci) => React.createElement("span", { key: ci, role: "cell", className: cellClass(ci) }, c)));
    }));
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/lists/DataTable.jsx", error: String((e && e.message) || e) }); }

// components/lists/SpecRow.jsx
try { (() => {
/* One row of a spec list inside a GlassPanel. Consecutive rows get hairline dividers.
   layout "inline":  mono label on the left, value on the right   (Model · GPT-6 Astra)
   layout "stacked": small label above, big value below           (Chatting with your dot / Doesn't count)
   layout "feature": big label above, small description below     (Its own browser / Signs in with…)
   highlight puts the row in the slide accent; use it on one row. */
function SpecRow({ label, value, layout = "inline", highlight = false, className, style }) {
  const kind = ["inline", "stacked", "feature"].indexOf(layout) >= 0 ? layout : "inline";
  return React.createElement("div", {
    className: ["ly-spec", "ly-spec--" + kind, highlight && "ly-spec--highlight", className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("span", { className: "ly-spec__label" }, label),
    value != null ? React.createElement("span", { className: "ly-spec__value" }, value) : null);
}
Object.assign(__ds_scope, { SpecRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/lists/SpecRow.jsx", error: String((e && e.message) || e) }); }

// components/lists/StepList.jsx
try { (() => {
/* Numbered steps in order: an accent mono number and one line of instruction each. */
function StepList({ steps = [], start = 1, className, style }) {
  const first = Number(start) || 1;
  return React.createElement("ol", { className: ["ly-steps", className].filter(Boolean).join(" "), style: style },
    steps.map((s, i) => React.createElement("li", { key: i, className: "ly-steps__item" },
      React.createElement("span", { className: "ly-steps__num", "aria-hidden": true }, String(first + i).padStart(2, "0")),
      React.createElement("span", { className: "ly-steps__text" }, s))));
}
Object.assign(__ds_scope, { StepList });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/lists/StepList.jsx", error: String((e && e.message) || e) }); }

// components/paper/ChatBubble.jsx
try { (() => {
/* A chat message inside a ProductWindow. from="agent" (left, paper-2) or "you"
   (right, in the slide accent's wash). name adds a small mono sender line. */
function ChatBubble({ from = "agent", name, className, style, children }) {
  const you = from === "you";
  return React.createElement("div", {
    className: ["ly-chat", you ? "ly-chat--you" : "ly-chat--agent", className].filter(Boolean).join(" "),
    style: style
  },
    name ? React.createElement("span", { className: "ly-chat__name" }, name) : null,
    React.createElement("div", { className: "ly-chat__bubble" }, children));
}
Object.assign(__ds_scope, { ChatBubble });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/paper/ChatBubble.jsx", error: String((e && e.message) || e) }); }

// components/paper/Pill.jsx
try { (() => {
/* An uppercase type or status tag for paper UI: the -ink shade on its -wash. */
function Pill({ tone = "accent", className, style, children }) {
  return React.createElement("span", {
    className: ["ly-pill", "ly-pill--" + tone, className].filter(Boolean).join(" "),
    style: style
  }, children);
}
Object.assign(__ds_scope, { Pill });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/paper/Pill.jsx", error: String((e && e.message) || e) }); }

// components/paper/ProductWindow.jsx
try { (() => {
/* A white app window floating on the stage, with a tab bar and a mono badge. */
function ProductWindow({ tabs = [], active = 0, badge, className, style, children }) {
  const bar = tabs.length || badge
    ? React.createElement("div", { className: "ly-window__bar" },
      tabs.map((t, i) => {
        const on = typeof active === "number" ? i === active : t === active;
        return React.createElement("span", { key: i, className: on ? "ly-window__tab is-active" : "ly-window__tab" }, t);
      }),
      badge ? React.createElement("span", { className: "ly-window__badge" }, badge) : null)
    : null;
  return React.createElement("div", {
    className: ["ly-window", className].filter(Boolean).join(" "),
    style: style
  }, bar, React.createElement("div", { className: "ly-window__body" }, children));
}
Object.assign(__ds_scope, { ProductWindow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/paper/ProductWindow.jsx", error: String((e && e.message) || e) }); }

// components/paper/TaskCard.jsx
try { (() => {
/* A white card floating on the stage: a small glossy tile, a title and one line. */

const GLYPHS = {
  code: { stroke: "M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5" },
  arrow: { stroke: "M5 12h13M13 6.5l5.5 5.5-5.5 5.5" },
  check: { stroke: "M5 12.5l4.5 4.5L19 7.5" },
  shield: { stroke: "M12 3.2 19 6v5.6c0 4.3-2.9 7.9-7 9.2-4.1-1.3-7-4.9-7-9.2V6z" },
  sparkle: { fill: "M11 4l1.9 5.1L18 11l-5.1 1.9L11 18l-1.9-5.1L4 11l5.1-1.9zM18.5 14.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z" },
  bolt: { fill: "M13.5 2.5 5 13.5h6l-1.5 8 9-11.5h-6z" },
  bars: { fill: "M6.6 5.5h10.8a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 10.4h6.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 15.3h2.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2z" },
  eyes: { fill: "M8.4 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2zM15.6 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2z" }
};

function TaskCard({ title, description, color = "azure", glyph = "sparkle", float = false, className, style, children }) {
  const c = ["azure", "iris", "ember", "mint"].indexOf(color) >= 0 ? color : "azure";
  const g = GLYPHS[glyph] || GLYPHS.sparkle;
  return React.createElement("div", {
    className: ["ly-task", float && "ly-float", className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("div", { className: "ly-tile ly-tile--sm ly-tile--" + c, style: { width: "52px", height: "52px", borderRadius: "16px", flexShrink: 0 }, "aria-hidden": true },
      React.createElement("span", { className: "ly-tile__gloss" }),
      React.createElement("svg", { className: "ly-glyph", width: 28, height: 28, viewBox: "0 0 24 24" },
        g.stroke ? React.createElement("path", { d: g.stroke, fill: "none", stroke: "#FFFFFF", strokeWidth: 2.6, strokeLinecap: "round", strokeLinejoin: "round" }) : null,
        g.fill ? React.createElement("path", { d: g.fill, fill: "#FFFFFF" }) : null)),
    React.createElement("div", { className: "ly-task__text" },
      title ? React.createElement("div", { className: "ly-task__title" }, title) : null,
      description ? React.createElement("div", { className: "ly-task__desc" }, description) : null,
      children));
}
Object.assign(__ds_scope, { TaskCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/paper/TaskCard.jsx", error: String((e && e.message) || e) }); }

// components/slide/SlideTitle.jsx
try { (() => {
/* The title block every slide starts with: optional eyebrow, the title, one accent
   subtitle and an optional footnote, at fixed sizes so slides stay consistent.
   size: "display" (hero, 140px), "headline" (content slides, 96px) or
   "split" (two or three lines in a 700px column beside a visual, 108px).
   Children render above the eyebrow: put the icon tiles there. */
const SIZES = {
  display: { title: "var(--type-display)", lead: 1, track: "var(--track-display)", sub: "var(--type-subtitle)", gap: 52 },
  headline: { title: "var(--type-headline)", lead: 1.02, track: "var(--track-headline)", sub: "40px", gap: 22 },
  split: { title: "108px", lead: 1.04, track: "var(--track-display)", sub: "44px", gap: 44 }
};

function SlideTitle({ eyebrow, title, subtitle, note, size = "headline", className, style, children }) {
  const s = SIZES[size] || SIZES.headline;
  return React.createElement("div", { className: ["ly-title", "ly-title--" + (SIZES[size] ? size : "headline"), className].filter(Boolean).join(" "), style: style },
    children,
    eyebrow ? React.createElement("div", { className: "ly-label ly-title__eyebrow" }, eyebrow) : null,
    React.createElement("h1", { className: "ly-title__main", style: { fontSize: s.title, lineHeight: s.lead, letterSpacing: s.track } }, title),
    subtitle ? React.createElement("p", { className: "ly-title__sub", style: { fontSize: s.sub, marginTop: s.gap + "px" } }, subtitle) : null,
    note ? React.createElement("p", { className: "ly-title__note" }, note) : null);
}
Object.assign(__ds_scope, { SlideTitle });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slide/SlideTitle.jsx", error: String((e && e.message) || e) }); }

// components/slide/Stage.jsx
try { (() => {
/* The 1920×1080 slide: a graphite stage lit from above, two soft light beams,
   the horizon wave (a dot field under a drifting crest that glows in the slide
   accent) and a vignette. Children sit in the safe area, left of the webcam lane. */

const ACCENTS = {
  azure: [47, 149, 255],
  ember: [255, 138, 91],
  iris: [156, 124, 255],
  mint: [79, 214, 160]
};

function parseColor(s) {
  if (!s) return null;
  s = String(s).trim();
  let m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(s);
  if (m) {
    const x = m[1].length === 3 ? m[1].replace(/./g, (c) => c + c) : m[1];
    return [parseInt(x.slice(0, 2), 16), parseInt(x.slice(2, 4), 16), parseInt(x.slice(4, 6), 16)];
  }
  m = /^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)/i.exec(s);
  return m ? [Math.round(+m[1]), Math.round(+m[2]), Math.round(+m[3])] : null;
}

/* Where the crest sits. "low" keeps it below y≈800 so text on the bare stage
   stays clear of it; "high" is for slides whose lower half is empty. */
const LEVELS = { low: [880, 0.7], middle: [800, 0.85], high: [740, 1] };

function paintWave(ctx, t, rgb, k, base, amp) {
  const W = 1920, H = 1080, S = 12;
  const cols = Math.ceil(W / S) + 1;
  const tint = (a) => "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + "," + Math.min(a * k, 1) + ")";
  const tops = [];
  for (let i = 0; i < cols; i++) {
    const x = i * S + S / 2;
    tops.push(base + amp * (70 * Math.sin(x * 0.0031 + t * 0.22) + 34 * Math.sin(x * 0.0087 - t * 0.37) + 16 * Math.sin(x * 0.019 + t * 0.61)));
  }
  ctx.clearRect(0, 0, W, H);
  ctx.lineJoin = "round";
  ctx.lineCap = "round";
  [[120 * amp, 0.03], [56 * amp, 0.05], [18 * amp, 0.09]].forEach(([width, alpha]) => {
    ctx.beginPath();
    for (let i = 0; i < cols; i++) {
      const x = i * S + S / 2;
      if (i) ctx.lineTo(x, tops[i]); else ctx.moveTo(x, tops[i]);
    }
    ctx.lineWidth = width;
    ctx.strokeStyle = tint(alpha);
    ctx.stroke();
  });
  const first = tops.map((y) => Math.ceil(y / S));
  const rows = Math.ceil(H / S);
  const depth = rows - Math.min.apply(null, first);
  for (let d = 0; d < depth; d++) {
    const rad = d === 0 ? 2.2 : d === 1 ? 1.8 : 1.5;
    ctx.beginPath();
    for (let i = 0; i < cols; i++) {
      const row = first[i] + d;
      if (row >= rows) continue;
      const x = i * S + S / 2, y = row * S + S / 2;
      ctx.moveTo(x + rad, y);
      ctx.arc(x, y, rad, 0, 6.2832);
    }
    ctx.fillStyle = d === 0 ? tint(0.95) : d === 1 ? tint(0.45)
      : "rgba(255,255,255," + Math.min(Math.max(0.08, 0.2 - d * 0.004) * k, 1) + ")";
    ctx.fill();
  }
}

function Stage({ accent = "azure", wave = true, waveIntensity = 1, waveLevel = "low", showLane = false, fullBleed = false, className, style, children }) {
  const name = ACCENTS[accent] ? accent : "azure";
  const k = Number(waveIntensity) || 1;
  const level = LEVELS[waveLevel] ? waveLevel : "low";
  const rootRef = React.useRef(null);
  const canvasRef = React.useRef(null);
  React.useEffect(() => {
    const c = canvasRef.current;
    if (!wave || !c) return undefined;
    const rgb = parseColor(getComputedStyle(rootRef.current).getPropertyValue("--slide-accent")) || ACCENTS[name];
    const still = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    const ctx = c.getContext("2d");
    let raf = 0, last = -1000, drawn = false;
    const frame = (ms) => {
      raf = requestAnimationFrame(frame);
      if (ms - last < 33 || (still && drawn)) return;
      if (!c.isConnected || !c.getClientRects().length) return;
      last = ms;
      drawn = true;
      paintWave(ctx, ms / 1000, rgb, k, LEVELS[level][0], LEVELS[level][1]);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [wave, name, k, level]);
  return React.createElement("div", {
    ref: rootRef,
    className: ["ly-stage", "ly-accent-" + name, className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("div", { className: "ly-stage__beam ly-stage__beam--a", "aria-hidden": true }),
    React.createElement("div", { className: "ly-stage__beam ly-stage__beam--b", "aria-hidden": true }),
    wave ? React.createElement("canvas", { ref: canvasRef, className: "ly-stage__wave", width: 1920, height: 1080, "aria-hidden": true }) : null,
    React.createElement("div", { className: "ly-stage__vignette", "aria-hidden": true }),
    showLane ? React.createElement("div", { className: "ly-stage__lane", "aria-hidden": true }) : null,
    React.createElement("div", { className: fullBleed ? "ly-stage__full" : "ly-stage__safe" }, children));
}
Object.assign(__ds_scope, { Stage });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slide/Stage.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/CodePanel.jsx
try { (() => {
/* A frosted-glass code block with line numbers and syntax colours, optionally
   with the glowing accent cursor at its top-left corner. */

const KEYWORDS = /^(?:const|let|var|await|async|return|function|new|import|from|export|if|else|for|while|class|def|GET|POST|PUT|PATCH|DELETE)\b/;
const LITERALS = /^(?:true|false|null|undefined|None|True|False)\b/;

function highlight(text, inString) {
  const parts = [];
  let key = 0;
  let i = 0;
  let m;
  const push = (kind, s) => {
    if (!s) return;
    parts.push(kind ? React.createElement("span", { key: key++, className: "ly-code__" + kind }, s) : s);
  };
  const wordBefore = () => /[A-Za-z0-9_$.]/.test(text.charAt(i - 1));
  if (inString) {
    const close = text.indexOf('"');
    if (close === -1) {
      push("str", text);
      return { parts, inString: true };
    }
    push("str", text.slice(0, close + 1));
    i = close + 1;
  }
  while (i < text.length) {
    const rest = text.slice(i);
    if (rest.slice(0, 2) === "//" || (rest.charAt(0) === "#" && /^\s*$/.test(text.slice(0, i)))) {
      push("com", rest);
      break;
    }
    const q = rest.charAt(0);
    if (q === '"' || q === "'") {
      const end = rest.indexOf(q, 1);
      if (end === -1) {
        push("str", rest);
        return { parts, inString: q === '"' };
      }
      push(/^\s*:/.test(rest.slice(end + 1)) ? "key" : "str", rest.slice(0, end + 1));
      i += end + 1;
      continue;
    }
    if (!wordBefore() && (m = LITERALS.exec(rest))) { push("val", m[0]); i += m[0].length; continue; }
    if (!wordBefore() && (m = KEYWORDS.exec(rest))) { push("kw", m[0]); i += m[0].length; continue; }
    if (!wordBefore() && (m = /^-?\d+(?:\.\d+)?/.exec(rest))) { push("val", m[0]); i += m[0].length; continue; }
    m = /^[A-Za-z_$][A-Za-z0-9_$]*|^[^"'A-Za-z_$0-9#\/-]+|^[\s\S]/.exec(rest);
    push(null, m[0]);
    i += m[0].length;
  }
  return { parts, inString: false };
}

function codeRows(lines, code, children, startLine) {
  let src = lines;
  if (!src || !src.length) {
    const text = code != null ? code : (typeof children === "string" ? children : "");
    src = String(text).replace(/^\n/, "").replace(/\n\s*$/, "").split("\n");
  }
  let n = startLine == null ? 1 : Number(startLine) || 1;
  return src.map((item) => {
    const obj = item && typeof item === "object";
    return { text: obj ? String(item.text || "") : String(item), num: obj && item.wrap ? null : n++ };
  });
}

function CodePanel({ lines, code, cursor = false, glow, fontSize, startLine, className, style, children }) {
  const rows = codeRows(lines, code, children, startLine);
  const cells = [];
  let inString = false;
  rows.forEach((row, i) => {
    const res = highlight(row.text, inString);
    inString = res.inString;
    cells.push(React.createElement("span", { key: "n" + i, className: "ly-code__ln" }, row.num == null ? "" : String(row.num)));
    cells.push(React.createElement("span", { key: "l" + i, className: "ly-code__line" }, res.parts));
  });
  const bloom = glow == null ? !!cursor : !!glow;
  return React.createElement("div", { className: ["ly-code", className].filter(Boolean).join(" "), style: style },
    bloom ? React.createElement("div", { className: "ly-code__bloom", "aria-hidden": true }) : null,
    React.createElement("div", { className: "ly-code__panel", style: fontSize ? { fontSize: typeof fontSize === "number" ? fontSize + "px" : fontSize } : undefined },
      React.createElement("div", { className: "ly-code__grid" }, cells)),
    cursor
      ? React.createElement("div", { className: "ly-code__cursor", "aria-hidden": true },
        React.createElement("svg", { className: "ly-cursor", width: 84, height: 84, viewBox: "0 0 40 40" },
          React.createElement("path", { d: "M7 6 L34 16.5 L21.5 20.5 L16.5 33 Z" })))
      : null);
}
Object.assign(__ds_scope, { CodePanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/CodePanel.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/GlassPanel.jsx
try { (() => {
/* Frosted glass over the stage: the container for comparisons and charts.
   highlight = accent border and glow, for the winning side (once per slide). */
function GlassPanel({ highlight = false, padding, className, style, children }) {
  const s = padding != null ? Object.assign({ padding: typeof padding === "number" ? padding + "px" : padding }, style) : style;
  return React.createElement("div", {
    className: ["ly-glass", highlight && "ly-glass--highlight", className].filter(Boolean).join(" "),
    style: s
  }, children);
}
Object.assign(__ds_scope, { GlassPanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/GlassPanel.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Cursor = __ds_scope.Cursor;

__ds_ns.IconTile = __ds_scope.IconTile;

__ds_ns.MonoLabel = __ds_scope.MonoLabel;

__ds_ns.BarRow = __ds_scope.BarRow;

__ds_ns.Stat = __ds_scope.Stat;

__ds_ns.Track = __ds_scope.Track;

__ds_ns.DataTable = __ds_scope.DataTable;

__ds_ns.SpecRow = __ds_scope.SpecRow;

__ds_ns.StepList = __ds_scope.StepList;

__ds_ns.ChatBubble = __ds_scope.ChatBubble;

__ds_ns.Pill = __ds_scope.Pill;

__ds_ns.ProductWindow = __ds_scope.ProductWindow;

__ds_ns.TaskCard = __ds_scope.TaskCard;

__ds_ns.SlideTitle = __ds_scope.SlideTitle;

__ds_ns.Stage = __ds_scope.Stage;

__ds_ns.CodePanel = __ds_scope.CodePanel;

__ds_ns.GlassPanel = __ds_scope.GlassPanel;

})();
