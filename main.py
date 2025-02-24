from ai.workflows import ChatBotBuilder, WebsiteContentBuilder


def run():
    print(
        """
        1) Chat Bot
        2) Website Content builder
    """
    )
    try:
        user_input = int(input("You : "))
    except Exception:
        user_input = 0

    if user_input == 0:
        print("Invalid Input")
    if user_input == 1:
        ChatBotBuilder().invoke()
    if user_input == 2:
        WebsiteContentBuilder().invoke()
