from fastapi import HTTPException

from ai.managers import DbManager, WorkflowManager
from ai.model import WorkflowModel
from ai.services.workflow_service.workflow_data import WorkflowDBItem
from ai.utilities import generate_uuid


class WorkflowService:

    def get_workflows(self) -> list[WorkflowModel]:
        """This List out all workflows details"""
        try:
            return WorkflowManager().get_workflows()
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching workflows: {str(exc)}",
            ) from None

    def get_workflow_by_id(self, id: str) -> WorkflowModel | None:
        """Get the workflow by ID"""
        try:
            return WorkflowManager().get_workflow_by_id(id)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching workflow by ID: {str(exc)}",
            ) from None

    def create_workflow(self, data):
        uuid = generate_uuid()
        table = "AI#WORKFLOWS"
        item = WorkflowDBItem(
            table=table, app_id=uuid, id=uuid, name=data.name, detail=data.detail
        )
        DbManager().add_item(item.to_json())
        return item.to_json()

    def update_workflow(self, id, data):
        table = "AI#WORKFLOWS"
        item = DbManager().get_item({"table": table, "app_id": id})
        if item:
            (
                update_expression,
                expression_attribute_values,
                expression_attribute_names,
            ) = self._get_workflow_details(data)
            DbManager().update_item(
                Key={"table": "AI#WORKFLOWS", "app_id": id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
            )
            return item

    def delete_workflows_by_id(self, id):
        table = "AI#WORKFLOWS"
        return DbManager().remove_item({"table": table, "app_id": id})

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

    def update_workflow_node(self, wf_id, id, data):
        item = DbManager().get_item({"table": "AI#WORKFLOWS", "app_id": wf_id})
        if item:
            nodes = item.get("nodes", {})
            node = nodes.get(id, {})
            new_data = {
                **node,
                **data.to_dict(),
            }
            nodes[id] = new_data
            new_items = {**item, "nodes": nodes}
            DbManager().update_item(
                Key={"table": "AI#WORKFLOWS", "app_id": wf_id},
                UpdateExpression="set nodes= :nodes",
                ExpressionAttributeValues={":nodes": nodes},
            )
            return new_items

    def _get_workflow_details(self, data):
        expression = {}
        if data.name:
            expression["name"] = {
                "name": "#name",
                "key": ":name",
                "value": data.name,
            }
        if data.detail:
            expression["detail"] = {
                "name": "#detail",
                "key": ":detail",
                "value": data.detail,
            }
        if data.complete is not None:
            expression["complete"] = {
                "name": "#complete",
                "key": ":complete",
                "value": data.complete,
            }
        update_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}
        for key, value in expression.items():
            update_expression.append(f"{value['name']} = {value['key']}")
            expression_attribute_values[value["key"]] = value["value"]
            expression_attribute_names[value["name"]] = key

        return (
            "set " + ", ".join(update_expression),
            expression_attribute_values,
            expression_attribute_names,
        )
