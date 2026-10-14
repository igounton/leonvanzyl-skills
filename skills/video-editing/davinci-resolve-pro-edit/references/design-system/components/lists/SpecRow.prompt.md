SpecRow is one row of a list inside a GlassPanel; consecutive rows get hairline dividers automatically.

```jsx
<GlassPanel style={{ width: 680 }}>
  <SpecRow label="Model" value="GPT-6 Astra" />
  <SpecRow label="Uptime" value="24/7, several projects at once" highlight />
  <SpecRow label="Your laptop" value="Opt-in, off by default" />
</GlassPanel>
```

Three layouts:
- `inline` (default): mono key on the left (200px), value on the right. For specs and facts.
- `stacked`: small grey line on top, big value below. For "question → answer" lists: "Chatting with your dot" / "Doesn't count toward limits".
- `feature`: big heading on top, one grey line of description below. For capability lists: "Its own browser" / "Signs in with saved passwords".

At most seven rows. Highlight one row at most. Keep values to one or two lines; if they wrap more, the panel is too narrow or the copy too long.
