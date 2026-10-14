import React from "react";

/* A chat message inside a ProductWindow. from="agent" (left, paper-2) or "you"
   (right, in the slide accent's wash). name adds a small mono sender line. */
export function ChatBubble({ from = "agent", name, className, style, children }) {
  const you = from === "you";
  return React.createElement("div", {
    className: ["ly-chat", you ? "ly-chat--you" : "ly-chat--agent", className].filter(Boolean).join(" "),
    style: style
  },
    name ? React.createElement("span", { className: "ly-chat__name" }, name) : null,
    React.createElement("div", { className: "ly-chat__bubble" }, children));
}
