GlassPanel is frosted glass over the stage: the container for comparisons, charts and grouped figures.

```jsx
<GlassPanel highlight style={{ display: "flex", flexDirection: "column", gap: 36 }}>
  <MonoLabel tone="accent">System 1 · Jev</MonoLabel>
  …
</GlassPanel>
```

`highlight` (accent border and glow) marks the winner, on one panel per slide at most. Panels usually fill a two-column grid with a 40px gap. No glass inside glass, no paper inside glass.
