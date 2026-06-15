# src/llm.py
from groq import Groq
from src.config import config

class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.LLM_MODEL

    def chat(self, messages: list[dict]) -> str:
        """
        messages format (OpenAI-compatible):
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "What is RAG?"}
        ]
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )

        # Extract text from response
        return response.choices[0].message.content

    def chat_with_usage(self, messages: list[dict]) -> tuple[str, dict]:
        """Same as chat() but also returns token usage — useful for cost tracking"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )
        usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return response.choices[0].message.content, usage