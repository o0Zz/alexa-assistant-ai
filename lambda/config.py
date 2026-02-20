from agents.github_copilot import GitHubCopilotAgent
from agents.chatgpt import ChatGPTAgent
from agents.claude import ClaudeAgent
from agents.mistral_ai import MistralAI

AGENT = GitHubCopilotAgent(model="gpt-4.1", api_token="your_openai_api_key_here")
#AGENT = ChatGPTAgent(model="gpt-4o-mini", api_token="your_openai_api_key_here")
#AGENT = ClaudeAgent(model="claude-3-5-sonnet-20241022", api_token="your_anthropic_api_key_here")
#AGENT = MistralAI(model="mistral-small-latest", api_token="your_mistral_api_key_here")

ENABLE_FOLLOWUP_SUGGESTIONS = False