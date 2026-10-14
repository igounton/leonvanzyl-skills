import type * as React from "react";

export interface IconTileProps {
  /** Default "azure". */
  color?: "azure" | "iris" | "ember" | "mint";
  /** Default "code". "eyes" is a robot face and adds an antenna. */
  glyph?: "code" | "eyes" | "shield" | "sparkle" | "bars" | "bolt" | "arrow" | "check";
  /** Tile side in px. Default 116. */
  size?: number;
  /** Rotation in degrees. Default -8. */
  tilt?: number;
  /** Robot antenna. Default true for the "eyes" glyph. */
  antenna?: boolean;
  /** Slow 12px bob. Default false. */
  float?: boolean;
  /** Accessible name; without one the tile is decorative. */
  label?: string;
  className?: string;
  style?: React.CSSProperties;
}
export declare function IconTile(props: IconTileProps): React.ReactElement;
