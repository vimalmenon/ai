from factory import Factory, Faker

from ai.model import AiMessage
from ai.model.enums import AIMessageType


class FactoryAiMessage(Factory):
    class Meta:
        model = AiMessage

    id = Faker("uuid4")
    content = Faker("text")
    type = Faker(
        "random_element",
        elements=[
            AIMessageType.AI,
            AIMessageType.Human,
            AIMessageType.System,
            AIMessageType.Tool,
        ],
    )
    total_token = Faker("random_int", min=0, max=1000)
    model_name = Faker("word")
