---
name: daily-russian
description: Deliver the full Russian daily digest — word of the day, video, transcript, translation, and conversation drill — using the russian-mcp-server tools. Trigger when the user asks for "daily Russian", "today's lesson", "Russian digest", or invokes `/daily-russian`. Accept an optional CEFR level argument (A1–C2); default to A1. Skip for unrelated requests (general translation, single-tool calls).
---

# Daily Russian Digest

Orchestrates the russian-mcp-server tools into one coherent lesson. The MCP tools return raw prompt text (from `WOTD.md` / `DRILL.md`) — you are responsible for *following* those instructions and producing the content.

## Inputs

- `level` (optional): CEFR level `A1`, `A2`, `B1`, `B2`, `C1`, or `C2`. Default `A1`.
- If the user said something like "intermediate", map it: A1=beginner, A2=elementary, B1=intermediate, B2=upper-intermediate, C1=advanced, C2=mastery.

## Steps

1. **Word of the day** — call `get_word_of_the_day(level=<level>)`. The tool returns the WOTD.md instruction template. Follow it literally: pick a word appropriate for the level (noun, verb, *or* adjective — vary it across sessions), then produce the full breakdown the template demands (cases for nouns, conjugations for verbs, gender forms for adjectives, plus example sentences with English translations).

2. **Video recommendation** — call `video_to_watch()` and keep the returned URL. Present it with a one-line "why this is worth watching at your level" framing.

3. **Transcript** — call `get_video_transcript(url=<url from step 2>)` so the transcript matches the recommended video. The transcript is Russian (with English fallback). Show a short excerpt (~10–20 lines) rather than the full dump unless the user asks for it.

4. **Translation** — call `translate(text=<the excerpt from step 3>, language="english")`. Present the Russian and English side by side so the user can compare.

5. **Conversation drill** — call `drill_convo(level=<level>)`. The tool returns the DRILL.md instructions. Follow them: open with a greeting, start the conversation in Russian at the right level, correct mistakes inline, and ensure the user learns at least one new word/phrase/slang from the exchange.

## Output structure

Use clear section headings so the user can skim:

```
## Word of the Day (<level>)
…

## Video
<url> — <why>

## Transcript excerpt
<russian>

## Translation
<english>

## Let's chat
<open the drill conversation>
```

## Notes

- Don't pre-translate the drill conversation opener — the user is supposed to read it in Russian first.
- If any tool call fails (network, API quota), report which step broke and continue with the remaining steps where possible.
- Keep the WHOLE digest in one response unless the user asks to break it up.
