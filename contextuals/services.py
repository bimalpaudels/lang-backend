import json
from contextuals.models import ContextsModel, DialogueSchema
from utils.helpers import openai_structure_builder
from core.models import BaseResponse


def context_generator(user, model):
    """
    A function that generates real-life context tailored to specific user.
    It takes user details and generates few scenarios for them that could occur in
    their life that they might need to learn and practice. For e.g: Not finding things in
    a supermarket
    :param user:
    :param model:
    :return:
    """
    instructs = """ Only respond with exactly 2 realistic day-to-day social scenarios for the user in 2nd person.
                    Description should be of around 10 words.
                """
    inp = f"User context: {user.model_dump()}"
    schema = openai_structure_builder(ContextsModel)

    response = model.generate_structured(inp, instructions=instructs, text=schema)
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()


def generate_contextual_dialogue(context, model):
    """
    A function that takes a context and generates potential dialogues for it.
    For example: Talking to supermarket worker to ask for help.
    :param context:
    :param model:
    :return:
    """
    instructs = """ You generate a 1-liner realistic German A1 conversation of 3 turns each in under 100 words of the given context, 
                    starting and ending with greetings. Start with user talking.
                """
    inp = f"Context: {context.model_dump()}"
    schema = openai_structure_builder(DialogueSchema)
    response = model.generate_structured(inp, instructions=instructs, text=schema)
    return BaseResponse(data=json.loads(response), message="Yay").model_dump()
