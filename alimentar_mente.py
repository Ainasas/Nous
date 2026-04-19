import os
from Vigilancia import Obsidian # Reutiliza sua lógica de processamento
import time

def alimentar_nous_historico(caminho_obsidian):
    handler = Obsidian()
    print(f"--- Iniciando Carga de Memória Histórica: {caminho_obsidian} ---")
    
    arquivos_processados = 0
    for raiz, diretorios, arquivos in os.walk(caminho_obsidian):
        for arquivo in arquivos:
            if arquivo.endswith(".md"):
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    handler.processar_nota(caminho_completo)
                    arquivos_processados += 1
                    time.sleep(5)
                except Exception as e:
                    print(f"Erro ao processar {arquivo}: {e}")
    
    print(f"--- Carga Finalizada. {arquivos_processados} notas integradas ao Nous. ---")

if __name__ == "__main__":
    PASTA_NOTAS = r"C:\Endless mind"
    alimentar_nous_historico(PASTA_NOTAS)