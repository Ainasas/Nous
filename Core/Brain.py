import ollama
import uuid
from datetime import datetime
from Core.Memoria_Nous import lembrar



def processar_conversa(user_input):
    with open('system_prompt.md', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    contexto = lembrar(user_input)
    
    response_stream = ollama.chat(
        model='Nous', 
        stream=True,
        messages=[
            
            {'role': 'user', 'content':  f'{user_input} considere essas informações para gerar a resposta: {contexto}'}  # Força desativar thinking
        ],
        options={
            'temperature': 0.42 
        }
    )
    return response_stream

def analisar_nota(input_nota):
    analisador_prompt = """
    Você é o subsistema de análise de contexto do Nous. 
    Seu objetivo é analisar as notas e identificar pensamentos que o Ainas acharia interessante
    Analise a nota do Ainas e formate o texto para que seja útil para você e para que sirva de contexto quando Ainas perguntar sobre algo relacionado
    """
    analisador = ollama.chat(
        model='Nous',
        messages=[
            {'role': 'system', 'content': analisador_prompt},
            {'role': 'user', 'content': input_nota}
        ],
        options={
            'temperature': 0.2 
        }
    )
    return analisador['message']['content']

# def salvar_interacao(user_input, full_response):
#     coleção_nous.add(
#         documents=[user_input, full_response],
#         ids=[str(uuid.uuid4()), str(uuid.uuid4())],
#         metadatas=[
#             {"role": "Ainas", "timestamp": str(datetime.now())}, 
#             {"role": "Nous", "timestamp": str(datetime.now())}
#         ]
#     )