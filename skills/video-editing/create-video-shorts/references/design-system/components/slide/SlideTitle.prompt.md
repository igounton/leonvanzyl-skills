SlideTitle is the title block every slide starts with: optional eyebrow, the title, one accent subtitle and an optional footnote, at fixed sizes so every slide in a deck matches.

```jsx
<SlideTitle size="display" eyebrow="DevDay 2026 · September 29" title="OpenAI dots" subtitle="Always-on agents inside ChatGPT">
  <div style={{ position: "relative", height: 150, marginBottom: 30 }}>…two IconTiles…</div>
</SlideTitle>

<SlideTitle title="Where you reach your dot" subtitle="One memory across every channel" />

<SlideTitle size="split" title="Rules, reviews and approvals" subtitle="You decide what it does alone"
  note="Auto-review checks any action that touches your accounts." style={{ width: 700 }} />
```

- `display` for the opening slide only: one to three words, vertically centred.
- `headline` (default) for slides with the content below the title, across the full 1440px.
- `split` for slides with the title on the left (700px) and a visual on the right. It takes two or three lines.
- Always use this instead of a hand-built `<h1>` and `<p>`: subtitle sizes and gaps then stay consistent.
- The `note` sits on the bare stage, so keep the whole block above y≈780 (see Stage). If the note would fall lower, drop it or move it into the visual.
