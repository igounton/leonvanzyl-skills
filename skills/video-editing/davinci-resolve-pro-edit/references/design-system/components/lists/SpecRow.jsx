import React from "react";

/* One row of a spec list inside a GlassPanel. Consecutive rows get hairline dividers.
   layout "inline":  mono label on the left, value on the right   (Model · GPT-6 Astra)
   layout "stacked": small label above, big value below           (Chatting with your dot / Doesn't count)
   layout "feature": big label above, small description below     (Its own browser / Signs in with…)
   highlight puts the row in the slide accent; use it on one row. */
export function SpecRow({ label, value, layout = "inline", highlight = false, className, style }) {
  const kind = ["inline", "stacked", "feature"].indexOf(layout) >= 0 ? layout : "inline";
  return React.createElement("div", {
    className: ["ly-spec", "ly-spec--" + kind, highlight && "ly-spec--highlight", className].filter(Boolean).join(" "),
    style: style
  },
    React.createElement("span", { className: "ly-spec__label" }, label),
    value != null ? React.createElement("span", { className: "ly-spec__value" }, value) : null);
}
