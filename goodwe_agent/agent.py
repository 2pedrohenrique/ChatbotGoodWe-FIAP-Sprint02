"""Grafo conversacional com memória de sessão gerenciada pelo LangGraph."""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from .config import Settings, settings
from .guardrails import Decision, evaluate_input
from .prompts import SYSTEM_PROMPT


class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    blocked: bool
    guardrail_decision: str
    refusal: str


def build_ollama_model(config: Settings = settings) -> BaseChatModel:
    return ChatOllama(
        model=config.model,
        base_url=config.base_url,
        temperature=config.temperature,
        top_p=config.top_p,
        num_predict=config.num_predict,
    )


def create_graph(model: BaseChatModel):
    """Monta e compila o pipeline. O checkpointer preserva cada thread_id."""

    def guardrail_node(state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        last_user = next(message for message in reversed(messages) if isinstance(message, HumanMessage))
        result = evaluate_input(str(last_user.content), messages[:-1])
        return {
            "blocked": result.decision is not Decision.ALLOW,
            "guardrail_decision": result.decision.value,
            "refusal": result.response or "",
        }

    def route_after_guardrail(state: AgentState) -> str:
        return "refusal" if state.get("blocked") else "model"

    def refusal_node(state: AgentState) -> AgentState:
        return {"messages": [AIMessage(content=state["refusal"])]}

    def model_node(state: AgentState) -> AgentState:
        conversation = [SystemMessage(content=SYSTEM_PROMPT), *state.get("messages", [])]
        return {"messages": [model.invoke(conversation)]}

    builder = StateGraph(AgentState)
    builder.add_node("guardrail", guardrail_node)
    builder.add_node("model", model_node)
    builder.add_node("refusal", refusal_node)
    builder.add_edge(START, "guardrail")
    builder.add_conditional_edges(
        "guardrail", route_after_guardrail, {"model": "model", "refusal": "refusal"}
    )
    builder.add_edge("model", END)
    builder.add_edge("refusal", END)
    return builder.compile(checkpointer=InMemorySaver())


class GoodWeAgent:
    def __init__(self, model: BaseChatModel | None = None):
        self.model = model or build_ollama_model()
        self.graph = create_graph(self.model)

    def ask(self, message: str, session_id: str = "default") -> str:
        if not message.strip():
            raise ValueError("A mensagem não pode estar vazia.")
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config={"configurable": {"thread_id": session_id}},
        )
        return str(result["messages"][-1].content)

    def history(self, session_id: str = "default") -> list[BaseMessage]:
        snapshot = self.graph.get_state({"configurable": {"thread_id": session_id}})
        return list(snapshot.values.get("messages", [])) if snapshot.values else []


def create_agent(model: BaseChatModel | None = None) -> GoodWeAgent:
    return GoodWeAgent(model=model)
