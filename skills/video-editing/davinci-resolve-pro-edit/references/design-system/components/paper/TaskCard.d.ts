import type * as React from "react";

export interface TaskCardProps {
  title?: React.ReactNode;
  description?: React.ReactNode;
  /** Colour of the small tile. Default "azure". */
  color?: "azure" | "iris" | "ember" | "mint";
  /** Default "sparkle". */
  glyph?: "code" | "eyes" | "shield" | "sparkle" | "bars" | "bolt" | "arrow" | "check";
  float?: boolean;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function TaskCard(props: TaskCardProps): React.ReactElement;
