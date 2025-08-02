from ai.tests.factory.modal.workflow import FactoryWorkflowModel


def test_workflow_model_factory():
    workflow = FactoryWorkflowModel()
    assert workflow.id is not None
