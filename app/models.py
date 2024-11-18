from pydantic import BaseModel


class Message(BaseModel):
    content: str
    room_id: str
    sender_id: str


class User(BaseModel):
    id: str  # Уникальный идентификатор пользователя
