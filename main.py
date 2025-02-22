def run():
    print("Hello!! My name is Elara, How can i help you today?")
    while user_input := input("You: "):
        if user_input.lower() == "bye":
            print("Elara: Bye! Have a nice day!")
            break
        if user_input.lower() == "how are you?":
            print("Elara: I am doing great, Thanks for asking")
            continue
        if user_input.lower() == "what is your name?":
            print("Elara: My name is Elara")
            continue
        print("Elara: I am sorry, I didn't get that. Can you please repeat?")
