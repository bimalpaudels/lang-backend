from core.llm import Llama
from utils.helpers import build_user_context
from core.models import BaseResponse
import edge_tts


def about_me(user):
    llm = Llama()
    prompt = """
        Generate me a 200 words Introduction paragraph, following the format:
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
