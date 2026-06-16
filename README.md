## Sobre o Projeto

O GoodWe AI Assistant é um chatbot desenvolvido para o EV Challenge 2026 da FIAP em parceria com a GoodWe.

A solução foi projetada para atuar como um assistente virtual especializado nas plataformas:

- ChargeGrid Intelligence
- EV ChargeOps

O objetivo é fornecer respostas contextualizadas sobre infraestrutura de carregamento para veículos elétricos, modos inteligentes de carregamento e gerenciamento operacional de estações de recarga.

---

## Problema Abordado

O desafio proposto pela GoodWe envolve a necessidade de soluções inteligentes para gerenciamento de carregadores de veículos elétricos.

Entre os principais problemas estão:

- Orquestração eficiente da potência disponível.
- Integração com sistemas fotovoltaicos.
- Monitoramento operacional dos carregadores.
- Gestão compartilhada de infraestrutura de recarga.
- Suporte aos usuários e operadores da plataforma.

O chatbot foi desenvolvido para auxiliar na disseminação dessas informações de forma rápida e acessível.

---

## Tecnologias Utilizadas
### Linguagem
- Python 3.11+
### Modelo de IA
- Llama 3
### Runtime Local
- Ollama
### Técnicas Aplicadas
- System Prompting
- Few-Shot Prompting
- Context Injection
- Conversational Memory

---

## Arquitetura da Solução

Fluxo de funcionamento:

1. Usuário envia uma pergunta.
2. A pergunta é adicionada ao histórico da conversa.
3. O histórico é enviado ao modelo Llama 3 através do Ollama.
4. O modelo gera uma resposta considerando:
    - Contexto GoodWe
    - Histórico da conversa
    - Exemplos Few-Shot
5. A resposta é retornada ao usuário.
6. O histórico é atualizado para manter a continuidade do diálogo.

---

## Funcionalidades
### ChargeGrid Intelligence

O chatbot pode responder perguntas relacionadas a:

- PV Priority
- PV + Battery
- Fast Charging
- Integração com energia solar
- Autoconsumo energético

## EV ChargeOps

O chatbot pode responder perguntas relacionadas a:

- Monitoramento de carregadores
- Gestão de infraestrutura
- Controle operacional
- Uso compartilhado
- Gerenciamento de carga

## Restrição de Escopo

Perguntas fora do contexto GoodWe são recusadas de forma educada para garantir aderência ao escopo definido no desafio.

---

## Instalação
### 1. Instalar o Ollama

Instale o Ollama em:

https://ollama.com

---

### 2. Baixar o modelo

Após instalar o Ollama:

```bash
ollama pull llama3
```

---

### 3. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd goodwe-ai-assistant
```

---

### 4. Criar ambiente virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:
```
source .venv/bin/activate
```

---

### 5. Instalar dependências
```bash
pip install -r requirements.txt
```

---

## Execução

Certifique-se de que o Ollama esteja em execução.

Execute:
```bash
python main.py
```

---