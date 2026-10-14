import React from "react";

/* Numbered steps in order: an accent mono number and one line of instruction each. */
export function StepList({ steps = [], start = 1, className, style }) {
  const first = Number(start) || 1;
  return React.createElement("ol", { className: ["ly-steps", className].filter(Boolean).join(" "), style: style },
    steps.map((s, i) => React.createElement("li", { key: i, className: "ly-steps__item" },
      React.createElement("span", { className: "ly-steps__num", "aria-hidden": true }, String(first + i).padStart(2, "0")),
      React.createElement("span", { className: "ly-steps__text" }, s))));
}
