import type * as React from "react";

export interface BarRowProps {
  label: React.ReactNode;
  value: React.ReactNode;
  /** Bar length, 0 to 1, relative to the largest row. Tiny values still show a 14px stub. */
  fraction: number;
  highlight?: boolean;
  className?: string;
  style?: React.CSSProperties;
}
export declare function BarRow(props: BarRowProps): React.ReactElement;
