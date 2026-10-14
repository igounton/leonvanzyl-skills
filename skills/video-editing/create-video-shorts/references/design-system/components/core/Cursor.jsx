import React from "react";

/* The glowing pointer in the slide accent, with a thick white outline. */
export function Cursor({ size = 84, className, style }) {
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
