class WorkflowService:

    def get_workflows(self):
        return [
            {
                "name": "TopicWorkflow",
                "detail": "This workflow generate topic for blogs",
                "agents": [{"name": "topic_writer", "type": "agent"}],
                "connection": {"START": ["topic_writer"], "topic_writer": ["END"]},
            },
            {
                "name": "BlogWorkflow",
                "detail": "This workflow help to create blogs",
                "agents": [
                    {"name": "blog_writer", "type": "agent"},
                    {"name": "blog_critique", "type": "agent"},
                    {"name": "supervisor", "type": "supervisor"},
                ],
                "workflow": {},
            },
        ]

    def add_workflow(self):
        return []
