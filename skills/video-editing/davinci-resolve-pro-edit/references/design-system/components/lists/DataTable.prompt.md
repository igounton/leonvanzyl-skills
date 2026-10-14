DataTable is a compact comparison or pricing table, placed inside a GlassPanel.

```jsx
<GlassPanel padding={36}>
  <DataTable
    columns={["Plan", "Price", "Dots", "Regions"]}
    highlightColumn={2}
    rows={[
      ["Pro 100", "$100/mo", "1 included", "Not in EEA, UK, CH"],
      ["Business Premium", "Per seat", "1 included", "All regions"],
      { cells: ["Free, Go, Plus", "–", "Not available", "–"], tone: "dim" }
    ]}
  />
</GlassPanel>
```

- **Six rows and five columns at most, every cell one short line.** Abbreviate ("Not in EEA, UK, CH") rather than wrap. If it doesn't fit, split the slide in two.
- Leave `waveIntensity` at 0.6 on the Stage behind a table.
- `highlightColumn` marks the subject of the comparison; `rowHeader="label"` when the first column holds row keys ("Made by", "Runs on") rather than names.
- Title with `SlideTitle` (headline), then the panel 48px below. Title, table and footnote together must fit 880px; check the panel's bottom edge stays inside the safe area.
