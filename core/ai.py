from openai import OpenAI
from config import settings
from core.models import TranslationResponse
from utils.helpers import openai_structure_builder


class GPT:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_structured(self, input_text: str, instructions: str = None, text: dict = None, **kwargs):
        """
        Method generates structured JSON format response from OpenAI API.
        :param input_text: User input text.
        :param instructions: System/Developer instructions
        :param text: Response type structure from Pydantic model.
        :param kwargs: Additional possible keyword arguments.
        :return: JSON(Response)
        """

        return self.client.responses.create(
            model=self.model,
            input=input_text,
            instructions=instructions,
            text=text,
            **kwargs
        ).output_text

