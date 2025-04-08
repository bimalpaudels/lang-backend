from core.llm import Llama, Gemini
from utils.helpers import build_user_context, get_single_result
from core.models import BaseResponse, DetailedMeaningResponse
import edge_tts


def generate_about_me(user):
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
    return BaseResponse(data=output, message="Yay").model_dump()


async def text_to_speech(text):
    communicate = edge_tts.Communicate(text=text, voice="de-DE-KatjaNeural")
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


def detailed_meaning(context):
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
    return BaseResponse(data=response, message="Yay").model_dump()


def about_me(user):
    """
    Getting user context based on Google's Models
    :return:
    """
    print("Generating about me...")
    llm = Gemini()
    prompt = """
                Write a 60 words simple 'About Me' in and translate it to German in JSON format.
                Use this JSON schema:
                Return({"original":str, "translated":str})
            """
    user_context = build_user_context(user.model_dump())
    response = llm.generate_translation_pair(user_context, prompt)
    return response

