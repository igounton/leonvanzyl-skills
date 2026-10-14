import React from "react";

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

export function IconTile({ color = "azure", glyph = "code", size = 116, tilt = -8, antenna, float = false, label, className, style }) {
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
