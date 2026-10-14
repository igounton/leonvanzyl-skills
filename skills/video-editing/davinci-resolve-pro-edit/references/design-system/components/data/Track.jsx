import React from "react";

/* A thin channel with a travelling dot that shows speed. Use in pairs:
   a slow grey one against a fast, glowing accent one (highlight). */
export function Track({ highlight = false, duration, className, style }) {
  const sec = Number(duration) || (highlight ? 0.9 : 6);
  return React.createElement("div", {
    className: ["ly-track", highlight && "ly-track--highlight", className].filter(Boolean).join(" "),
    style: style,
    "aria-hidden": true
  }, React.createElement("span", { className: "ly-track__dot", style: { animationDuration: sec + "s" } }));
}
