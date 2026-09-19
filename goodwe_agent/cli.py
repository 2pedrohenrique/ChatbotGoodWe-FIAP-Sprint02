"""Interface de linha de comando."""

from __future__ import annotations

import argparse
import uuid

from .agent import GoodWeAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="GoodWe AI Assistant - Sprint 03")
    parser.add_argument("--session-id", default=str(uuid.uuid4()), help="Identificador da sessão")
    args = parser.parse_args()

    agent = GoodWeAgent()
    print("=" * 68)
    print("GOODWE AI ASSISTANT - CHARGEGRID & EV CHARGEOPS [LANGGRAPH]")
    print(f"Sessão: {args.session_id} | Digite 'sair' para encerrar")
    print("=" * 68)

    while True:
        try:
            message = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSessão encerrada.")
            return
        if message.casefold() == "sair":
            print("Sessão encerrada.")
            return
        if not message:
            continue
        try:
            print(f"\nGoodWe AI: {agent.ask(message, args.session_id)}")
        except Exception as exc:
            print(f"\nFalha ao consultar o modelo: {exc}")
            print("Confirme se o Ollama está ativo e se o modelo foi baixado.")
