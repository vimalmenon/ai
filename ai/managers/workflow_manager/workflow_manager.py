from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import WorkflowModel, WorkflowSlimModel
from ai.utilities import generate_uuid


class WorkflowManager:
    table = "AI#WORKFLOWS"

    def get_workflows(self) -> list[WorkflowModel]:
        """This List out all workflows details"""
        items = DbManager().query_items(Key("table").eq(self.table))
        if not items:
            return []
        return [WorkflowModel.from_dict(item) for item in items]

    def get_workflow_by_id(self, id: str) -> WorkflowModel | None:
        """Get the workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": id})
        if item:
            return WorkflowModel.from_dict(item)
        return None

    def create_workflow(self, data: WorkflowSlimModel):
        """Create workflow"""
        uuid = generate_uuid()
        item = WorkflowModel(id=uuid, name=data.name)
        DbManager().add_item({"table": self.table, "app_id": uuid, **item.to_dict()})
        return item.to_dict()

    def update_workflow(self, id, data: WorkflowModel):
        """Update workflow"""
        pass

    def delete_workflows_by_id(self, id: str):
        """Delete the workflow by ID"""
        pass
