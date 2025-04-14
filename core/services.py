import json

from core.llm import Llama, Gemini
from core.ai import GPT
from utils.helpers import build_user_context, openai_structure_builder
from core.models import BaseResponse, DetailedMeaningResponse, TranslationResponse
import edge_tts


def llama_about_me(user):
    # First working function: Depreciated
    llm = Llama()
    prompt = """
        Generate me a 150 words Introduction paragraph, following the format:
        Target: <target_language_text>
        Translation: <English_translation>
        Ensure there are no extra sentences.
        """
    user_context = build_user_context(user.model_dump())
    output = llm.generate_translation_pair(user_context, prompt)
    return BaseResponse(data=json.loads(output), message="Yay").model_dump()


async def text_to_speech(text):
    communicate = edge_tts.Communicate(text=text, voice="de-DE-KatjaNeural")
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


def gemini_detailed_meaning(context):
    """
    Generates context description for a word. The prompt should use language detail from the user_context.
    TODO: Support for a phrase
    :param context:
    :return:
    """
    print("Fetching detailed meaning...")
    llm = Gemini()
    prompt = f"""
            Write 20 words context in English  {context['word']} 
            is used in {context['target_language']} with 2 
            different examples.
            """
    config = {
        'response_mime_type': 'application/json',
        'response_schema': DetailedMeaningResponse,
    }
    response = llm.generate_text(prompt, **config)
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()


def gemini_about_me(user):
    """
    Getting user context based on Google's Models
    :return:
    """
    print("Generating about me...")
    llm = Gemini()
    prompt = """
                Write a 60 words simple 'About Me' and translate it to German.
            """
    config = {
        'response_mime_type': 'application/json',
        'response_schema': TranslationResponse,
        'system_instruction': build_user_context(user.model_dump()),
    }
    response = llm.generate_text(prompt, **config).strip()
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()


def translate_user_introduction(user, gpt):
    """
    Generates and translates a short introduction paragraph for the given user.
    :param user: User object with their personal information.
    :param gpt: Shared gpt instance.
    :return: JSON Object with original and translated text.
    """

    instructs = "You are a translator that generates a 24 words paragraph and translates to target language."
    inp = (f"Intro for {user.model_dump()} starting with a greeting in the "
           f"target language.")

    schema = openai_structure_builder(TranslationResponse, strict=True)

    response = gpt.generate_structured(inp, instructions=instructs, text=schema)
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()


def detailed_description(context, gpt):
    """
    Receives a word (also phrase in the future) and generates a detailed description in English
    in the context of the user's target language.
    :param context: User details and the word to describe.
    :param gpt: Shared gpt instance.
    :return: Detailed description wrapped in BaseResponse.
    """
    instructs = """You define a given word in English concisely in the context of target language in 30 words. 
                    and provide 2 examples (10 words) at the end with translation in (brackets)."""
    inp = f"""Context: {context.model_dump()}"""

    schema = openai_structure_builder(DetailedMeaningResponse, strict=True)
    response = gpt.generate_structured(inp, instructions=instructs, text=schema)
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()
