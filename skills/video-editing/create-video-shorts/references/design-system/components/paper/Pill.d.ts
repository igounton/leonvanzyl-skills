import type * as React from "react";

export interface PillProps {
  /** "accent" follows the slide accent. Default "accent". */
  tone?: "accent" | "azure" | "ember" | "iris" | "mint" | "neutral";
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function Pill(props: PillProps): React.ReactElement;
