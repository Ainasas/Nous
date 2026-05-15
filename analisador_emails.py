from typing import TypedDict, Annotated, List, Literal
import operator
from langchain_ollama import ChatOllama
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_gmail_service,
    get_gmail_credentials,
)
from langchain.agents import create_agent
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from Core.auth import autenticar_g

creds = autenticar_g()
service_gmail = build_gmail_service(credentials=creds)

toolkit = GmailToolkit(api_resource=service_gmail)
llm = ChatOllama(model="qwen3:8b-q4_K_M", temperature=0.2)

Nous_email_agent = create_agent(llm, toolkit.get_tools())


class ClassificacaoEmail(BaseModel):
    categoria: Literal["Trabalho", "Distração", "inutil"]
    tipo: Literal["Precisa de Resposta", "Precisa de ação", "Feedback Positivo", "Feedback Negativo"]
    resumo: str = Field(description="Resumo claro e direto do e-mail em no máximo 2 linhas.")

class NousMailState(TypedDict):
    #Fila
    pending_emails: List[str] 
    current_email_id: str     
    job_summaries: Annotated[List[dict], operator.add] 
    
    #E-mail Atual
    quem_mandou: str
    assunto_email: str  
    corpo_email: str
    classificacao: ClassificacaoEmail | None
    draft: str | None
    aprovado_Ainas: bool | None



def ingest_emails_node(state: NousMailState):
    toolkit = GmailToolkit(api_resource=service_gmail)
    search_tool = [t for t in toolkit.get_tools() if t.name == "search_gmail"][0]
    
    today = datetime.now().strftime("%Y/%m/%d")
    query = f"after:{today}" 
    
    print(f"--- [Nous] Iniciando ingestão de e-mails: {query} ---")
    
    results = search_tool.run(query)
    
    email_ids = []
    if isinstance(results, list):
        email_ids = [msg['id'] for msg in results]
    elif isinstance(results, str) and "Message" not in results:
        print(f"--- [Nous] Nenhum e-mail encontrado para o dia {today} ---")
        pass

    print(f"--- [Nous] {len(email_ids)} e-mails encontrados para processamento ---")
    
    return {"pending_emails": email_ids}

def read_content_node(state: NousMailState):
    toolkit = GmailToolkit(api_resource=service_gmail)
    read_tool = [t for t in toolkit.get_tools() if t.name == "get_gmail_message"][0]
    
    # Captura o ID atual antes de removê-lo da fila
    email_id = state["pending_emails"][0]
    
    print(f"--- [Nous] Lendo conteúdo do e-mail: {email_id} ---")
    email_data = read_tool.run(email_id)
    
    remetente = "Desconhecido"
    assunto = "Sem Assunto"
    corpo = ""

    if isinstance(email_data, dict):
        remetente = email_data.get('sender', 'Desconhecido')
        assunto = email_data.get('subject', 'Sem Assunto')
        corpo = email_data.get('body', '')
    
    # Atualizamos a lista de pendentes removendo o primeiro
    remaining_emails = state["pending_emails"][1:]
    
    # É CRUCIAL retornar o current_email_id e o assunto_email aqui
    return {
        "current_email_id": email_id,
        "quem_mandou": remetente,
        "assunto_email": assunto,
        "corpo_email": corpo,
        "pending_emails": remaining_emails
    }
    
