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
        return DbManager().query_items(Key("table").eq(self.table))

    def delete_workflow(self, wf_id: str, id: str):
        """This will delete the executed workflow"""
        DbManager().remove_item(
            {
                "table": self.table,
                "app_id": f"{wf_id}#{id}",
            }
        )
