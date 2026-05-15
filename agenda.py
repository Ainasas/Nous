from Core.auth import autenticar_g
from googleapiclient.discovery import build
from langchain_core.tools import tool

# É mais eficiente instanciar o serviço globalmente para não recriar a conexão a cada execução
cred = autenticar_g()
calendar_service = build("calendar", "v3", credentials=cred)

@tool
def criar_evento(resumo: str, inicio: str, fim: str, descricao: str = "") -> str:
    """
    Cria um novo evento na agenda do Google Calendar.
    
    Args:
        resumo (str): O título ou nome do evento.
        inicio (str): Data e hora de início estritamente no formato ISO 8601 (ex: '2026-05-04T15:00:00-03:00').
        fim (str): Data e hora de término estritamente no formato ISO 8601 (ex: '2026-05-04T16:00:00-03:00').
        descricao (str, opcional): Descrição detalhada do evento.
    """
    evento = {
        'summary': resumo,
        'description': descricao,
        'start': {
            'dateTime': inicio,
            'timeZone': 'America/Sao_Paulo', 
        },
        'end': {
            'dateTime': fim,
            'timeZone': 'America/Sao_Paulo',
        }
    }
    
    try:
        # Executa a criação do evento usando o serviço instanciado fora da função
        resultado = calendar_service.events().insert(calendarId='primary', body=evento).execute()
        link = resultado.get('htmlLink')
        
        # Retornar uma string descritiva ajuda o LLM a formular a resposta final com sucesso
        return f"Evento '{resumo}' criado com sucesso no Calendar. Link: {link}"
        
    except Exception as e:
        # Retornar o erro como string permite que o LLM informe você caso algo dê errado (ex: formato de data inválido)
        return f"Falha ao criar o evento no Calendar. Erro retornado: {str(e)}"