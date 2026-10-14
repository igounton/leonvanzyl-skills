import type * as React from "react";

export interface SpecRowProps {
  /** inline: the mono key. stacked: the small line on top. feature: the big heading. */
  label: React.ReactNode;
  /** inline: the value. stacked: the big line below. feature: the description. */
  value?: React.ReactNode;
  /** Default "inline". */
  layout?: "inline" | "stacked" | "feature";
  /** Puts the row in the slide accent. One row per list. */
  highlight?: boolean;
  className?: string;
  style?: React.CSSProperties;
}
export declare function SpecRow(props: SpecRowProps): React.ReactElement;
