import type * as React from "react";

export interface StatProps {
  /** Include the unit: "70–500 ms", "$21", "4,000+". */
  value: React.ReactNode;
  label?: React.ReactNode;
  /** "accent" marks the winner (it glows); "secondary" the other side. Default "white". */
  tone?: "white" | "secondary" | "accent";
  /** A number is px. Default var(--type-stat), 112px; 220 for a big-stat slide. */
  size?: number | string;
  /** Shrink the figure to fit its column. Default true. */
  fit?: boolean;
  className?: string;
  style?: React.CSSProperties;
}
export declare function Stat(props: StatProps): React.ReactElement;
