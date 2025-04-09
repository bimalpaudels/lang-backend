import re
from typing import List, Tuple


def build_user_context(user_data: dict) -> str:
    """
    :param user_data:
    :return: User context in a format expected by model
    """
    context = f"Your name is {user_data['full_name']}. You are from {user_data['original']}. "
    context += f"Currently living in {user_data['current']} as a {user_data['occupation']}. "
    context += f"You want to learn {user_data['target_language']} to {user_data['target_level']}."
    context += f"Your current Level:{user_data['current_level']}"

    return context.strip()


def get_result(result):
    """
    Function that takes the full output from a returning generated/translated model and
    extracts just the last part
    :param result:
    :return:
    """
    output, md = result
    output = regex_splitter(output[1:][0][-1])
    target, translation = output
    return [target, translation]


def regex_splitter(text):
    """
    Function that separates string with the given regex.
    :return: list of strings
    """
    regex = r"Target:\s*(.*?)\s*Translation:\s*(.*)"
    match = re.search(regex, text, re.DOTALL)
    if match:
        return [match.group(1), match.group(2)]
    return None


def get_single_result(result):
    output, md = result
    return output[0][-1]


def openai_structure_builder(validation_model, strict=True):
    return {
        "format":
            {
                "type": "json_schema",
                "name": validation_model.__name__,
                "schema": validation_model.model_json_schema(),
                "strict": strict,
            }
    }
