import chromadb
from chromadb.utils import embedding_functions

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="nomic-embed-text",
)

client_nous = chromadb.PersistentClient(path=r"C:\Users\nerde\Documents\Projetos\Nous\Memoria")
coleção_nous = client_nous.get_or_create_collection(name="nous_db", embedding_function=ollama_ef)

def lembrar(pergunta, n_resultados = 3):
    resultados = coleção_nous.query(
        query_texts=[pergunta],
        n_results=n_resultados
    )
    return "\n".join(resultados["documents"][0]) # Retorna a resposta concatenada