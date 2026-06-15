SYSTEM_PROMPT ="""You are a helpful AI assistant.
You answer clearly and concisely. If you don't know the something, say so honestly."""

class ConversationManager:
    def __init__(self, system_prompt: str = SYSTEM_PROMPT):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]
    
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> list[dict]:
        return self.messages
    
    def get_history_length(self) -> int:
        # Exclude system prompt from history length count
        return len(self.messages)-1
    
    def clear(self):
        # Clear all messages except system prompt
        self.messages = [self.messages[0]]
        print("Conversation history cleared, system prompt retained.")
    
    def trim_to_last_n_turns(self, n: int = 10):
        """
        Keep only last N user+assistant pairs to avoid hitting context limits.
        This is a real production technique called 'sliding window memory'.
        """
        system = self.messages[0]
        # Each turn = 1 user + 1 assistant message = 2 items
        recent = self.messages[1:][-n * 2:]
        self.messages = [system] + recent