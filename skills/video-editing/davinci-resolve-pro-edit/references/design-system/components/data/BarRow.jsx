import React from "react";

/* One row of a horizontal bar chart: mono label, bar, value.
   highlight = the one row the slide is about, in the accent with a glow. */
export function BarRow({ label, value, fraction = 0, highlight = false, className, style }) {
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
