import type * as React from "react";

export interface GlassPanelProps {
  /** Accent border and glow for the winning side. Default false. */
  highlight?: boolean;
  /** A number is px. Default var(--panel-pad), 44px. */
  padding?: number | string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function GlassPanel(props: GlassPanelProps): React.ReactElement;
