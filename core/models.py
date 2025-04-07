from pydantic import BaseModel


class User(BaseModel):
    full_name: str
    original: str
    current: str
    occupation: str
    target_language: str
    current_level: str
    target_level: str
