import React from "react";

/* The uppercase Geist Mono eyebrow: names a panel, a figure or an axis. */
export function MonoLabel({ tone = "muted", size, className, style, children }) {
  const cls = ["ly-label", tone !== "muted" && "ly-label--" + tone, className].filter(Boolean).join(" ");
  const s = size ? Object.assign({ fontSize: typeof size === "number" ? size + "px" : size }, style) : style;
  return React.createElement("div", { className: cls, style: s }, children);
}
