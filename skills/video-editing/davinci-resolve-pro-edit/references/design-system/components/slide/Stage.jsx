import React from "react";

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

export function Stage({ accent = "azure", wave = true, waveIntensity = 1, waveLevel = "low", showLane = false, fullBleed = false, className, style, children }) {
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
