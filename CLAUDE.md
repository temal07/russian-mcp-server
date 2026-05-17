# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Russian language learning MCP (Model Context Protocol) server built with FastMCP. It connects to LLMs (Claude, GPT, Folk, etc.) to deliver a daily Russian language digest: word of the day with full grammatical breakdown, a YouTube video recommendation, video transcript, translation, and conversation drill. All lesson content and behavior is driven by the `.md` prompt files rather than hardcoded logic.

## Environment Setup

Requires Python 3.11. Uses `uv` for dependency management.

```powershell
uv sync           # install dependencies into .venv
```

Two environment variables are required in `.env`:
- `RU_MCP_API_KEY` — YouTube Data API v3 key (used in both `main.py` and `tools/tools.py`)
- `YOUTUBE_API_KEY` — also loaded but currently unused; `RU_MCP_API_KEY` is the active key

## Running the Server

```powershell
uv run main.py
# or with hot-reload via mcpmon:
uv run mcpmon main.py
```

## Architecture

```
main.py          — FastMCP app entry point; all tool definitions live here
tools/tools.py   — YouTube API helpers (channel lookup, random video URL)
WOTD.md          — Prompt template for get_word_of_the_day; {level} is substituted at runtime
DRILL.md         — Prompt template for drill_convo; {level} is substituted at runtime
```

**Tool → helper flow:** `main.py` tools call `tools/tools.py` for YouTube interactions. The YouTube client (`googleapiclient`) is initialized at module import time in `tools/tools.py`, so the `.env` file must be present before import.

**Prompt-as-instruction pattern:** `get_word_of_the_day` and `drill_convo` don't generate content themselves — they read `WOTD.md` / `DRILL.md`, substitute `{level}`, and return the raw instruction text to the LLM client, which then follows those instructions. Editing those `.md` files changes the LLM's behavior without touching Python code.

**Channel list:** The curated YouTube channels are a plain list in `tools/tools.py:20`. Add new channel handles there to expand the video pool.

## MCP Tool Reference

| Tool | Description |
|------|-------------|
| `translate(text, language)` | Translate text via Google Translate (default: Russian) |
| `get_word_of_the_day(level)` | Returns WOTD.md instructions with level substituted (default: A1) |
| `drill_convo(level)` | Returns DRILL.md instructions with level substituted (default: A1) |
| `video_to_watch()` | Returns a random YouTube URL from a curated channel list |
| `get_video_transcript()` | Fetches Russian/English transcript from a random video |
