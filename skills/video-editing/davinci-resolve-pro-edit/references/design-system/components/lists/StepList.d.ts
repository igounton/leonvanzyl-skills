import type * as React from "react";

export interface StepListProps {
  /** One short instruction per step, in order. */
  steps: React.ReactNode[];
  /** First number. Default 1, shown as "01". */
  start?: number;
  className?: string;
  style?: React.CSSProperties;
}
export declare function StepList(props: StepListProps): React.ReactElement;
