from ai.model.others import Tool
from ai.services.tool_service.save_notes import save_notes
from ai.services.tool_service.save_to_db import save_to_db
from ai.services.tool_service.save_to_s3 import save_to_s3


class ToolService:

    def get_tool_func(self, name: Tool):
        if name == Tool.SaveToNotes:
            return save_notes
        if name == Tool.SaveToDB:
            return save_to_db
        if name == Tool.SaveToS3:
            return save_to_s3
