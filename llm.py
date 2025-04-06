import re
import textwrap
from gradio_client import Client
from typing import List, Tuple


class ContextHandler:
    """
    Contains method to handle all kinds of contexts from frontend.
    TODO: Think of a better name
    """
    def __init__(self):
        client_id = "openfree/Llama-4-Maverick-17B-Research"
        self.client = Client(client_id)

    def regex_splitter(self, text):
        """
        Function that separates string with the given regex.
        :return: list of strings
        """
        regex = r"Target:\s*(.*?)\s*Translation:\s*(.*)"
        match = re.search(regex, text, re.DOTALL)
        if match:
            return [match.group(1), match.group(2)]
        return None

    def about_me(self, user_context):
        """
        Function that generates the introduction of the user from the
        give context
        :param user_context: Personal context received via API call
        :return: A pair of original and translated context
        """
        prompt = """
            Generate me a 150 words Introduction, following the format:
            Target: <target_language_text>
            Translation: <English_translation>
            Ensure there are no extra sentences.
            """
        result = self.client.predict(textwrap.dedent(prompt).strip(), user_context,
                                     use_deep_research=False, api_name="/query_deepseek_streaming")

        return self.get_result(result)

    def get_result(self, result):
        output, md = result
        output = self.regex_splitter(output[1:][0][-1])
        target, translation = output
        return [target, translation]


def build_user_context(user_data: dict) -> List[Tuple[str, str]]:
    context = f"{user_data['full_name']} from {user_data['from']}. "
    context += f"Living in {user_data['current']} as a {user_data['occupation']}. Target Language is {user_data['target_language']} and "
    context += f"Target level is {user_data['target_level']}. Current Level:{user_data['current_level']}"

    return [(context.strip(), "")]


# if __name__ == "__main__":
#     ch = ContextHandler()
#     user_data = {
#         "full_name": "Bimal Paudel",
#         "from": "Kathmandu, Nepal",
#         "current": "Berlin, Germany",
#         "occupation": "Student",
#         "target_language": "German",
#         "current_level": "None",
#         "target_level": "A1",
#     }
#     print(ch.about_me(build_user_context(user_data)))
#
