"""OpenAI-compatible LLM client for DeepSeek API."""

import json
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()


@dataclass
class LLMConfig:
    api_key: str = field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"))
    model: str = field(default_factory=lambda: os.getenv("DEEPSEEK_MODEL", "deepseek-chat"))
    temperature: float = 0.3
    max_tokens: int = 8192

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls()


class LLMClient:
    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig.from_env()
        if not self.config.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set. Copy .env.example to .env and fill in your API key.")
        self._client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
        )

    def chat(self, system_prompt: str, user_msg: str) -> str:
        response = self._client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
        )
        return response.choices[0].message.content or ""

    def chat_json(self, system_prompt: str, user_msg: str) -> dict:
        raw = self.chat(system_prompt, user_msg)
        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first and last fence lines
            start = 1 if lines[0].startswith("```") else 0
            end = -1 if lines[-1].strip() == "```" else len(lines)
            cleaned = "\n".join(lines[start:end])
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"raw_response": raw, "_parse_error": True}
