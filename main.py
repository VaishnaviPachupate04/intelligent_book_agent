from engine import run_agent

print("Book Agent Started. Type 'exit' to stop.\n")

conversation_history = []

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    assistant_message = run_agent(user_input, conversation_history)

    print("\nAssistant:")
    print(assistant_message["content"])
    print("\n" + "-"*50)

    conversation_history.append(assistant_message)