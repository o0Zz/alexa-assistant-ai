import json
import logging
import requests

_LOGGER = logging.getLogger(__name__)


class ChatGPTAgent:
    def __init__(self, model: str = "gpt-4.1", api_token: str = None):
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_token = api_token
        self.model = model

    def chat(self, messages, max_tokens=None, temperature=None, timeout=None):
        if not self.api_token:
            raise ValueError("OpenAI API token is missing, please set it in the configuration.")

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages
        }

        if max_tokens is not None:
            data["max_tokens"] = max_tokens

        if temperature is not None:
            data["temperature"] = temperature

        _LOGGER.info(f"Requesting: {self.api_url} ...")
        response = requests.post(self.api_url, headers=headers, data=json.dumps(data), timeout=timeout)
        response_data = response.json()

        if not response.ok:
            error_message = response_data.get("error", {}).get("message", response.text)
            raise RuntimeError(f"Error {response.status_code}: {error_message}")

        return response_data["choices"][0]["message"]["content"]
