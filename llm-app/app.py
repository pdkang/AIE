import os
from openai import AsyncOpenAI
import chainlit as cl
from chainlit.prompt import Prompt, PromptMessage
from chainlit.playground.providers import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Template for LLM system vibe checking
user_template = """You are an assistant helping to perform quick evaluations of LLM-powered systems. Your role is to:
1. Help identify potential critical failure points in the system
2. Assess basic functionality and obvious issues
3. Look for significant problems that would be immediately noticeable
4. Provide a cursory but meaningful evaluation
5. Focus on crucial functions where failure would be severe

Frame your assessment in these sections:
- Basic Functionality Check
- Critical Issues Assessment
- Obvious Failure Points
- Quick Recommendations

System or component to evaluate: {input}

Key areas to examine:
- Core functionality problems
- Obvious response issues
- Critical safety concerns
- Basic performance problems
- User-facing issues

Provide an informal but insightful evaluation focusing on major concerns.
"""

@cl.on_chat_start
async def start_chat():
    # Welcome message with LLM system vibe check introduction
    await cl.Message(
        content="👋 Welcome to the LLM System Vibe Check Assistant! I'll help you perform quick evaluations "
        "of LLM-powered systems. Share any component or behavior you want to evaluate, such as:\n\n"
        "1. Response quality or consistency\n"
        "2. Safety mechanism effectiveness\n"
        "3. Basic functionality issues\n"
        "4. User interaction problems\n"
        "5. Critical system behaviors\n\n"
        "Remember: This is meant to be a cursory check for obvious issues, not a comprehensive evaluation."
    ).send()

    settings = {
        "model": "o1-mini",
    }

    cl.user_session.set("settings", settings)

@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")
    client = AsyncOpenAI()

    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=message.content),
            ),
        ],
        inputs={"input": message.content},
        settings=settings,
    )

    msg = cl.Message(content="")

    async for stream_resp in await client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages], 
        stream=True, 
        **settings
    ):
        token = stream_resp.choices[0].delta.content
        if token is not None:
            await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    await msg.send()
