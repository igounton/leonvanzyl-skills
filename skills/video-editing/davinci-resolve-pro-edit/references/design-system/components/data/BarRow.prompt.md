BarRow is one row of a horizontal bar chart: a mono label, the bar and the value.

```jsx
<BarRow label="jev" value="$21" fraction={0.003} highlight />
<BarRow label="sonnet 5" value="$1,500" fraction={0.2} />
```

`highlight` goes on exactly one row, the one the slide is about. Stack rows in a GlassPanel with a 30–34px gap, under a two-sided MonoLabel header. Highlighted row first, then ascending; every value has its unit.
