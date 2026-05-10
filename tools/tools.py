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

############# LIST OF CHANNELS ################
channels = [
    "EasyRussianVideos",
    "1420channel",
]


def get_random_channel() -> str:
    """Selects a random channel to get videos and transcripts from"""
    return random.choice(channels)


def get_random_video_url() -> str:
    response = youtube.search().list(
        part="snippet",
        channelId=get_channel_id(get_random_channel()),
        maxResults=50,
        type="video"
    ).execute()
    items = response["items"]
    video_id = random.choice(items)["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"


def get_channel_id(handle: str) -> str:
    response = youtube.channels().list(
        part="id",
        forHandle=handle
    ).execute()
    return response["items"][0]["id"] 
