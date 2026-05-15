from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import processar_conversa

# Importando a função
from analisador_emails import executar_varredura_emails

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str
    user: str = "Ainas"

@app.post("/chat")
async def chat(body: Message):
    response = processar_conversa(body.message)
    return {"response": response}

# Foco no Hub de E-mails
@app.get("/sync_emails")
async def sync_emails():
    try:
        # Aciona o LangGraph e espera ele terminar de processar, ler, rascunhar
        resumos = executar_varredura_emails()
        
        # Devolve o JSON estruturado
        return {"status": "success", "job_summaries": resumos}
    except Exception as e:
        return {"status": "error", "detail": str(e)}