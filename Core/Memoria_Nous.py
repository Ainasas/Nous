import chromadb
from chromadb.utils import embedding_functions
import watchdog

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text",
)

client_nous = chromadb.PersistentClient(path=r"C:\Nous\Memoria")

colecao_notas = client_nous.get_or_create_collection(name="notas_db", embedding_function=ollama_ef)
colecao_livros = client_nous.get_or_create_collection(name="livros_db", embedding_function=ollama_ef)

def lembrar(pergunta, n_resultados = 5):
    resultados = colecao_notas.query(
        query_texts=[pergunta],
        n_results=n_resultados
    )
    return "\n".join(resultados["documents"][0]) # Retorna a resposta concatenada

#def verificar_notas():
    