Stat is a big figure with tabular numerals and its mono label underneath. It shrinks to fit its column, so long figures like "4,000+" never run under the next panel.

```jsx
<Stat value="70–500 ms" label="End-to-end latency · vendor figures" tone="accent" />
<Stat value="4,000+" label="Connected apps" size={220} />
```

Use it for every big figure, including the one on a big-stat slide (`size={220}`), rather than a hand-sized `<div>`. The value always carries its unit. The label says what was measured and, if you didn't measure it, where it came from. `tone="accent"` for the winner (one per slide), `secondary` for the other side. On a big-stat slide, 220px fits four characters in the 560px column; longer figures shrink automatically.
