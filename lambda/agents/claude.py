import json
import logging
import requests

_LOGGER = logging.getLogger(__name__)


class ClaudeAgent:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022", api_token: str = None):
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.api_token = api_token
        self.model = model

    def chat(self, messages, max_tokens=None, temperature=None, timeout=None):
        if not self.api_token:
            raise ValueError("Claude API token is missing, please set it in the configuration.")

        system_parts = []
        anthropic_messages = []
        for message in messages or []:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                system_parts.append(content)
                continue

            mapped_role = "assistant" if role == "assistant" else "user"
            anthropic_messages.append({"role": mapped_role, "content": content})

        if not anthropic_messages:
            anthropic_messages = [{"role": "user", "content": ""}]

        payload = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens if max_tokens is not None else 300
        }

        if system_parts:
            payload["system"] = "\n\n".join(system_parts)

        if temperature is not None:
            payload["temperature"] = temperature

        headers = {
            "x-api-key": self.api_token,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        _LOGGER.info(f"Requesting: {self.api_url} ...")
        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=timeout)
        response_data = response.json()

        if not response.ok:
            error_message = response_data.get("error", {}).get("message", response.text)
            raise RuntimeError(f"Error {response.status_code}: {error_message}")

        content_blocks = response_data.get("content", [])
        text_parts = [block.get("text", "") for block in content_blocks if block.get("type") == "text"]
        return "".join(text_parts).strip()
