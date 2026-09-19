# GoodWe AI Assistant - Sprint 03

Refatoração do chatbot do EV Challenge 2026 para um pipeline de agentes com
LangGraph, memória por sessão, guardrails e avaliação reproduzível de modelos.

O relatório final da entrega está em `docs/Relatorio_Evolucao_GoodWe_Sprint03.pdf`.

## Integrantes

| Integrante | RM | Responsabilidade principal |
|---|---:|---|
| Pedro Henriue Izidoro Andreaza | 571107 | Integração, documentação e relatório de evolução |
| Eduardo Oliveira Reis | 569727 | Arquitetura do agente e memória |
| Felipe Alves Canazza | 572470 | Comparação de modelos e parametrização |
| Caio Eguia Ceschini | 570798 | Segurança, guardrails e testes |

> Ajuste a divisão acima se ela não representar o trabalho real da equipe.

## Evolução da Sprint 2

| Aspecto | Sprint 2 | Sprint 3 |
|---|---|---|
| Orquestração | Script linear | Grafo `guardrail -> modelo/recusa` |
| Memória | Lista global manual | `InMemorySaver` nativo, separado por `thread_id` |
| Modelos | `llama3` fixo | Qwen 2.5 3B selecionado após benchmark de 2 modelos |
| Segurança | Instrução no prompt | Filtro determinístico + prompt de defesa em profundidade |
| Testes | Ausentes | 11 testes automatizados |
| Evidências | README descritivo | Casos versionados, JSON bruto e relatório Markdown |

## Arquitetura

```text
Usuário + session_id
        |
        v
  [Guardrail determinístico]
        | permitido             | bloqueado
        v                       v
  [LLM via Ollama]        [Recusa segura]
        |                       |
        +----------+------------+
                   v
       [Checkpoint LangGraph por sessão]
```

O guardrail é executado antes do modelo, evitando custo e exposição desnecessários.
O prompt de sistema adiciona uma segunda camada contra alucinação e quebra de escopo.

## Requisitos

- Python 3.11 ou superior
- [Ollama](https://ollama.com/)
- Aproximadamente 5 GB livres para os dois modelos de avaliação

Nenhuma chave de API é necessária. Não versionar arquivos `.env` ou credenciais.

## Instalação

```bash
git clone <URL-DO-REPOSITORIO-DA-SPRINT-03>
cd ChatbotGoodWe-FIAP-Sprint03
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Execução do chatbot

```bash
ollama pull qwen2.5:3b
python main.py --session-id demonstracao
```

Para demonstrar a memória em mais de três turnos, use a mesma sessão:

1. `Explique o PV Priority do ChargeGrid.`
2. `E como ele ajuda no autoconsumo?`
3. `Compare isso ao EV ChargeOps.`
4. `Continue com mais detalhes.`

## Testes

```bash
python -m pytest -q
```

Resultado verificado nesta versão: **11 testes aprovados**. A matriz de segurança
está em `docs/TESTES_SEGURANCA.md`.

## Comparação entre modelos

```bash
ollama pull llama3.2:3b
ollama pull qwen2.5:3b
python scripts/compare_models.py
```

Parâmetros controlados: temperatura `0.2`, `top_p=0.9` e máximo de `350` tokens.
O script executou os mesmos sete casos nos dois modelos e criou:

- `results/model_comparison.json`: entradas, respostas, latências, erros e notas;
- `results/relatorio_modelos.md`: tabela comparativa e seleção justificada.

Resultado: o `qwen2.5:3b` obteve **95,2%** e **7,332 s** de latência média;
o `llama3.2:3b` obteve **85,7%** e **10,427 s**. O Qwen foi selecionado porque
teve melhor nota, menor latência e, na revisão humana, evitou inventar preços e
garantias. Os dados brutos e as respostas completas estão versionados em `results/`.

## Configuração

| Variável | Padrão | Função |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Endpoint local do Ollama |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Modelo selecionado pelo benchmark |
| `OLLAMA_TEMPERATURE` | `0.2` | Variação das respostas |
| `OLLAMA_TOP_P` | `0.9` | Amostragem cumulativa |
| `OLLAMA_NUM_PREDICT` | `350` | Limite de geração |

## Estrutura

```text
goodwe_agent/          núcleo do agente, prompt e guardrails
evaluation/cases.json casos de avaliação versionados
scripts/               comparador de modelos
tests/                 testes automatizados
docs/                  evidências e relatórios
main.py                ponto de entrada
```

## Limitações e próximos passos

- `InMemorySaver` preserva a conversa durante o processo; persistência após reinício
  pode ser adicionada com checkpointer SQLite/PostgreSQL.
- Filtros por padrões não substituem monitoramento contínuo e novos testes adversariais.
- Informações comerciais e especificações devem ser confirmadas nos canais oficiais.

## Integridade acadêmica

A IA apoiou a refatoração e a documentação. A equipe deve compreender o código,
executar a comparação no próprio ambiente, revisar as respostas e manter commits
individuais e regulares no repositório público.
