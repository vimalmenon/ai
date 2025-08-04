from ai.services import AiMessageService


def test_ai_message_service_get_messages_empty(dynamodb_mock) -> None:
    result = AiMessageService().get_messages("test_id")
    assert len(result) == 0
