from ddgs import DDGS
from Core.Memoria_Nous import colecao_ainas
import datetime, uuid

def pesquisar_web(parametros):
    """
    Realiza uma busca no DuckDuckGo usando a versão mais recente da biblioteca
    """
    query = parametros.get('query')
    if not query:
        return "Erro: Nenhuma query de busca fornecida."

    print(f"Nous: Pesquisando na web por: {query}")
    
    resultados_formatados = []
    
    try:
        # Instancia a classe DDGS
        with DDGS() as ddgs:
            results = ddgs.text(
                query=query, 
                region='wt-wt', 
                safesearch='moderate', 
                timelimit='y' 
            )
            
            for i, r in enumerate(results):
                if i >= 3: break
                
                titulo = r.get('title', 'Sem título')
                link = r.get('href', 'Sem link')
                resumo = r.get('body', 'Sem resumo disponível')
                
                resultados_formatados.append(f"Título: {titulo}\nLink: {link}\nResumo: {resumo}\n")
        
        if not resultados_formatados:
            return "A busca não retornou nenhum resultado relevante."
            
        return "\n".join(resultados_formatados)
    
    except Exception as e:
        print(f"ERRO NA BUSCA: {e}")
        return f"Desculpe, houve um erro técnico ao acessar a busca: {str(e)}"


    