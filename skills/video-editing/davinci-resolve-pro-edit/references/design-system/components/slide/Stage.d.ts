import type * as React from "react";

export interface StageProps {
  /** The slide accent: subtitle line, winning figure, highlighted panel, cursor and wave crest. Default "azure". */
  accent?: "azure" | "ember" | "iris" | "mint";
  /** The animated horizon wave. Default true. */
  wave?: boolean;
  /** Wave brightness, 0.4 to 2.5. Default 1. */
  waveIntensity?: number;
  /** Where the crest sits. "low" (default) keeps it below y≈800 so text stays clear; "middle" and "high" only when the lower half is empty. */
  waveLevel?: "low" | "middle" | "high";
  /** Tints the 380px webcam lane while laying out. Turn off before recording. Default false. */
  showLane?: boolean;
  /** Children get the whole 1920×1080 frame instead of the 1440×880 safe area. Default false. */
  fullBleed?: boolean;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function Stage(props: StageProps): React.ReactElement;
