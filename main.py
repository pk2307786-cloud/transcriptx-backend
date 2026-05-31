from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

app = FastAPI()


def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None


def get_youtube_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()

        transcript_list = ytt_api.list(video_id)

        transcript = transcript_list.find_transcript(
            ['hi', 'en']
        )

        fetched_transcript = transcript.fetch()

        return " ".join([item.text for item in fetched_transcript])

    except Exception as e:
        return f"No transcript available: {str(e)}"


@app.post("/transcript")
async def get_transcript(data: dict):
    url = data.get("url")

    video_id = extract_video_id(url)

    if not video_id:
        return {"success": False, "error": "Invalid YouTube URL"}

    result = get_youtube_transcript(video_id)

    if result.startswith("No transcript available"):
        return {
            "success": False,
            "error": result
        }

    return {
        "success": True,
        "transcript": result
    }
