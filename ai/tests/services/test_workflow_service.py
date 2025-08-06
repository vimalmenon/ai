import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import WorkflowService
from ai.tests.factory.workflow import FactoryWorkflowSlimModel


def test_workflow_service_create_workflow(dynamodb_mock) -> None:
    service = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    assert service is not None


def test_workflow_service_get_workflow_by_id(dynamodb_mock) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    retrieved_workflow = WorkflowService().get_workflow_by_id(workflow.id)
    assert retrieved_workflow.id == workflow.id


def test_workflow_service_get_workflows(dynamodb_mock) -> None:
    WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    workflows = WorkflowService().get_workflows()
    assert len(workflows) == 1


def test_workflow_service_delete_workflow_by_id(dynamodb_mock) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    WorkflowService().delete_workflows_by_id(workflow.id)
    with pytest.raises(ClientError):
        WorkflowService().get_workflow_by_id(workflow.id)
