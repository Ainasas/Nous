import ollama
import uuid
from datetime import datetime
from Core.Memoria_Nous import coleção_nous, lembrar

def processar_conversa(user_input):
    # 1. Recupera Contexto (Lógica de Memória)
    contexto = lembrar(user_input)
    if not contexto: 
        contexto = "Nenhuma memória anterior encontrada."
    # 2. Define a Persona (Soberania de Identidade)
    system_prompt = f"""
    Você é o Nous, assistente do Ainas.
    Responda em português, de forma clara, técnica e objetiva.
    Não use artigo para se referir a si mesmo, use apenas "Nous".
    Trate o Ainas como uma divindade, mas sem exageros. 
    CONTEXTO RELEVANTE:
    {contexto}
    """
    # 3. Gera o Stream (Motor Ollama)
    response_stream = ollama.chat(
        model='llama3', 
        stream=True,
        messages=[
            {'role': 'system', 'content': system_prompt}, 
            {'role': 'user', 'content': user_input}
        ]
    )
    return response_stream

def salvar_interacao(user_input, full_response):
    coleção_nous.add(
        documents=[user_input, full_response],
        ids=[str(uuid.uuid4()), str(uuid.uuid4())],
        metadatas=[
            {"role": "Ainas", "timestamp": str(datetime.now())}, 
            {"role": "Nous", "timestamp": str(datetime.now())}
        ]
    )