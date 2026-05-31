from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route("/transcript", methods=["POST"])
def get_transcript():
    data = request.get_json()

    url = data.get("url")
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({
            "success": False,
            "error": "Invalid YouTube URL"
        })

    try:
        ytt_api = YouTubeTranscriptApi()

        transcript_list = ytt_api.list(video_id)

        transcript = transcript_list.find_transcript(
            ["hi", "en"]
        )

        fetched = transcript.fetch()

        text = " ".join([item.text for item in fetched])

        return jsonify({
            "success": True,
            "transcript": text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
