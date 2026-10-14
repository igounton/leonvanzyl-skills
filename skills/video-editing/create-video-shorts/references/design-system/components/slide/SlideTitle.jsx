import React from "react";

/* The title block every slide starts with: optional eyebrow, the title, one accent
   subtitle and an optional footnote, at fixed sizes so slides stay consistent.
   size: "display" (hero, 140px), "headline" (content slides, 96px) or
   "split" (two or three lines in a 700px column beside a visual, 108px).
   Children render above the eyebrow: put the icon tiles there. */
const SIZES = {
  display: { title: "var(--type-display)", lead: 1, track: "var(--track-display)", sub: "var(--type-subtitle)", gap: 52 },
  headline: { title: "var(--type-headline)", lead: 1.02, track: "var(--track-headline)", sub: "40px", gap: 22 },
  split: { title: "108px", lead: 1.04, track: "var(--track-display)", sub: "44px", gap: 44 }
};

export function SlideTitle({ eyebrow, title, subtitle, note, size = "headline", className, style, children }) {
  const s = SIZES[size] || SIZES.headline;
  return React.createElement("div", { className: ["ly-title", "ly-title--" + (SIZES[size] ? size : "headline"), className].filter(Boolean).join(" "), style: style },
    children,
    eyebrow ? React.createElement("div", { className: "ly-label ly-title__eyebrow" }, eyebrow) : null,
    React.createElement("h1", { className: "ly-title__main", style: { fontSize: s.title, lineHeight: s.lead, letterSpacing: s.track } }, title),
    subtitle ? React.createElement("p", { className: "ly-title__sub", style: { fontSize: s.sub, marginTop: s.gap + "px" } }, subtitle) : null,
    note ? React.createElement("p", { className: "ly-title__note" }, note) : null);
}
