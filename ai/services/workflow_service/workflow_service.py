from fastapi import HTTPException

from ai.managers import DbManager, WorkflowManager
from ai.model import WorkflowModel
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
        """Create workflow"""
        try:
            return WorkflowManager().create_workflow(data)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating workflow: {str(exc)}",
            ) from None

    def update_workflow(self, id, data):
        """Update workflow"""
        try:
            return WorkflowManager().update_workflow(id, data)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating workflow: {str(exc)}",
            ) from None

    def delete_workflows_by_id(self, id):
        """Delete the workflow by ID"""
        try:
            return WorkflowManager().delete_workflows_by_id(id)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting workflow by ID: {str(exc)}",
            ) from None

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
