It's not possible to directly convert this React JavaScript code to Python, as React is a JavaScript library specifically designed for building user interfaces, and Python is a general-purpose programming language. However, I can provide you with a Python equivalent for the core logic of the code.

```python
import asyncio
import aiohttp
import json
from typing import List, Dict, Optional, Any, Callable

class ChatRole:
    User = "user"
    Assistant = "assistant"

class ChatMessage:
    def __init__(self, content: str, role: str):
        self.content = content
        self.role = role

class ChatConfig:
    def __init__(self, stream: bool = False):
        self.stream = stream

class ChatGPTProps:
    def __init__(
        self,
        prompts: Optional[List[ChatMessage]] = None,
        config: Optional[ChatConfig] = None,
        fetch_path: str = "",
        on_messages: Optional[Callable[[List[ChatMessage]], None]] = None,
        on_settings: Optional[Callable[[], None]] = None,
        on_change_version: Optional[Callable[[], None]] = None,
    ):
        self.prompts = prompts or []
        self.config = config or ChatConfig()
        self.fetch_path = fetch_path
        self.on_messages = on_messages
        self.on_settings = on_settings
        self.on_change_version = on_change_version

async def request_message(
    url: str,
    messages: List[ChatMessage],
    prompts: List[ChatMessage],
    config: ChatConfig,
) -> Any:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json={
                "messages": [message.__dict__ for message in messages],
                "prompts": [prompt.__dict__ for prompt in prompts],
                "config": config.__dict__,
            },
        ) as response:
            if config.stream:
                return await response.content.read()
            else:
                return await response.json()

async def fetch_message(
    fetch_path: str,
    messages: List[ChatMessage],
    prompts: List[ChatMessage],
    config: ChatConfig,
    on_messages: Optional[Callable[[List[ChatMessage]], None]] = None,
) -> None:
    try:
        data = await request_message(fetch_path, messages, prompts, config)
        if config.stream:
            # Handle streaming data here
            pass
        else:
            new_message = ChatMessage(content=data["message"], role=ChatRole.Assistant)
            messages.append(new_message)
            if on_messages:
                on_messages(messages)
    except Exception as e:
        print(f"Error: {e}")

# Example usage
async def main():
    chat_gpt_props = ChatGPTProps(fetch_path="https://example.com/api/chat")
    user_message = ChatMessage(content="Hello, how are you?", role=ChatRole.User)
    chat_gpt_props.prompts.append(user_message)

    await fetch_message(
        chat_gpt_props.fetch_path,
        chat_gpt_props.prompts,
        [],
        chat_gpt_props.config,
        on_messages=lambda messages: print(f"New messages: {messages}"),
    )

asyncio.run(main())
```

This Python code provides a basic structure for the core logic of the original React code. It includes the classes `ChatRole`, `ChatMessage`, `ChatConfig`, and `ChatGPTProps`, as well as the asynchronous functions `request_message` and `fetch_message`. Note that this code does not include any user interface components or event handling, as those are specific to React and JavaScript.