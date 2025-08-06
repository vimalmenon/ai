from factory import Factory, Faker

# from factory import FactoryList
from ai.model import UpdateWorkflowRequest, WorkflowModel, WorkflowSlimModel, WorkflowNodeRequest


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


class FactoryWorkflowNodeRequest(Factory):
    class Meta:
        model = WorkflowNodeRequest

    id = Faker("uuid4")
    wf_id = Faker("uuid4")
    name = Faker("name")
    type = Faker("word")
    request_at_run_time = Faker("boolean")
    data_from_previous_node = Faker("boolean")
    structured_output = None