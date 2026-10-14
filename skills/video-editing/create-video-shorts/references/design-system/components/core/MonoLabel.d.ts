import type * as React from "react";

export interface MonoLabelProps {
  /** Default "muted". */
  tone?: "muted" | "secondary" | "accent" | "white";
  /** Font size; a number is px. Default var(--type-label), 22px. */
  size?: number | string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function MonoLabel(props: MonoLabelProps): React.ReactElement;
