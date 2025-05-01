from ai.services.workflow_service.workflow_service import WorkflowService


class ExecuteWorkflowService:
    def __init__(self, id: str):
        self.id = id

    def execute(self):
        item = WorkflowService().get_workflow_by_id(self.id)
        if item:
            nodes = item.get("nodes", {})
            [self.__execute_node(node) for id, node in nodes.items()]
        return {"item": None}

    def __execute_node(self, node):
        print(node)
