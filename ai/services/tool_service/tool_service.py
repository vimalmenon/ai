from collections.abc import Callable

from ai.model.others import Tool
from ai.services.tool_service.save_notes.save_notes import save_to_notes
from ai.services.tool_service.save_to_db.save_to_db import save_to_db
from ai.services.tool_service.save_to_s3.save_to_s3 import save_to_s3
from ai.services.tool_service.text_to_speech.text_to_speech import text_to_speech


class ToolService:

    def get_tool_func(self, name: Tool) -> Callable:
        if name == Tool.SaveToNotes:
            return save_to_notes
        if name == Tool.SaveToDB:
            return save_to_db
        if name == Tool.SaveToS3:
            return save_to_s3
        if name == Tool.TextToSpeech:
            return text_to_speech
