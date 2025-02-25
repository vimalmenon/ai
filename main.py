from ai.workflows import ChatBotBuilder, WebsiteContentBuilder


def run():
    print(
        """
        Choose a workflow:
        ___________________
        1) Chat Bot
        2) Website Content builder
    """
    )
    try:
        user_input = int(input("You : "))
    except Exception:
        user_input = 0

    if user_input == 1:
        ChatBotBuilder().invoke()
    elif user_input == 2:
        WebsiteContentBuilder().invoke()
    else:
        print("Invalid Input")
