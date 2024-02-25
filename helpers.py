from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
from pytube import Search
from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import openai

def generate_summary(text: str) -> str:
    """
    Generate a summary of the provided text using OpenAI API
    """
    # Initialize the OpenAI API client
    openai.api_key = "sk-..."

    # Use GPT to generate a summary
    instructions = "Please summarize the provided text"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        n=1,
        max_tokens=4096, # max accepted value (at present) is 4096
        presence_penalty=0,
        frequency_penalty=0.1,
    )

    # Return the generated summary
    return response.choices[0].message.content.strip()

def summarize_youtube_video(video_url: str) -> str:
    """
    Summarize the provided YouTube video
    """
    # Extract the video ID from the URL
    video_id = extract_youtube_video_id(video_url)

    # Fetch the video transcript
    transcript = get_video_transcript(video_id)

    # If no transcript is found, return an error message
    if not transcript:
        return f"No English transcript found " \
               f"for this video: {video_url}"

    # Generate the summary
    summary = generate_summary(transcript)

    # Return the summary
    return summary

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