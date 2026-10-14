import React from "react";

/* A compact comparison or pricing table for a GlassPanel.
   columns: header labels. rows: arrays of cells, or { cells, tone: "dim" | "accent" }.
   highlightColumn: index of the column the slide is about (accent header, white bold cells).
   rowHeader: "strong" (first column bold white, default) or "label" (first column mono muted).
   template: optional grid-template-columns; default gives the first column a little more room.
   Keep it to 6 rows and 5 columns, with every cell one short line. */
export function DataTable({ columns = [], rows = [], highlightColumn, rowHeader = "strong", template, className, style }) {
  const n = Math.max(columns.length, rows.reduce((m, r) => Math.max(m, (Array.isArray(r) ? r : (r && r.cells) || []).length), 0));
  const grid = template || ("minmax(0, 1.25fr) repeat(" + Math.max(n - 1, 1) + ", minmax(0, 1fr))");
  const cellClass = (ci) => {
    if (ci === 0) return "ly-table__cell ly-table__cell--head ly-table__cell--" + rowHeader;
    return ci === highlightColumn ? "ly-table__cell ly-table__cell--hl" : "ly-table__cell";
  };
  return React.createElement("div", { className: ["ly-table", className].filter(Boolean).join(" "), style: style, role: "table" },
    columns.length
      ? React.createElement("div", { className: "ly-table__row ly-table__row--header", style: { gridTemplateColumns: grid }, role: "row" },
        columns.map((c, ci) => React.createElement("span", { key: ci, role: "columnheader", className: ci === highlightColumn ? "ly-table__th ly-table__th--hl" : "ly-table__th" }, c)))
      : null,
    rows.map((r, ri) => {
      const cells = Array.isArray(r) ? r : (r && r.cells) || [];
      const tone = !Array.isArray(r) && r ? r.tone : null;
      return React.createElement("div", { key: ri, role: "row", className: ["ly-table__row", tone && "ly-table__row--" + tone].filter(Boolean).join(" "), style: { gridTemplateColumns: grid } },
        cells.map((c, ci) => React.createElement("span", { key: ci, role: "cell", className: cellClass(ci) }, c)));
    }));
}
