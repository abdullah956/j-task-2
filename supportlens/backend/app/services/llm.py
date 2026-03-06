from time import perf_counter
from groq import AsyncGroq

from app.config import settings


CHATBOT_SYSTEM_PROMPT = """You are a helpful customer support agent for BillFlow, a SaaS billing platform.
Help with billing, refunds, account access, cancellations, and general questions.
Be concise, professional, empathetic. Keep responses under 100 words."""


class GroqClient:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def chat_complete(self, system_prompt: str, user_message: str) -> tuple[str, int]:
        """
        Send a chat completion request to Groq.

        Returns:
            tuple[str, int]: (response_text, response_time_ms)
        """
        start_time = perf_counter()

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )

        end_time = perf_counter()
        response_time_ms = int((end_time - start_time) * 1000)

        response_text = response.choices[0].message.content.strip()

        return response_text, response_time_ms
