from typing import List
from pydantic import BaseModel
from core.models import OpenAIBaseResponse, TranslationResponse


class Context(OpenAIBaseResponse):
    title: str
    description: str


class ContextsModel(OpenAIBaseResponse):
    contexts: List[Context]


class DialogueSchema(OpenAIBaseResponse):
    dialogue: List[TranslationResponse]
