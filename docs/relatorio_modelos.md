# Comparação entre modelos - resultado final

Execução realizada em 19/09/2026 com Ollama local.

## Parâmetros controlados

- Modelos: `llama3.2:3b` e `qwen2.5:3b`
- Temperatura: `0.2`
- `top_p`: `0.9`
- Máximo de geração: `350` tokens
- Mesmo prompt de sistema e os mesmos sete casos para ambos

## Resultados

| Modelo | Casos concluídos | Qualidade média | Latência média |
|---|---:|---:|---:|
| llama3.2:3b | 7/7 | 85,7% | 10,427 s |
| qwen2.5:3b | 7/7 | 95,2% | 7,332 s |

## Seleção justificada

O modelo selecionado foi **qwen2.5:3b**. Ele apresentou qualidade automática
9,5 pontos percentuais superior e latência média 29,7% menor.

A revisão humana reforçou a decisão: no caso de limite factual, o Llama 3.2
inventou nomes de modelos, preços e garantias, contrariando a instrução de não
inventar especificações. O Qwen declarou não possuir os dados e orientou a consulta
ao canal oficial GoodWe. Nos três casos bloqueados pelos guardrails, ambos obtiveram
100%, pois a recusa ocorreu antes da inferência.

## Evidências

- `results/model_comparison.json`: parâmetros, respostas completas, tempos e notas.
- `results/relatorio_modelos.md`: relatório integral gerado pelo comparador.
- `evaluation/cases.json`: casos e conceitos esperados versionados.

Observação: a primeira inferência de cada modelo inclui o carregamento em memória,
e por isso foi consideravelmente mais lenta. A latência média registrada representa
a execução completa observada no ambiente de teste.
