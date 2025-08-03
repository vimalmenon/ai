from ai.managers.ai_message_manager.ai_message_manager import AiMessageManager
from ai.model import AiMessage


class AiMessageService:

    def get_messages(self, id: str) -> list[AiMessage]:
        return AiMessageManager().get_data(id)
