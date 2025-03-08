class WorkflowService:

    def get_workflows(self):
        return [
            {
                "name": "BlogWorkflow",
                "detail": "This workflow help to create blogs",
                "agents": [
                    {"name": "blog_writer", "type": "agent"},
                    {"name": "blog_critique", "type": "agent"},
                    {"name": "supervisor", "type": "supervisor"},
                ],
            }
        ]

    def add_workflow(self):
        return []
