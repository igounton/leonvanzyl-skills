ProductWindow is a white app window floating on the stage, with a tab bar and a mono badge, for real product output.

```jsx
<ProductWindow tabs={["Request", "Answers", "Usage"]} active="Answers" badge="jev-latest" style={{ width: 680 }}>
  …rows…
</ProductWindow>
```

Build rows as a grid (`92px 148px minmax(0, 1fr)`, 20px gap, `--paper-line` dividers): a Pill, a mono key, the value. For chats use `ChatBubble`. For a list with a status per row (rules, checks, permissions), end each row with a `Pill`: `mint` for allowed or done, `ember` for ask first or warning, `neutral` for blocked. Don't use coloured text for status. Text is `--ink` and `--ink-2`; accent text uses `--slide-accent-ink`. Body text inside the window is 24–26px. The window must end inside the safe area; leave about 100px of empty body at the bottom if a TaskCard overlaps its lower-left edge. Show real output; no fake window buttons or status bars, and don't imitate another company's UI.
