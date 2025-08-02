from factory import Factory, Faker

# from factory import FactoryList
from ai.model import WorkflowModel


class FactoryWorkflowModel(Factory):
    class Meta:
        model = WorkflowModel

    id = Faker("uuid4")
    name = Faker("name")
    detail = Faker("text")
    nodes: dict = {}
