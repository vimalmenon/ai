class ToolService:

    def get_tools(self):
        return [
            {
                "id": "91fc80be-b91c-40c7-baa4-8f7508290cb9",
                "name": "Save Notes",
                "tool": "save_to_notes",
            },
            {
                "id": "6afa1343-2dd7-4ead-a96d-642731f6d86f",
                "name": "Upload To S3 Bucket",
                "tool": "save_to_s3",
            },
        ]
