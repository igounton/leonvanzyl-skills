import React from "react";

/* A frosted-glass code block with line numbers and syntax colours, optionally
   with the glowing accent cursor at its top-left corner. */

const KEYWORDS = /^(?:const|let|var|await|async|return|function|new|import|from|export|if|else|for|while|class|def|GET|POST|PUT|PATCH|DELETE)\b/;
const LITERALS = /^(?:true|false|null|undefined|None|True|False)\b/;

function highlight(text, inString) {
  const parts = [];
  let key = 0;
  let i = 0;
  let m;
  const push = (kind, s) => {
    if (!s) return;
    parts.push(kind ? React.createElement("span", { key: key++, className: "ly-code__" + kind }, s) : s);
  };
  const wordBefore = () => /[A-Za-z0-9_$.]/.test(text.charAt(i - 1));
  if (inString) {
    const close = text.indexOf('"');
    if (close === -1) {
      push("str", text);
      return { parts, inString: true };
    }
    push("str", text.slice(0, close + 1));
    i = close + 1;
  }
  while (i < text.length) {
    const rest = text.slice(i);
    if (rest.slice(0, 2) === "//" || (rest.charAt(0) === "#" && /^\s*$/.test(text.slice(0, i)))) {
      push("com", rest);
      break;
    }
    const q = rest.charAt(0);
    if (q === '"' || q === "'") {
      const end = rest.indexOf(q, 1);
      if (end === -1) {
        push("str", rest);
        return { parts, inString: q === '"' };
      }
      push(/^\s*:/.test(rest.slice(end + 1)) ? "key" : "str", rest.slice(0, end + 1));
      i += end + 1;
      continue;
    }
    if (!wordBefore() && (m = LITERALS.exec(rest))) { push("val", m[0]); i += m[0].length; continue; }
    if (!wordBefore() && (m = KEYWORDS.exec(rest))) { push("kw", m[0]); i += m[0].length; continue; }
    if (!wordBefore() && (m = /^-?\d+(?:\.\d+)?/.exec(rest))) { push("val", m[0]); i += m[0].length; continue; }
    m = /^[A-Za-z_$][A-Za-z0-9_$]*|^[^"'A-Za-z_$0-9#\/-]+|^[\s\S]/.exec(rest);
    push(null, m[0]);
    i += m[0].length;
  }
  return { parts, inString: false };
}

function codeRows(lines, code, children, startLine) {
  let src = lines;
  if (!src || !src.length) {
    const text = code != null ? code : (typeof children === "string" ? children : "");
    src = String(text).replace(/^\n/, "").replace(/\n\s*$/, "").split("\n");
  }
  let n = startLine == null ? 1 : Number(startLine) || 1;
  return src.map((item) => {
    const obj = item && typeof item === "object";
    return { text: obj ? String(item.text || "") : String(item), num: obj && item.wrap ? null : n++ };
  });
}

export function CodePanel({ lines, code, cursor = false, glow, fontSize, startLine, className, style, children }) {
  const rows = codeRows(lines, code, children, startLine);
  const cells = [];
  let inString = false;
  rows.forEach((row, i) => {
    const res = highlight(row.text, inString);
    inString = res.inString;
    cells.push(React.createElement("span", { key: "n" + i, className: "ly-code__ln" }, row.num == null ? "" : String(row.num)));
    cells.push(React.createElement("span", { key: "l" + i, className: "ly-code__line" }, res.parts));
  });
  const bloom = glow == null ? !!cursor : !!glow;
  return React.createElement("div", { className: ["ly-code", className].filter(Boolean).join(" "), style: style },
    bloom ? React.createElement("div", { className: "ly-code__bloom", "aria-hidden": true }) : null,
    React.createElement("div", { className: "ly-code__panel", style: fontSize ? { fontSize: typeof fontSize === "number" ? fontSize + "px" : fontSize } : undefined },
      React.createElement("div", { className: "ly-code__grid" }, cells)),
    cursor
      ? React.createElement("div", { className: "ly-code__cursor", "aria-hidden": true },
        React.createElement("svg", { className: "ly-cursor", width: 84, height: 84, viewBox: "0 0 40 40" },
          React.createElement("path", { d: "M7 6 L34 16.5 L21.5 20.5 L16.5 33 Z" })))
      : null);
}