def classificar_email_node(state: NousMailState):
    corpo = state.get("corpo_email", "")
    remetente = state.get("quem_mandou", "")
    assunto = state.get("assunto_email", "Sem Assunto") # Pegando o assunto do State
    
    print(f"--- [Nous] Analisando e-mail de: {remetente} ---")
    
    # Prompt atualizado para incluir o Assunto
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é o assistente autônomo Nous. Sua função é ler e-mails corporativos e pessoais e classificá-los estritamente de acordo com o esquema fornecido. "
                   "Não adicione texto extra, retorne apenas os dados solicitados."
                   "Se o e-mail for sobre candidaturas de emprego e status do processo seletivo, classifique como 'Trabalho'"
                   "Se o e-mail for de newsletters, promoções, ou marketing, classifique como 'Distração'"
                   "Se o e-mail for claramente irrelevante, classifique como 'Inutil'"),
        ("user", "Remetente: {remetente}\nAssunto: {assunto}\n\nCorpo do e-mail:\n{corpo}")
    ])
    
    structured_llm = llm.with_structured_output(ClassificacaoEmail)
    chain = prompt | structured_llm
    
    # Passamos o assunto para a chain
    resultado_classificacao = chain.invoke({
        "remetente": remetente, 
        "assunto": assunto, 
        "corpo": corpo
    })
    
    # DEBUG: Isso vai mostrar exatamente o que o Qwen decidiu
    print(f"--- [Nous] decidiu -> Categoria: {resultado_classificacao.categoria} | Tipo: {resultado_classificacao.tipo} ---")
    
    novo_summary = {
        "id": state.get("current_email_id", "sem_id"),
        "remetente": remetente,
        "categoria": resultado_classificacao.categoria,
        "tipo": resultado_classificacao.tipo,
        "resumo": resultado_classificacao.resumo
    }
    
    return {
        "classificacao": resultado_classificacao,
        "job_summaries": [novo_summary]
    }

def router_pos_classificacao(state: NousMailState):
    tipo = state["classificacao"].tipo
    
    if tipo == "Precisa de Resposta":
        return "redigir_draft"
        
    elif tipo in ["Feedback Positivo", "Feedback Negativo"]:
        return "registrar_devolutiva"
        
    else:
        # Caminho para "Futilidade", "Spam", "Interessante", etc.
        # Pula qualquer ação e vai direto para o próximo e-mail ou encerra
        if len(state["pending_emails"]) > 0:
            return "ler_conteudo"
        return "fim"
    
from langchain_core.output_parsers import StrOutputParser

def gerar_draft_node(state: NousMailState):
    remetente = state.get("quem_mandou", "")
    corpo = state.get("corpo_email", "")
    classificacao = state.get("classificacao")
    
    print(f"--- [Nous] Redigindo rascunho para: {remetente} ---")
    
    # Prompt estruturado com contexto profissional
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "Você é Nous, o assistente autônomo. Sua função é redigir um e-mail de resposta em nome de Felipe (Ainas). "
         "Ele é um profissional de tecnologia focado em Arquiterura de Sistemas e Engenharia de AI."
         "Regras estritas: "
         "1. O tom deve ser profissional, direto e educado. "
         "2. Se for um convite para entrevista, demonstre disponibilidade e interesse. "
         "3. Se for um feedback negativo, agradeça a oportunidade e mantenha a porta aberta para o futuro. "
         "4. Retorne APENAS o texto do e-mail. NENHUMA palavra a mais. Não inclua 'Aqui está o rascunho' ou blocos markdown de código. "
         "5. Assine como 'Felipe (Ainas)' no final."
        ),
        ("user", 
         "Tipo de Resposta Esperada: {tipo}\n"
         "Resumo da Situação: {resumo}\n\n"
         "E-mail recebido de {remetente}:\n{corpo}"
        )
    ])
    
    # Encadeia o prompt, o modelo e o parser de saída
    chain = prompt | llm | StrOutputParser()
    
    
    draft_gerado = chain.invoke({
        "tipo": classificacao.tipo,
        "resumo": classificacao.resumo,
        "remetente": remetente,
        "corpo": corpo
    })
    
    return {"draft": draft_gerado}

from langchain_google_community import GmailToolkit

