from factory import Factory, Faker

from ai.model import AiMessage
from ai.model.enums import AiMessageType


class FactoryAiMessage(Factory):
    class Meta:
        model = AiMessage

    id = Faker("uuid4")
    content = Faker("text")
    type = Faker(
        "random_element",
        elements=[
            AiMessageType.AI,
            AiMessageType.Human,
            AiMessageType.System,
            AiMessageType.Tool,
        ],
    )
    total_token = Faker("random_int", min=0, max=1000)
    model_name = Faker("word")
