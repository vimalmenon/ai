import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import ExecuteWorkflowService
from ai.tests.factory.workflow import FactoryCreateExecuteWorkflowRequest


def test_execute_workflow_service_workflow_not_found(faker):
    service = ExecuteWorkflowService()
    with pytest.raises(ClientError):
        service.create_executed_workflow(
            faker.uuid4(), FactoryCreateExecuteWorkflowRequest.build()
        )
