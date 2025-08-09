import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import ExecuteWorkflowService, WorkflowService
from ai.tests.factory.workflow import (
    FactoryCreateExecuteWorkflowRequest,
    FactoryWorkflowSlimModel,
)


def test_execute_workflow_service_workflow_not_found(faker, dynamodb_mock):
    service = ExecuteWorkflowService()
    with pytest.raises(ClientError):
        service.create_executed_workflow(
            faker.uuid4(), FactoryCreateExecuteWorkflowRequest.build()
        )


def test_execute_workflow_service_workflow_not_complete(faker, dynamodb_mock):
    service = WorkflowService().create_workflow(FactoryWorkflowSlimModel.build())
    with pytest.raises(ClientError):
        ExecuteWorkflowService().create_executed_workflow(
            service.id, FactoryCreateExecuteWorkflowRequest.build()
        )
