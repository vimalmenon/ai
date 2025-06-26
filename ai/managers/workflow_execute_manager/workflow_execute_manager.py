from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.model import ExecuteWorkflowModel


class WorkflowExecuteManager:
    table = "AI#EXECUTE"

    def add_workflow(self, id: str, data: ExecuteWorkflowModel):
        """This will save executed workflow"""
        DbManager().add_item(
            {"table": self.table, "app_id": f"{id}#{data.id}", **data.to_dict()}
        )

    def update_workflow(self, id: str, data: ExecuteWorkflowModel):
        """This will update the executed workflow"""
        pass

    def get_workflow(self, id: str):
        """This will get the executed workflow"""
        result = DbManager().query_items(
            Key("table").eq(self.table) & Key("app_id").begins_with(f"{id}#")
        )
        return result

    def get_workflow_by_id(self, wf_id: str, id: str):
        """This will get the executed workflow by ID"""
        item = DbManager().get_item({"table": self.table, "app_id": f"{wf_id}#{id}"})
        if item:
            return ExecuteWorkflowModel.to_cls(item)
        return None

    def delete_workflow(self, wf_id: str, id: str):
        """This will delete the executed workflow"""
        DbManager().remove_item(
            {
                "table": self.table,
                "app_id": f"{wf_id}#{id}",
            }
        )
