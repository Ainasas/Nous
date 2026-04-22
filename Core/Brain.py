import ollama
import uuid, json, re
from datetime import datetime
from Core.Memoria_Nous import lembrar, colecao_notas, colecao_chat
from agenda import criar_evento
from Core.auth import autenticar_g
from ferramentas_gerais import pesquisar_web

hoje = datetime.now()

ferramentas_nous = [
  {
    'type': 'function',
    'function': {
      'name': 'criar_evento',
      'description': 'Cria um novo evento na agenda do Google Calendar',
      'parameters': {
        'type': 'object',
        'properties': {
          'resumo': {'type': 'string', 'description': 'O título do evento'},
          'inicio': {'type': 'datetime', 'description': 'Data e hora de início em formato ISO (ex: 2026-04-21T10:00:00-03:00)'},
          'fim': {'type': 'datetime', 'description': 'Data e hora de término em formato ISO'},
          'descricao': {'type': 'string', 'description': 'Detalhes opcionais do evento'}
        },
        'required': ['resumo', 'inicio', 'fim'],
      },
    },
  },
  {
        'type': 'function',
        'function': {
            'name': 'pesquisar_web',
            'description': 'Pesquisa informações em tempo real na internet quando você não souber a resposta ou precisar de dados atuais.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'O termo de busca otimizado para motores de pesquisa'}
                },
                'required': ['query'],
            },
        },
    },
]

def processar_conversa(user_input):
    service = autenticar_g() 
    
    with open('tool_prompt.md', 'r', encoding='utf-8') as f:
        tool_prompt = f.read()

    mensagens = [
        {'role': 'system', 'content': f'{tool_prompt} \n Dia atual: {hoje}'},
        {'role': 'user', 'content': f"Ainas: {user_input}"}
    ]

    response = ollama.chat(
        model='qwen3:8b-q4_K_M', 
        messages=mensagens,
        options={'temperature': 0.1},
        tools=ferramentas_nous 
    )
    
    # 1. Verifica se houve Tool Call
    if response.get('message', {}).get('tool_calls'):
        for call in response['message']['tool_calls']:
            nome_funcao = call['function']['name']
            argumentos = call['function']['arguments']
            
            # Executa a ferramenta escolhida
            if nome_funcao == "criar_evento":
                resultado_ferramenta = criar_evento(service, argumentos)
            elif nome_funcao == "pesquisar_web":
                resultado_ferramenta = pesquisar_web(argumentos)
            
            mensagens.append(response['message']) 
            mensagens.append({
                'role': 'tool', 
                'content': str(resultado_ferramenta), 
                'name': nome_funcao
            })

            
            final_response = ollama.chat(model='qwen3:8b-q4_K_M', messages=mensagens)
            return final_response['message']['content']
    
    return response['message']['content']
            

    

def analisar_nota(input_nota):
    
    with open('system_prompt.md', 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    analisador_prompt = f"""
    {system_prompt}
    Você é o subsistema de análise de contexto do Nous. 
    Seu objetivo é analisar as notas e identificar pensamentos que o Ainas acharia interessante
    Analise a nota do Ainas e formate o texto para que seja útil para você e para que sirva de contexto quando Ainas perguntar sobre algo relacionado
    """
    analisador = ollama.chat(
        model='llama3.1:8b',
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

def execute_tool_calling(model_output):
    """
    Extrai o JSON da resposta do modelo e simula a execução da ferramenta.
    """
    service = autenticar_g() 

    try:
        # 1. Usar Regex para encontrar o conteúdo entre chaves { }
        # Isso protege o código caso o modelo escreva algo como "Aqui está o JSON: { ... }"
        json_match = re.search(r'\{.*\}', model_output, re.DOTALL)
        
        if not json_match:
            print("Erro: Nenhum formato JSON encontrado na resposta.")
            return None

        json_string = json_match.group(0)
        
        # 2. Converter string para dicionário Python
        tool_data = json.loads(json_string)
        
        tool_name = tool_data.get("tool")
        parameters = tool_data.get("parameters", {})

        # 3. Lógica de roteamento das funções
        if tool_name == "criar_evento":
            return criar_evento(service, parameters)
        
        else:
            return f"Ferramenta '{tool_name}' não reconhecida."

    except json.JSONDecodeError as e:
        return f"Erro ao processar JSON: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"