from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from agenda import criar_evento

class NousChatState(TypedDict):
    mensagens: Annotated[List[BaseMessage], add_messages] 

@tool
def criar_evento(resumo: str, inicio: str, fim: str, descricao: str = "") -> str:
    """Cria um novo evento na agenda do Google Calendar."""
    return f"Evento '{resumo}' criado com sucesso."

@tool
def pesquisar_web(query: str) -> str:
    """Pesquisa informações em tempo real na internet."""
    return f"Resultados para: {query}"

tools = [criar_evento]
tool_node = ToolNode(tools)

llm = ChatOllama(model="qwen3:8b-q4_K_M", temperature=0)
llm_with_tools = llm.bind_tools(tools)

with open('tool_prompt.md', 'r', encoding='utf-8') as f:
    TOOL_PROMPT = f.read()
    
with open('system_prompt.md', 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

COMBINED_PROMPT = f"{SYSTEM_PROMPT}\n\n{TOOL_PROMPT}"

def call_model(state: NousChatState):
    messages = state["mensagens"]
    prompt_sistema = SystemMessage(content=COMBINED_PROMPT)
    full_messages = [prompt_sistema] + messages
    
    response = llm_with_tools.invoke(full_messages)
    return {"mensagens": [response]}

def should_continue(state: NousChatState) -> str:
    messages = state["mensagens"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    
    return END 

workflow = StateGraph(NousChatState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

Nous_chat_app = workflow.compile()

def processar_conversa(user_input):
    initial_state = NousChatState(mensagens=[HumanMessage(content=user_input)])
    final_state = Nous_chat_app.invoke(initial_state)
    
    resposta_final = final_state["mensagens"][-1].content
    return resposta_final