from typing import Optional, Literal
from enum import Enum

class Message:
    role: str
    content: str

class ChatConfig:
    model: Optional[str]
    stream: Optional[bool]

class ChatGPTVersion(Enum):
    GPT_35_turbo = 'gpt-35-turbo'
    GPT_4 = 'gpt-4'
    GPT_4_32K = 'gpt-4-32k'

Role = Literal['assistant', 'user']