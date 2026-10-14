CodePanel is a frosted-glass code block with line numbers and syntax colours, optionally with the glowing accent cursor at its top-left corner.

```jsx
<CodePanel cursor style={{ width: 616 }} lines={[
  "POST /v1/systemone",
  "{",
  '  "model": "jev-latest",',
  '  "state": "Help! My payouts have',
  { text: '    been failing for 3 days."', wrap: true },
  "}"
]} />
```

Colours are automatic: strings, JSON keys, numbers and booleans, keywords and HTTP verbs, comments. A long line continues on an unnumbered row with `{ text, wrap: true }`, like a wrapped line in an editor. Keep lines to about 36 characters at 22px, wrap by hand rather than shrinking the font, and show 14 lines or fewer of real code.