def criar_rascunho_no_gmail_node(state: NousMailState):
    toolkit = GmailToolkit(api_resource=service_gmail)
    draft_tool = [t for t in toolkit.get_tools() if t.name == "create_gmail_draft"][0]
    
    draft_text = state.get("draft")
    email_id = state.get("current_email_id")
    remetente = state.get("quem_mandou")
    assunto = state.get("assunto_email")
    
    print(f"--- [Nous] Injetando rascunho na pasta de Drafts ---")
    
    
    input_params = {
        "message": draft_text,
        "to": [remetente],  
        "subject": f"Re: {assunto}",
        "threadId": email_id
    }
    
    try:
        draft_tool.run(input_params)
        print(f"--- [Nous] Rascunho criado com sucesso ---")
    except Exception as e:
        print(f"--- [Nous] Erro ao criar rascunho: {e} ---")

    return {"draft": None}

import os

def registrar_devolutiva_node(state: NousMailState):
    classificacao = state.get("classificacao")
    remetente = state.get("quem_mandou", "")
    email_id = state.get("current_email_id")
    
    #Hub local do Nous
    hub_file = "Nous_Hub_Devolutivas.md"
    
    print(f"--- [Nous] Registrando {classificacao.tipo} no Hub ---")
    
    # Marcador visual generico
    icone = "🟢" if classificacao.tipo == "Feedback Positivo" else "🔴"
    
    registro = f"### {icone} {classificacao.tipo} - {remetente}\n" \
               f"- **Resumo:** {classificacao.resumo}\n" \
               f"- **ID Thread:** `{email_id}`\n\n"
               
    # Anexa ao arquivo
    with open(hub_file, "a", encoding="utf-8") as f:
        f.write(registro)
        
    
    return {}

def router_verificar_fila(state: NousMailState):
   
    if len(state["pending_emails"]) > 0:
        return "ler_conteudo"
    
    return "fim"

from langgraph.graph import StateGraph, END

# 1. Inicializa o Grafo
workflow = StateGraph(NousMailState)

# 2. Adiciona os Nós
workflow.add_node("ingestao", ingest_emails_node)
workflow.add_node("ler_conteudo", read_content_node)
workflow.add_node("classificar", classificar_email_node)
workflow.add_node("redigir_draft", gerar_draft_node)
workflow.add_node("salvar_draft_gmail", criar_rascunho_no_gmail_node)
workflow.add_node("registrar_devolutiva", registrar_devolutiva_node)

# 3. Arestas 
workflow.set_entry_point("ingestao")
workflow.add_edge("ingestao", "ler_conteudo")
workflow.add_edge("ler_conteudo", "classificar")
workflow.add_edge("redigir_draft", "salvar_draft_gmail") 

# 4. Arestas Condicionais 
workflow.add_conditional_edges(
    "classificar",
    router_pos_classificacao,
    {
        "redigir_draft": "redigir_draft",
        "registrar_devolutiva": "registrar_devolutiva",
        "ler_conteudo": "ler_conteudo", # Retorno direto do loop
        "fim": END                      # Fim direto se a fila esvaziar
    }
)

# 5. Fechamento do Ciclo para os Nós de Ação
for node in ["salvar_draft_gmail", "registrar_devolutiva"]:
    workflow.add_conditional_edges(
        node,
        router_verificar_fila,
        {
            "ler_conteudo": "ler_conteudo",
            "fim": END
        }
    )

# 6. Compilação
nous_app = workflow.compile()

def executar_varredura_emails():
    """Função chamada pelo FastAPI para disparar o LangGraph"""
    print("--- [Sistema] Inicializando Varredura Nous via API... ---")
    
    estado_inicial = {
        "pending_emails": [],
        "current_email_id": "",
        "job_summaries": [],
        "quem_mandou": "",
        "corpo_email": "",
        "classificacao": None,
        "draft": None,
        "aprovado_Ainas": None,
        "assunto_email": ""
    }
    
    # Dispara a execução do grafo
    resultado_final = nous_app.invoke(estado_inicial)
    
    resumos = resultado_final.get('job_summaries', [])
    print(f"--- [Sistema] Ciclo Concluído. {len(resumos)} e-mails processados. ---")
    
    return resumos