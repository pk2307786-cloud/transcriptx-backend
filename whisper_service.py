import whisper
import os

class WhisperService:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, file_path: str):
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        result = self.model.transcribe(file_path)
        return {
            "text": result["text"],
            "segments": result["segments"]
        }

whisper_service = WhisperService()
