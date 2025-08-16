import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import ExecuteWorkflowService, WorkflowNodeService, WorkflowService
from ai.tests.factory.workflow import (
    FactoryCreateExecuteWorkflowRequest,
    FactoryCreateNodeRequest,
    FactoryUpdateWorkflowRequest,
    FactoryWorkflowSlimModel,
)


def test_execute_workflow_service_raises_error_with_invalid_workflow_id(
    faker, dynamodb_mock
) -> None:
    service = ExecuteWorkflowService()
    with pytest.raises(ClientError):
        service.create_executed_workflow(faker.uuid4(), FactoryCreateExecuteWorkflowRequest.build())


def test_execute_workflow_service_raises_error_when_workflow_not_complete(
    dynamodb_mock,
) -> None:
    service = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    with pytest.raises(ClientError) as msg:
        ExecuteWorkflowService().create_executed_workflow(
            service.id, FactoryCreateExecuteWorkflowRequest.build()
        )
    assert str(msg.value.detail) == f"Workflow with ID {service.id} is not complete."


def test_execute_workflow_service_successfully_creates_executed_workflow(
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
