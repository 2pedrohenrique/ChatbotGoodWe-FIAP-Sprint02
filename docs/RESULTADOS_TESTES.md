# Resultado da suíte automatizada

Execução realizada em 19/09/2026, com Python 3.14.7.

```text
...........                                                              [100%]
11 passed in 0.62s
```

Cobertura comportamental:

- memória preservada durante quatro turnos;
- isolamento de duas sessões;
- bloqueio de quatro formulações de prompt injection;
- recusa de assunto fora do domínio;
- encaminhamento de instalação elétrica a profissional habilitado;
- aceite de solicitação válida do escopo GoodWe;
- validação de mensagem vazia.

Os testes do pipeline usam uma LLM falsa determinística. Isso valida o grafo sem
depender do Ollama; a qualidade dos modelos reais é medida separadamente pelo script
`scripts/compare_models.py`.
