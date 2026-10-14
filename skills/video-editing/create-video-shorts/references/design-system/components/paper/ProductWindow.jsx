import React from "react";

/* A white app window floating on the stage, with a tab bar and a mono badge. */
export function ProductWindow({ tabs = [], active = 0, badge, className, style, children }) {
  const bar = tabs.length || badge
    ? React.createElement("div", { className: "ly-window__bar" },
      tabs.map((t, i) => {
        const on = typeof active === "number" ? i === active : t === active;
        return React.createElement("span", { key: i, className: on ? "ly-window__tab is-active" : "ly-window__tab" }, t);
      }),
      badge ? React.createElement("span", { className: "ly-window__badge" }, badge) : null)
    : null;
  return React.createElement("div", {
    className: ["ly-window", className].filter(Boolean).join(" "),
    style: style
  }, bar, React.createElement("div", { className: "ly-window__body" }, children));
}
