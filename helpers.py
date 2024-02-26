from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
from pytube import Search
from pytube import YouTube
from pytube import Playlist
from pytube import Channel

def extract_youtube_video_id(url: str) -> str | None:
    """
    Extract the video ID from the URL
    https://www.youtube.com/watch?v=XXX -> XXX
    https://youtu.be/XXX -> XXX
    """
    found = re.search(r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if found:
        return found.group(1)
    return None

def get_video_transcript(video_id: str) -> str | None:
    """
    Fetch the transcript of the provided YouTube video
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        # The video doesn't have a transcript
        return None

    text = " ".join([line["text"] for line in transcript])
    return text
