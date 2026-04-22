from Core.auth import autenticar_g

cred = autenticar_g()

def criar_evento(cred, parametros):
    resumo = parametros.get('resumo')
    descricao = parametros.get('descricao', "") 
    inicio = parametros.get('inicio')
    fim = parametros.get('fim')
    
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
    
    return cred.events().insert(calendarId='primary', body=evento).execute()
