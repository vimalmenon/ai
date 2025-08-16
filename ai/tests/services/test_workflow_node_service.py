import pytest

from ai.exceptions.exceptions import ClientError
from ai.services import WorkflowNodeService
from ai.tests.factory.workflow import FactoryCreateNodeRequest


def test_workflow_node_service_create_workflow_node_with_exception(
    dynamodb_mock,
) -> None:
    with pytest.raises(ClientError):
        WorkflowNodeService().create_workflow_node(
            "non_existent_workflow_id", FactoryCreateNodeRequest.build()
        )
