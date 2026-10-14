import type * as React from "react";

export type DataRow = React.ReactNode[] | { cells: React.ReactNode[]; tone?: "dim" | "accent" };

export interface DataTableProps {
  /** Header labels, shown as mono uppercase. */
  columns?: React.ReactNode[];
  /** One entry per row. A { cells, tone } row can be dimmed (not available) or put in the accent. */
  rows: DataRow[];
  /** Index of the column the slide is about: accent header, white bold cells. */
  highlightColumn?: number;
  /** "strong" (default): first column bold white. "label": first column mono muted, for row keys like "Runs on". */
  rowHeader?: "strong" | "label";
  /** grid-template-columns override. Default: first column 1.25fr, the rest 1fr. */
  template?: string;
  className?: string;
  style?: React.CSSProperties;
}
export declare function DataTable(props: DataTableProps): React.ReactElement;
