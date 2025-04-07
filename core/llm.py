import textwrap
from gradio_client import Client
from utils.helpers import get_result


class Llama:
    """
    Contains method to handle all kinds of contexts from frontend.
    TODO: Think of a better name
    """
    def __init__(self):
        client_id = "openfree/Llama-4-Maverick-17B-Research"
        self.client = Client(client_id)

    def generate_translation_pair(self, user_context, prompt):
        """
        Method that generates target language output and translation output. Controls the
        output format irrespective of the user context.
        :param user_context:  Historical context of the user. List[Tuple[str, str]]
        :param prompt: Prompt to generate output for. String
        :return: A pair of original and translated context. List[str]
        """
        result = self.client.predict(textwrap.dedent(prompt).strip(), user_context,
                                     use_deep_research=False, api_name="/query_deepseek_streaming")

        return get_result(result)

    def generate_text(self, prompt):
        """
        Method to generate text for a given context. For example if a user clicks on "Ein",
        it explains the context shortly
        :param prompt: Prompt to generate text for. String
        :return:
        """
        result = self.client.predict(textwrap.dedent(prompt).strip(),[],
                                     use_deep_research=False, api_name="/query_deepseek_streaming")
        return result
