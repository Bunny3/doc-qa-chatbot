# main.py  (in project root)
from src.config import config
from src.llm import LLMClient
from src.chat import ConversationManager

def main():
    config.validate()

    llm = LLMClient()
    conversation = ConversationManager()

    print("\n🤖 Doc QA Chatbot — Milestone 1")
    print("Commands: 'quit' to exit | 'clear' to reset | 'usage' to see tokens\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            conversation.clear()
            continue

        conversation.add_user_message(user_input)

        if user_input.lower() == "usage":
            # Show token usage for the last message
            reply, usage = llm.chat_with_usage(conversation.get_messages())
            print(f"\n📊 Tokens — input: {usage['input_tokens']} | "
                  f"output: {usage['output_tokens']} | "
                  f"total: {usage['total_tokens']}\n")
            conversation.messages.pop()  # Remove the 'usage' command from history
            continue
        else:
            reply = llm.chat(conversation.get_messages())
            conversation.add_assistant_message(reply)
            print(f"\nAssistant: {reply}\n")

        # Auto-trim if history gets long (sliding window)
        if conversation.get_history_length() > 20:
            conversation.trim_to_last_n_turns(10)
            print("⚡ [Memory trimmed to last 10 turns]\n")

if __name__ == "__main__":
    main()