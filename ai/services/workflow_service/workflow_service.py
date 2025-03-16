from boto3.dynamodb.conditions import Key

from ai.managers import DbManager
from ai.services.workflow_service.workflow_data import WorkflowDBItem
from ai.utilities import generate_uuid


class WorkflowService:

    def get_workflows(self):
        #  [
        #     {
        #         "id": "9454830b-6daf-47f7-8fca-13d966660cf1",
        #         "name": "TopicWorkflow",
        #         "detail": "This workflow generate topic for blogs",
        #         "agents": [
        #             {
        #                 "name": "topic_writer",
        #                 "type": "agent",
        #                 "prompt": (
        #                     "You have to come up with 10 titles for the blogs based on topic."
        #                     "Give the output as a list."
        #                     "Topic should be innovative and interesting"
        #                 ),
        #             }
        #         ],
        #         "connections": {"START": ["topic_writer"], "topic_writer": ["END"]},
        #     },
        #     {
        #         "id": "18aad31b-ef41-4853-a97a-17fd8647574c",
        #         "name": "BlogWorkflow",
        #         "detail": "This workflow help to create blogs",
        #         "agents": [
        #             {"name": "blog_writer", "type": "agent"},
        #             {"name": "blog_critique", "type": "agent"},
        #             {"name": "supervisor", "type": "supervisor"},
        #         ],
        #         "connections": {
        #             "START": ["supervisor"],
        #             "supervisor": ["blog_writer", "blog_critique", "END"],
        #             "blog_writer": ["supervisor"],
        #             "blog_critique": ["supervisor"],
        #         },
        #     },
        # ]
        table = "AI#WORKFLOWS"
        return DbManager().query_items(Key("table").eq(table))

    def create_workflow(self, data):
        uuid = generate_uuid()
        table = "AI#WORKFLOWS"
        item = WorkflowDBItem(
            table=table, app_id=uuid, id=uuid, name=data.name, detail=data.detail
        )
        DbManager().add_item(item.to_json())
        return item.to_json()

    def delete_workflows_by_id(self, id):
        table = "AI#WORKFLOWS"
        return DbManager().remove_item({"table": table, "app_id": id})

    def get_workflow_by_id(self, id):
        table = "AI#WORKFLOWS"
        # items = DbManager().query_items(Key("table").eq(table) & Key("app_id").eq(id))
        item = DbManager().get_item({"table": table, "app_id": id})
        if item:
            return item
        return None

    def delete_workflow_nodes(self, wf_id, id):
        item = DbManager().get_item({"table": "AI#WORKFLOWS", "app_id": wf_id})
        if item:
            nodes = item.get("nodes", {})
            del nodes[id]
            new_items = {**item, "nodes": nodes}
            DbManager().update_item(
                Key={"table": "AI#WORKFLOWS", "app_id": wf_id},
                UpdateExpression="set nodes= :nodes",
                ExpressionAttributeValues={":nodes": nodes},
            )
            return new_items

    def create_workflow_node(self, wf_id, body):
        item = DbManager().get_item({"table": "AI#WORKFLOWS", "app_id": wf_id})
        if item:
            uuid = generate_uuid()
            nodes = item.get("nodes", {})
            nodes[uuid] = {"id": uuid, "name": body.name}
            new_items = {**item, "nodes": nodes}
            DbManager().update_item(
                Key={"table": "AI#WORKFLOWS", "app_id": wf_id},
                UpdateExpression="set nodes= :nodes",
                ExpressionAttributeValues={":nodes": nodes},
            )
            return new_items

    def update_workflow_node(self, id):
        return {"id": id}
