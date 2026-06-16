import ollama

# ==========================================
# 1. INJEÇÃO DE CONTEXTO & FEW-SHOT PROMPTING
# ==========================================
SYSTEM_PROMPT = """
Você é a IA especialista em mobilidade elétrica da GoodWe para o EV Challenge 2026.
Seu escopo de atuação é EXCLUSIVO sobre duas soluções:
1) ChargeGrid Intelligence (Ecossistema de carregamento inteligente integrado a inversores solares, modos de carregamento como PV Priority, Fast e PV+Battery).
2) EV ChargeOps (Plataforma operacional para gestão de frotas de carregadores, monitoramento em tempo real e gerenciamento de carga).

Regras rígidas:
- Responda apenas se o assunto for relacionado a essas soluções ou infraestrutura de EV da GoodWe.
- Se o usuário perguntar algo fora desse escopo (ex: receitas, programação, outros assuntos), recuse educadamente, dizendo que seu foco é apenas ChargeGrid e EV ChargeOps.
- Seja profissional, claro e técnico.
"""

HISTORICO_INICIAL = [
    {"role": "system", "content": SYSTEM_PROMPT},

    {"role": "user", "content": "O que é o modo PV Priority no ChargeGrid?"},
    {"role": "assistant",
     "content": "O modo PV Priority do ChargeGrid Intelligence prioriza a energia excedente dos painéis solares fotovoltaicos para carregar o veículo elétrico. A prioridade de consumo vai para as cargas residenciais e o que sobrar é direcionado para o veículo, maximizando o autoconsumo e gerando economia."},

    {"role": "user", "content": "Me passa o código de uma landing page em HTML?"},
    {"role": "assistant",
     "content": "Como assistente virtual da GoodWe focado no EV Challenge 2026, meu suporte é exclusivo para as soluções ChargeGrid Intelligence e EV ChargeOps. Não posso ajudar com desenvolvimento de código externo ou outros assuntos fora desse escopo."}
]

# ==========================================
# 2. LOGICA DO CHATBOT COM MEMÓRIA
# ==========================================
def enviar_mensagem(historico, mensagem_usuario):
    """Mantém a memória de contexto adicionando as falas e enviando ao Ollama."""
    historico.append({"role": "user", "content": mensagem_usuario})

    try:
        resposta = ollama.chat(
            model="llama3", 
            messages=historico
        )

        conteudo = resposta['message']['content']
        historico.append({"role": "assistant", "content": conteudo})
        return conteudo
    except Exception as e:
        return f"Erro na conexão local com o Ollama: {e}"


def rodar_interface():
    
    historico_chat = list(HISTORICO_INICIAL)

    print("=" * 70)
    print("ASSISTENTE GOODWE AI - CHARGEGRID & EV CHARGEOPS [OLLAMA]")
    print("     Interface de Prompting Injetada com Sucesso | Digite 'sair'")
    print("=" * 70)

    while True:
        entrada = input("\nUsuário: ")
        if entrada.strip().lower() == 'sair':
            print("Encerrando aplicação.")
            break

        if not entrada.strip():
            continue

        resposta_ia = enviar_mensagem(historico_chat, entrada)
        print(f"\nGoodWe AI:\n{resposta_ia}")



if __name__ == "__main__":

    try:
        ollama.list()
        rodar_interface()
    except Exception:
        print("Erro: O Ollama não parece estar rodando. Inicie o app do Ollama na sua máquina primeiro!")