from boto3.dynamodb.conditions import Key

from ai.managers import DbManager


class WorkflowExecuteManager:
    table = "AI#EXECUTE"

    def execute_workflow(self, data):
        """This will save executed workflow"""
        DbManager().add_item({"table": self.table, "app_id": data.id, **data.to_dict()})

    def get_executed_workflow(self, id: str):
        """This will get the executed workflow"""
        return DbManager().query_items(Key("table").eq(self.table))
