"""Compara modelos Ollama com parâmetros idênticos e gera evidências reproduzíveis."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from goodwe_agent.agent import GoodWeAgent  # noqa: E402
from goodwe_agent.config import Settings  # noqa: E402


def keyword_score(response: str, expected_terms: list[str]) -> float:
    normalized = response.casefold()
    hits = sum(term.casefold() in normalized for term in expected_terms)
    return round(100 * hits / len(expected_terms), 1)


def evaluate_model(model_name: str, cases: list[dict], args) -> dict:
    config = Settings(
        model=model_name,
        base_url=args.base_url,
        temperature=args.temperature,
        top_p=args.top_p,
        num_predict=args.max_tokens,
    )
    from goodwe_agent.agent import build_ollama_model

    agent = GoodWeAgent(build_ollama_model(config))
    rows = []
    for case in cases:
        started = time.perf_counter()
        error = None
        try:
            response = agent.ask(case["prompt"], f"benchmark-{model_name}-{case['id']}")
        except Exception as exc:  # relatório registra falhas sem esconder casos
            response, error = "", f"{type(exc).__name__}: {exc}"
        latency = round(time.perf_counter() - started, 3)
        rows.append(
            {
                **case,
                "response": response,
                "latency_seconds": latency,
                "quality_score": keyword_score(response, case["expected_terms"]) if response else 0,
                "error": error,
            }
        )
    successful = [row for row in rows if not row["error"]]
    return {
        "model": model_name,
        "parameters": {
            "temperature": args.temperature,
            "top_p": args.top_p,
            "max_tokens": args.max_tokens,
            "base_url": args.base_url,
        },
        "summary": {
            "cases": len(rows),
            "successful": len(successful),
            "average_quality": round(statistics.mean(row["quality_score"] for row in successful), 1)
            if successful
            else 0,
            "average_latency_seconds": round(
                statistics.mean(row["latency_seconds"] for row in successful), 3
            )
            if successful
            else 0,
        },
        "results": rows,
    }


def markdown_report(payload: dict) -> str:
    lines = [
        "# Relatório de comparação entre modelos",
        "",
        f"Execução UTC: `{payload['executed_at']}`",
        "",
        "## Parâmetros controlados",
        "",
        "Os modelos receberam os mesmos casos, prompt de sistema e parâmetros. "
        "A qualidade automática mede a presença de conceitos esperados; a decisão final deve incluir revisão humana.",
        "",
        "| Modelo | Casos concluídos | Qualidade média | Latência média |",
        "|---|---:|---:|---:|",
    ]
    for model in payload["models"]:
        summary = model["summary"]
        lines.append(
            f"| {model['model']} | {summary['successful']}/{summary['cases']} | "
            f"{summary['average_quality']:.1f}% | {summary['average_latency_seconds']:.3f}s |"
        )
    lines.extend(["", "## Resultados por caso", ""])
    for model in payload["models"]:
        lines.extend(
            [
                f"### {model['model']}",
                "",
                "| Caso | Categoria | Pontuação | Latência | Erro |",
                "|---|---|---:|---:|---|",
            ]
        )
        for row in model["results"]:
            error = (row["error"] or "-").replace("|", "/")
            lines.append(
                f"| {row['id']} | {row['category']} | {row['quality_score']:.1f}% | "
                f"{row['latency_seconds']:.3f}s | {error} |"
            )
        lines.append("")
    ranked = sorted(
        payload["models"],
        key=lambda model: (-model["summary"]["average_quality"], model["summary"]["average_latency_seconds"]),
    )
    winner = ranked[0]
    lines.extend(
        [
            "## Seleção",
            "",
            f"Pelo critério automatizado (maior qualidade e, em empate, menor latência), "
            f"o modelo recomendado é **{winner['model']}**. Confirme a escolha após revisar "
            "as respostas completas no arquivo JSON.",
            "",
            "## Respostas completas",
            "",
        ]
    )
    for model in payload["models"]:
        for row in model["results"]:
            lines.extend([f"### {model['model']} - {row['id']}", "", row["response"] or row["error"], ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["llama3.2:3b", "qwen2.5:3b"])
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--max-tokens", type=int, default=350)
    parser.add_argument("--base-url", default="http://localhost:11434")
    args = parser.parse_args()

    cases = json.loads((ROOT / "evaluation" / "cases.json").read_text(encoding="utf-8"))
    payload = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "models": [evaluate_model(name, cases, args) for name in args.models],
    }
    output_dir = ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "model_comparison.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "relatorio_modelos.md").write_text(markdown_report(payload), encoding="utf-8")
    print(f"Relatórios gerados em: {output_dir}")


if __name__ == "__main__":
    main()
