StepList is a numbered sequence: an accent mono number ("01") and one line of instruction per step.

```jsx
<GlassPanel style={{ width: 680 }}>
  <StepList steps={["Create it in the desktop app", "Name it", "Connect only the apps it needs", "Set Custom Rules before real work"]} />
</GlassPanel>
```

Only for real sequences where order matters; otherwise use SpecRow. Five steps at most, each one line, starting with a verb.
