from typing import List, Dict
from openai import AsyncOpenAI
import os

class SystemRolePrompt:
    def __init__(self, template: str):
        self.template = template

    def create_message(self) -> Dict[str, str]:
        return {
            "role": "system",
            "content": self.template
        }

class UserRolePrompt:
    def __init__(self, template: str):
        self.template = template

    def create_message(self, **kwargs) -> Dict[str, str]:
        return {
            "role": "user",
            "content": self.template.format(**kwargs)
        }

class ChatOpenAI:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def acomplete(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content 