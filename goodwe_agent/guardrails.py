"""Guardrails determinísticos executados antes da chamada ao modelo."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from langchain_core.messages import BaseMessage


class Decision(str, Enum):
    ALLOW = "allow"
    INJECTION = "injection"
    OUT_OF_SCOPE = "out_of_scope"
    PROFESSIONAL_REQUIRED = "professional_required"


@dataclass(frozen=True)
class GuardrailResult:
    decision: Decision
    response: str | None = None


INJECTION_PATTERNS = (
    r"ignore\s+(todas?\s+)?(as\s+)?(instru[cç][oõ]es|regras)",
    r"(revele|mostre|imprima|repita).{0,35}(prompt|mensagem de sistema|system prompt)",
    r"(jailbreak|developer mode|modo desenvolvedor|dan mode)",
    r"finja que (n[aã]o|voc[eê] deixou de)",
    r"desconsidere.{0,35}(prompt|regras|instru[cç][oõ]es)",
)

SCOPE_TERMS = {
    "goodwe", "chargegrid", "charge grid", "ev chargeops", "chargeops",
    "carregador", "carregamento", "recarga", "veículo elétrico", "veiculo eletrico",
    "energia solar", "fotovolta", "inversor", "pv priority", "pv + battery",
    "fast charging", "eletroposto", "gestão de carga", "gestao de carga",
    "balanceamento de carga", "frota", "estação de recarga", "estacao de recarga",
}

FOLLOW_UP_MARKERS = {
    "isso", "ele", "ela", "esse", "essa", "também", "tambem", "e como",
    "e qual", "e quanto", "pode explicar", "continue", "mais detalhes",
}

RISK_PATTERNS = (
    r"dimension(e|ar).{0,30}(disjuntor|cabo|instala[cç][aã]o)",
    r"qual (cabo|disjuntor).{0,30}(devo|usar|instalar)",
    r"fa[cç]a (o|um) projeto el[eé]trico",
    r"como ligar.{0,30}(rede|quadro|disjuntor)",
)

REFUSALS = {
    Decision.INJECTION: (
        "Não posso alterar minhas regras nem revelar instruções internas. "
        "Posso ajudar com ChargeGrid Intelligence e EV ChargeOps."
    ),
    Decision.OUT_OF_SCOPE: (
        "Este assistente atende exclusivamente a dúvidas sobre ChargeGrid Intelligence, "
        "EV ChargeOps e infraestrutura de recarga GoodWe."
    ),
    Decision.PROFESSIONAL_REQUIRED: (
        "Por segurança, não posso dimensionar ou orientar uma instalação elétrica "
        "individualizada. Consulte um profissional habilitado e as normas locais. "
        "Posso explicar os recursos gerais das soluções GoodWe."
    ),
}


def _contains(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def _has_scope(text: str) -> bool:
    lowered = text.casefold()
    return any(term in lowered for term in SCOPE_TERMS)


def evaluate_input(text: str, previous_messages: list[BaseMessage] | None = None) -> GuardrailResult:
    """Classifica a entrada antes que ela alcance a LLM."""
    normalized = " ".join(text.split())
    if _contains(normalized, INJECTION_PATTERNS):
        return GuardrailResult(Decision.INJECTION, REFUSALS[Decision.INJECTION])
    if _contains(normalized, RISK_PATTERNS):
        return GuardrailResult(
            Decision.PROFESSIONAL_REQUIRED,
            REFUSALS[Decision.PROFESSIONAL_REQUIRED],
        )
    if _has_scope(normalized):
        return GuardrailResult(Decision.ALLOW)

    lowered = normalized.casefold()
    is_follow_up = any(marker in lowered for marker in FOLLOW_UP_MARKERS) or len(normalized.split()) <= 5
    prior_in_scope = any(_has_scope(str(message.content)) for message in (previous_messages or []))
    if is_follow_up and prior_in_scope:
        return GuardrailResult(Decision.ALLOW)
    return GuardrailResult(Decision.OUT_OF_SCOPE, REFUSALS[Decision.OUT_OF_SCOPE])
