import React from "react";

/* A big figure with tabular numerals and its mono label underneath.
   tone: white (default), secondary for the losing side, accent for the winner.
   fit (default on) shrinks the figure to its column so "4,000+" never overflows. */
export function Stat({ value, label, tone = "white", size, fit = true, className, style }) {
  const ref = React.useRef(null);
  const base = size ? (typeof size === "number" ? size + "px" : size) : "";
  React.useEffect(() => {
    const el = ref.current;
    if (!el || !fit) return undefined;
    let lastW = -1;
    const measure = () => {
      el.style.fontSize = base;
      const avail = el.clientWidth;
      if (!avail) return;
      lastW = avail;
      const need = el.scrollWidth;
      if (need > avail + 1) {
        const px = parseFloat(getComputedStyle(el).fontSize) * avail / need;
        el.style.fontSize = Math.floor(px) + "px";
      }
    };
    measure();
    const ro = typeof ResizeObserver !== "undefined"
      ? new ResizeObserver((entries) => { const w = Math.round(entries[0].contentRect.width); if (w !== lastW) measure(); })
      : null;
    if (ro && el.parentElement) ro.observe(el.parentElement);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    return () => { if (ro) ro.disconnect(); };
  }, [value, base, fit]);
  return React.createElement("div", {
    className: ["ly-stat", tone !== "white" && "ly-stat--" + tone, className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("div", { ref: ref, className: "ly-stat__value", style: base ? { fontSize: base } : undefined }, value),
    label ? React.createElement("div", { className: "ly-label" }, label) : null);
}
