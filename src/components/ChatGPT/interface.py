from typing import List, Optional, Callable, Union
from enum import Enum

class ChatRole(Enum):
    Assistant = 'assistant'
    User = 'user'
    System = 'system'

class ChatGPTVersion(Enum):
    GPT_35_turbo = 'gpt-35-turbo'
    GPT_4 = 'gpt-4'
    GPT_4_32K = 'gpt-4-32k'

class Prompt:
    def __init__(self, title: Optional[str] = None, content: Optional[str] = None):
        self.title = title
        self.content = content

class ChatGPTProps:
    def __init__(self, header: Optional[str] = None, fetchPath: str = '', config: Optional['ChatConfig'] = None, prompts: Optional[List['ChatMessage']] = None, onMessages: Optional[Callable[[List['ChatMessage']], None]] = None, onSettings: Optional[Callable[[], None]] = None, onChangeVersion: Optional[Callable[['ChatGPTVersion'], None]] = None):
        self.header = header
        self.fetchPath = fetchPath
        self.config = config
        self.prompts = prompts
        self.onMessages = onMessages
        self.onSettings = onSettings
        self.onChangeVersion = onChangeVersion

class ChatMessage:
    def __init__(self, content: str, role: ChatRole):
        self.content = content
        self.role = role

class ChatMessageItemProps:
    def __init__(self, message: ChatMessage):
        self.message = message

class SendBarProps:
    def __init__(self, loading: bool, disabled: bool, inputRef: 'RefObject', onSettings: Optional[Callable[[], None]] = None, onSend: Callable[['ChatMessage'], None], onClear: Callable[[], None], onStop: Callable[[], None]):
        self.loading = loading
        self.disabled = disabled
        self.inputRef = inputRef
        self.onSettings = onSettings
        self.onSend = onSend
        self.onClear = onClear
        self.onStop = onStop

class ShowProps:
    def __init__(self, loading: Optional[bool] = None, fallback: Optional[str] = None, children: Optional[str] = None):
        self.loading = loading
        self.fallback = fallback
        self.children = children

class ChatGPInstance:
    def __init__(self, setPrompt: Callable[['ChatMessage'], None], setChatContent: Callable[['Prompt'], None], setMessages: Callable[[List['ChatMessage']], None], getMessages: Callable[[], List['ChatMessage']], scrollDown: Callable[[], None]):
        self.setPrompt = setPrompt
        self.setChatContent = setChatContent
        self.setMessages = setMessages
        self.getMessages = getMessages
        self.scrollDown = scrollDown

class ChatConfig:
    def __init__(self, model: Optional[ChatGPTVersion] = None, stream: Optional[bool] = None):
        self.model = model
        self.stream = stream