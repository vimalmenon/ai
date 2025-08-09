import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import ExecuteWorkflowService, WorkflowService
from ai.tests.factory.workflow import (
    FactoryCreateExecuteWorkflowRequest,
    FactoryUpdateWorkflowRequest,
    FactoryWorkflowSlimModel,
)


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


def test_workflow_service_delete_when_execute_workflow_exists(dynamodb_mock) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    update_data = FactoryUpdateWorkflowRequest.build()
    update_data.complete = True
    WorkflowService().update_workflow(workflow.id, update_data)
    ExecuteWorkflowService().create_executed_workflow(
        workflow.id, FactoryCreateExecuteWorkflowRequest.build()
    )
    with pytest.raises(ClientError):
        WorkflowService().delete_workflows_by_id(workflow.id)


def test_workflow_service_update_workflow(dynamodb_mock) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    update_data = FactoryUpdateWorkflowRequest.build()
    WorkflowService().update_workflow(workflow.id, update_data)
    updated_workflow = WorkflowService().get_workflow_by_id(workflow.id)
    assert updated_workflow.name == update_data.name
    assert updated_workflow.detail == update_data.detail
    assert updated_workflow.complete == update_data.complete
