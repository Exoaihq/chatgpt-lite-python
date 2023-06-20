from typing import List, Optional, Callable
from enum import Enum

class ChatRole(Enum):
    USER = "user"
    AI = "ai"

class ChatMessage:
    pass

class Persona:
    def __init__(self, role: ChatRole, avatar: Optional[str] = None, name: Optional[str] = None, prompt: Optional[str] = None):
        self.role = role
        self.avatar = avatar
        self.name = name
        self.prompt = prompt

class Chat:
    def __init__(self, id: str, persona: Optional[Persona] = None, messages: Optional[List[ChatMessage]] = None):
        self.id = id
        self.persona = persona
        self.messages = messages

class ChatSidebarProps:
    def __init__(self, isActive: Optional[bool] = None, chatList: Optional[List[Chat]] = None, currentChatId: Optional[str] = None, onChangeChat: Optional[Callable[[Chat], None]] = None, onCloseChat: Optional[Callable[[Chat], None]] = None, onNewChat: Optional[Callable[[Persona], None]] = None, onSettings: Optional[Callable[[], None]] = None):
        self.isActive = isActive
        self.chatList = chatList
        self.currentChatId = currentChatId
        self.onChangeChat = onChangeChat
        self.onCloseChat = onCloseChat
        self.onNewChat = onNewChat
        self.onSettings = onSettings