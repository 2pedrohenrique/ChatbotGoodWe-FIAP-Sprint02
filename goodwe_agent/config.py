"""Configuração centralizada por variáveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))
    top_p: float = float(os.getenv("OLLAMA_TOP_P", "0.9"))
    num_predict: int = int(os.getenv("OLLAMA_NUM_PREDICT", "350"))


settings = Settings()
