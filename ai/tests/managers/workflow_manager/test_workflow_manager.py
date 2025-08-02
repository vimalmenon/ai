from ai.managers.workflow_manager.workflow_manager import WorkflowManager
from ai.tests.factory.modal.workflow import (
    FactoryWorkflowSlimModel,
)


def test_create_and_read_workflow_by_id(dynamodb_mock, setup_environment) -> None:

    workflow = WorkflowManager().create_workflow(FactoryWorkflowSlimModel.build())
    assert workflow.id is not None
    assert WorkflowManager().get_workflow_by_id(workflow.id) == workflow


def test_get_workflows(dynamodb_mock, setup_environment) -> None:
    WorkflowManager().create_workflow(FactoryWorkflowSlimModel.build())
    workflows = WorkflowManager().get_workflows()
    assert len(workflows) == 1


def test_delete_workflow_by_id(dynamodb_mock, setup_environment) -> None:
    workflow = WorkflowManager().create_workflow(FactoryWorkflowSlimModel.build())
    WorkflowManager().delete_workflows_by_id(workflow.id)
    assert WorkflowManager().get_workflow_by_id(workflow.id) is None
