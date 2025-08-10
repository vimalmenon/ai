import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import ExecuteWorkflowService, WorkflowNodeService, WorkflowService
from ai.tests.factory.workflow import (
    FactoryCreateExecuteWorkflowRequest,
    FactoryCreateNodeRequest,
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


def test_workflow_service_delete_workflow_raises_error_when_executed_workflow_exists(
    dynamodb_mock,
) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    update_data = FactoryUpdateWorkflowRequest.build()
    update_data.complete = False
    updated_workflow = WorkflowService().update_workflow(workflow.id, update_data)
    WorkflowNodeService().create_workflow_node(
        updated_workflow.id, FactoryCreateNodeRequest.build()
    )
    update_data.complete = True
    WorkflowService().update_workflow(workflow.id, update_data)
    ExecuteWorkflowService().create_executed_workflow(
        workflow.id, FactoryCreateExecuteWorkflowRequest.build()
    )
    with pytest.raises(ClientError):
        WorkflowService().delete_workflows_by_id(workflow.id)


def test_workflow_service_update_workflow_with_no_nodes_should_fail(
    dynamodb_mock,
) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    update_data = FactoryUpdateWorkflowRequest.build()
    update_data.complete = True
    with pytest.raises(ClientError) as exc_info:
        WorkflowService().update_workflow(workflow.id, update_data)
    assert (
        str(exc_info.value.detail)
        == f"Workflow {workflow.id} cannot be marked as complete because it has no nodes"
    )


def test_workflow_service_update_workflow_marks_complete_when_nodes_exist(
    dynamodb_mock,
) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    WorkflowNodeService().create_workflow_node(
        workflow.id, FactoryCreateNodeRequest.build()
    )
    update_data = FactoryUpdateWorkflowRequest.build()
    update_data.complete = True
    workflow = WorkflowService().update_workflow(workflow.id, update_data)
    assert workflow.complete
    assert len(workflow.nodes) == 1
    assert workflow.detail == update_data.detail


def test_workflow_service_update_workflow_updates_name_detail_and_complete_status(
    dynamodb_mock,
) -> None:
    workflow = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    update_data = FactoryUpdateWorkflowRequest.build()
    update_data.complete = False
    WorkflowService().update_workflow(workflow.id, update_data)
    updated_workflow = WorkflowService().get_workflow_by_id(workflow.id)
    assert updated_workflow.name == update_data.name
    assert updated_workflow.detail == update_data.detail
    assert updated_workflow.complete == update_data.complete
