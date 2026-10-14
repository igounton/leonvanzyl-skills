Stage is the slide itself: a 1920×1080 graphite stage with the animated horizon wave, and the root of every slide. Children land in the safe area (left 100, top 100, 1440×880), so the 380px webcam lane on the right stays clear.

```jsx
<Stage accent="azure">
  <div style={{ display: "flex", alignItems: "center", gap: "var(--gap-xl)", height: "100%" }}>
    <SlideTitle size="split" title="Its own computer" subtitle="Hosted by OpenAI" />
    …main visual…
  </div>
</Stage>
```

- `accent`: `azure` by default, `ember` for security, warnings and costs. Inside the Stage, use `var(--slide-accent)` for any accent text.
- `waveLevel="low"` (default) keeps the crest below y≈800. **Text sitting directly on the stage must end above y≈780** (the top 680px of the safe area); anything lower goes on glass or paper, which blur the wave. Use `"middle"` or `"high"` only when the lower half of the slide is empty.
- `waveIntensity` 0.6 behind dense tables, 1.4 on title-only slides. Keep `wave` on.
- `showLane` tints the webcam lane while you lay out. In a deck, expose one `showLane` tweak and pass it to every Stage.
- `fullBleed` hands children the whole frame. Use it only for backgrounds; text still stays in the safe area.

One Stage per slide, never nested, and nothing but the background in the right 380px. In a deck, each `<section>` holds exactly one Stage.
