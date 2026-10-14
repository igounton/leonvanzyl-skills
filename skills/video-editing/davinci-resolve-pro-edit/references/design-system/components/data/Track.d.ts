import type * as React from "react";

export interface TrackProps {
  /** Accent dot for the fast side. Default false. */
  highlight?: boolean;
  /** Seconds per pass. Default 6, or 0.9 when highlighted. */
  duration?: number;
  className?: string;
  style?: React.CSSProperties;
}
export declare function Track(props: TrackProps): React.ReactElement;
