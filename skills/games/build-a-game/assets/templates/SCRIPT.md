# {{GAME_TITLE}}: dialogue script (v{{N}}, approved by the user on {{DATE}})

Every voiced and on-screen line in story order. The **status** column stops anyone from paying to record a line twice.

## How to read this script

| Column | Meaning |
|---|---|
| **id** | Stable id, never renamed once it has audio. `vo.<character>.<name>` spoken · `t.*` thought · `h.*` hint · `rd.*` readable · `ui.*` interface text |
| **speaker** | Who says it |
| **line** | Exactly what the subtitle shows |
| **delivery** | Direction for the voice ("tired, half-laughing"), or what the player sees for readables |
| **type** | spoken · thought · hint · phone / radio / echo (recorded dry, effect added offline) · readable · UI |
| **status** | ✅ recorded (file path, takes) · ⏳ not recorded · — not voiced |

## 1. Recording policy

1. **Never regenerate a ✅ line** unless the user explicitly asks. Don't edit its audio manifest entry either, because the tool caches by the exact request, so an edit silently re-buys it.
2. Every generation goes through `tools/gen-audio.mjs`: add the lines to the group's manifest, **dry-run** and show the estimate, then buy with `--max-credits`.
3. Record batch by batch as each part of the game is built.
4. Two takes for the main characters' lines, one for everyone else. One-word lines get two takes and context. Re-take only lines that fail review.

## 2. Cast

| Character | Voice (and alternates) | Notes |
|---|---|---|

## 3. The script

### {{Scene name}} ({{minute mark}})

| id | speaker | line | delivery | type | status |
|---|---|---|---|---|---|
| | | | | | ⏳ |
