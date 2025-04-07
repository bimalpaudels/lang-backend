from core.llm import Llama
from utils.helpers import build_user_context


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
    return output

