import json
import logging
import requests

_LOGGER = logging.getLogger(__name__)

class GitHubCopilotAgent:
	def __init__(self, api_token, model_name):
		self.api_url = "https://models.inference.ai.azure.com/chat/completions"
		self.api_token = api_token
		self.model_name = model_name

	def chat(self, messages, texts, max_tokens=300, temperature=None, timeout=8):
		if not self.api_token:
			raise ValueError(texts["missing_token_error"])

		headers = {
			"Authorization": f"Bearer {self.api_token}",
			"Content-Type": "application/json"
		}

		data = {
			"model": self.model_name,
			"messages": messages,
			"max_tokens": max_tokens
		}

		if temperature is not None:
			data["temperature"] = temperature

		_LOGGER.info(f"Requesting: {self.api_url} ...")
		response = requests.post(self.api_url, headers=headers, data=json.dumps(data), timeout=timeout)
		response_data = response.json()

		if not response.ok:
			error_message = response_data.get("error", {}).get("message", response.text)
			raise RuntimeError(f"Error {response.status_code}: {error_message}")

		return response_data["choices"][0]["message"]["content"]
