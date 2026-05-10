from mcp.server.fastmcp import FastMCP
import os
from deep_translator import GoogleTranslator
from tools.tools import get_channel_id, get_random_video_url
from youtube_transcript_api import TranscriptList, YouTubeTranscriptApi
import json
import random

app = FastMCP("russian-mcp-server")

RU_MCP_API_KEY = os.getenv("RU_MCP_API_KEY")
transcript_api = YouTubeTranscriptApi()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.tool()
def translate(text: str, language: str = "russian") -> str:
    """Translate text to the given language"""
    return GoogleTranslator(source="auto", target=language).translate(text)


@app.tool()
def get_word_of_the_day(level : str = "A1") -> str:
    """Generates a word of the day and use cases"""
    with open(os.path.join(BASE_DIR, "WOTD.md"), "r", encoding="utf-8") as f:
        instructions = f.read().replace("{level}", level)
        
    return instructions


@app.tool()
def drill_convo(level: str = "A1") -> str:
    """Engages in a conversation for the given level"""
    with open(os.path.join(BASE_DIR, "DRILL.md"), "r", encoding="utf-8") as f:
        instructions = f.read().replace("{level}", level)

    return instructions


@app.tool()
def video_to_watch():
    return get_random_video_url()


@app.tool()
def get_video_transcript() -> str:
    """Get the video transcript of a video by video ID"""
    url = get_random_video_url()

    # Gets the ID of the video by splitting www.youtube.com/watch?v={videoID} to the value 
    # after v=
    video_id = url.split("v=")[-1]

    transcript = transcript_api.fetch(video_id=video_id, languages=["ru", "en"], preserve_formatting=False)

    return "\n".join([snippet.text for snippet in transcript])


app.run()