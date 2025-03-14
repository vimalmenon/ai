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
