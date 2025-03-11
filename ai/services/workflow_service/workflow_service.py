class WorkflowService:

    def get_workflows(self):
        return [
            {
                "id": "9454830b-6daf-47f7-8fca-13d966660cf1",
                "name": "TopicWorkflow",
                "detail": "This workflow generate topic for blogs",
                "agents": [
                    {
                        "name": "topic_writer",
                        "type": "agent",
                        "prompt": (
                            "You have to come up with 10 titles for the blogs based on topic."
                            "Give the output as a list."
                            "Topic should be innovative and interesting"
                        ),
                    }
                ],
                "connections": {"START": ["topic_writer"], "topic_writer": ["END"]},
            },
            {
                "id": "18aad31b-ef41-4853-a97a-17fd8647574c",
                "name": "BlogWorkflow",
                "detail": "This workflow help to create blogs",
                "agents": [
                    {"name": "blog_writer", "type": "agent"},
                    {"name": "blog_critique", "type": "agent"},
                    {"name": "supervisor", "type": "supervisor"},
                ],
                "connections": {
                    "START": ["supervisor"],
                    "supervisor": ["blog_writer", "blog_critique", "END"],
                    "blog_writer": ["supervisor"],
                    "blog_critique": ["supervisor"],
                },
            },
        ]

    def add_workflow(self):
        return []
