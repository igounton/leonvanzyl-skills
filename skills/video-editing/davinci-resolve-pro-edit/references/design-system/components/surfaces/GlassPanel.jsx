import React from "react";

/* Frosted glass over the stage: the container for comparisons and charts.
   highlight = accent border and glow, for the winning side (once per slide). */
export function GlassPanel({ highlight = false, padding, className, style, children }) {
  const s = padding != null ? Object.assign({ padding: typeof padding === "number" ? padding + "px" : padding }, style) : style;
  return React.createElement("div", {
    className: ["ly-glass", highlight && "ly-glass--highlight", className].filter(Boolean).join(" "),
    style: s
  }, children);
}
