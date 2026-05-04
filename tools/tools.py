from datetime import date
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
from urllib.parse import urlparse, parse_qs
import random

# Build youtube
load_dotenv()

russian_mcp_key = os.getenv("RU_MCP_API_KEY")
youtube = build("youtube", "v3", developerKey=russian_mcp_key)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_channel_id(handle: str) -> str:
    """Get the channel ID of a YouTube channel"""
    response = youtube.channels().list(
        part="id",
        forHandle=handle
    ).execute()

    channelID = response["items"][0]["id"]

    return channelID


def get_random_video_id(channel_id: str) -> str:
    """Get the ID of a video"""
    response = youtube.search().list(
        part="id",
        channel_id=channel_id,
        order="date",
        maxResults=25,
        type="video"
    ).execute()
    
    items = response["items"]

    return random.choice(items)["id"]["videoId"]


