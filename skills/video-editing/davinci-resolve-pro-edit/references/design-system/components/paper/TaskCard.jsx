import React from "react";

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

export function TaskCard({ title, description, color = "azure", glyph = "sparkle", float = false, className, style, children }) {
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
