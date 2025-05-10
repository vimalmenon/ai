from ai.services.tool_service.save_notes import save_notes
from ai.services.tool_service.save_to_db import save_to_db
from ai.services.tool_service.save_to_s3 import save_to_s3


class ToolService:

    def get_tools(self):
        return [
            {
                "id": "91fc80be-b91c-40c7-baa4-8f7508290cb9",
                "name": "Save Notes",
                "tool_name": "save_to_notes",
            },
            {
                "id": "6afa1343-2dd7-4ead-a96d-642731f6d86f",
                "name": "Upload To S3 Bucket",
                "tool_name": "save_to_s3",
            },
            {
                "id": "6d73d308-733a-453d-90fb-707a6c215760",
                "name": "Save to DB",
                "tool_name": "save_to_db",
            },
        ]

    def get_tool_func(self, name):
        if name == "save_to_notes":
            return save_notes
        if name == "save_to_db":
            return save_to_db
        if name == "save_to_s3":
            return save_to_s3
