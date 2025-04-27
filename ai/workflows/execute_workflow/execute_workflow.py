from ai.services import WorkflowService


class ExecuteWorkflow:
    def __init__(self, id: str):
        self.id = id

    def execute(self):
        item = WorkflowService().get_workflow_by_id(self.id)
        return {"item": item}
