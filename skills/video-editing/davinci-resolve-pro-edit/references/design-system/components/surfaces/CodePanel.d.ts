import type * as React from "react";

export type CodeLine = string | { text: string; wrap?: boolean };

export interface CodePanelProps {
  /** One entry per line; { text, wrap: true } continues the previous line without a number. */
  lines?: CodeLine[];
  /** Alternative to lines: the code as one string, split on newlines. */
  code?: string;
  /** The glowing accent pointer at the top-left corner. Default false. */
  cursor?: boolean;
  /** Accent bloom behind the top-left corner. Default: on when cursor is. */
  glow?: boolean;
  /** Default var(--type-code), 22px. */
  fontSize?: number | string;
  /** Default 1. */
  startLine?: number;
  className?: string;
  style?: React.CSSProperties;
  children?: string;
}
export declare function CodePanel(props: CodePanelProps): React.ReactElement;
