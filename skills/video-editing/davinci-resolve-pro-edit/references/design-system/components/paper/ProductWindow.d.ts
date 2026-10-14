import type * as React from "react";

export interface ProductWindowProps {
  tabs?: string[];
  /** Index or name of the active tab. Default 0. */
  active?: number | string;
  /** Small mono badge at the right of the tab bar: a model, version or environment. */
  badge?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function ProductWindow(props: ProductWindowProps): React.ReactElement;
