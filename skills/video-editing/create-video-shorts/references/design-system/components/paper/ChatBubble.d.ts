import type * as React from "react";

export interface ChatBubbleProps {
  /** "agent" (left, paper-2) or "you" (right, the slide accent's wash). Default "agent". */
  from?: "agent" | "you";
  /** Small mono sender line above the bubble, e.g. "Iggy · your dot". */
  name?: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function ChatBubble(props: ChatBubbleProps): React.ReactElement;
