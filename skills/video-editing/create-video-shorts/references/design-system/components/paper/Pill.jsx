import React from "react";

/* An uppercase type or status tag for paper UI: the -ink shade on its -wash. */
export function Pill({ tone = "accent", className, style, children }) {
  return React.createElement("span", {
    className: ["ly-pill", "ly-pill--" + tone, className].filter(Boolean).join(" "),
    style: style
  }, children);
}
