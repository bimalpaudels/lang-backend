from typing import Any, List, Optional, Type

from pydantic import BaseModel, ConfigDict, typing
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


class DetailedMeaning(BaseModel):
    word: str = ""
    target_language: str = ""
    current_level: str = ""


class OpenAIBaseResponse(BaseModel):
    """
    Base Model For Structure Response from OpenAI.
    Models should inherit this along with their attributes before
    being passed as schemas because openAI expects extra attributes
    to be False.
    """
    model_config = ConfigDict(extra="forbid")


class DetailedMeaningResponse(OpenAIBaseResponse):
    """Structure of detailed meaning response from Gemini API"""
    word: str
    context: str
    examples: List[str]


class TranslationResponse(OpenAIBaseResponse):
    """
    Validator/Serializer response for translated texts.
    """
    original: str
    translated: str
