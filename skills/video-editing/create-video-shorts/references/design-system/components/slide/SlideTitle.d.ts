import type * as React from "react";

export interface SlideTitleProps {
  /** Mono uppercase line above the title, e.g. "DevDay 2026 · September 29". */
  eyebrow?: React.ReactNode;
  /** The title. "\n" in a string forces a line break. */
  title: React.ReactNode;
  /** One clause in the slide accent. */
  subtitle?: React.ReactNode;
  /** Optional footnote or source in text-muted, under the subtitle. */
  note?: React.ReactNode;
  /** "display" = hero, 140px, subtitle 46px. "headline" = content slides, 96px, subtitle 40px (default).
      "split" = 108px in a 700px column beside a visual, subtitle 44px. */
  size?: "display" | "headline" | "split";
  className?: string;
  style?: React.CSSProperties;
  /** Rendered above the eyebrow: icon tiles go here. */
  children?: React.ReactNode;
}
export declare function SlideTitle(props: SlideTitleProps): React.ReactElement;
