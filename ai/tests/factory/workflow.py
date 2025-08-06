from factory import Factory, Faker

# from factory import FactoryList
from ai.model import UpdateWorkflowRequest, WorkflowModel, WorkflowSlimModel


class FactoryWorkflowModel(Factory):
    class Meta:
        model = WorkflowModel

    id = Faker("uuid4")
    name = Faker("name")
    detail = Faker("text")
    nodes: dict = {}


class FactoryWorkflowSlimModel(Factory):
    class Meta:
        model = WorkflowSlimModel

    name = Faker("name")


class FactoryUpdateWorkflowRequest(Factory):
    class Meta:
        model = UpdateWorkflowRequest

    name = Faker("name")
    detail = Faker("text")
    complete = Faker("boolean")
