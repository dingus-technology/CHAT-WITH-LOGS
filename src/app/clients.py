"""
clients.py
"""

from openai import OpenAI


class OpenAIChatClient:
    def __init__(self, api_key, model="gpt-4o"):
        """
        Initialize the OpenAIChatClient.

        :param api_key: The API key for OpenAI.
        :param model: The model to use for the chat (default is "gpt-4").
        """
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages, temperature=0.0, max_tokens=1000):
        """
        Send a chat message to the OpenAI API.

        :param messages: A list of messages in the format [{'role': 'user'|'assistant'|'system', 'content': '...'}].
        :param temperature: Sampling temperature to control creativity (default 0.7).
        :param max_tokens: The maximum number of tokens to generate in the response (default 500).
        :return: The assistant's response as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except NameError as e:
            return f"Error during API call: {e}"
