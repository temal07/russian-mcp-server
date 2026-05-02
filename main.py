from mcp.server.fastmcp import FastMCP
import os
from deep_translator import GoogleTranslator
from tools.tools import get_channel_id, get_video_id
from youtube_transcript_api import YouTubeTranscriptApi
import json

app = FastMCP("russian-mcp-server")

RU_MCP_API_KEY = os.getenv("RU_MCP_API_KEY")
transcript_api = YouTubeTranscriptApi()


@app.tool()
def translate(text: str, language: str = "russian") -> str:
    """Translate text to the given language"""
    return GoogleTranslator(source="auto", target=language).translate(text)


@app.tool()
def get_word_of_the_day() -> str:
    """Get the word of the day"""
    return get_channel_id("EasyRussianVideos")
    

@app.tool()
def get_video_transcript(url) -> str:
    """Get the video transcript of a video by video ID"""

    channelID = get_channel_id("EasyRussianVideos")
    video_id = get_video_id(url)

    transcript = transcript_api.fetch(video_id=video_id, languages=["ru", "en"], preserve_formatting=False)
    return json.dumps([{"text": s.text, "start": s.start, "duration": s.duration} for s in transcript])

app.run()