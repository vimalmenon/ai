class ToolService:

    def get_tools(self):
        return [
            {"name": "Save Notes", "tool": "save_to_notes"},
            {"name": "Upload To S3 Bucket", "tool": "save_to_s3"},
        ]
