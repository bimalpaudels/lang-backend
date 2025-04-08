from typing import Any, List

from pydantic import BaseModel
from starlette import status


class User(BaseModel):
    full_name: str
    original: str
    current: str
    occupation: str
    target_language: str
    current_level: str
    target_level: str


class BaseResponse(BaseModel):
    message: str = ""
    success: bool = True
    data: Any


class DetailedMeaning(User):
    word: str = ""


class DetailedMeaningResponse(BaseModel):
    """Structure of detailed meaning response from Gemini API"""
    word: str
    context: str
    examples: List[str]
