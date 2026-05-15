# 🧠 Nous: Assistente Pessoal

O **Nous** é um assistente digital que construí para gerir as minhas tarefas profissionais de forma inteligente e privada. Em vez de apenas responder a perguntas, o Nous "pensa" através de fluxos de trabalho para organizar o meu e-mail e a minha agenda sem que eu precise de intervir manualmente.

<img width="1280" height="666" alt="nous" src="https://github.com/user-attachments/assets/4bb64109-b6e4-49ac-8bbe-e064de4bda77" />

---
<img width="3744" height="1966" alt="image" src="https://github.com/user-attachments/assets/d5f3ffcd-4a9d-458b-aa4c-648473a5ee64" />


---

## O que o Nous faz por mim?

### Triagem Inteligente de E-mails
O Nous lê a minha caixa de entrada do Gmail e decide sozinho o que é importante:
* **Recrutamento:** Identifica e-mails sobre propostas de emprego e entrevistas.
* **Ações Automáticas:** Se um recrutador pede uma entrevista, o Nous prepara um rascunho de resposta profissional.
* **Hub de Feedback:** Regista automaticamente todos os feedbacks (positivos ou negativos).
* **Limpeza:** Ignora newsletters e spam, poupando o meu tempo de foco.

### Gestão de Agenda
Consigo marcar compromissos apenas falando com o Nous. Ele converte minhas conversas em eventos direto no **Google Calendar**.

## Como foi construído?

O projeto foca-se em **Arquitetura de Sistemas** e **Engenharia de IA**:

* **Inteligência (LLM):** Utiliza o modelo Qwen (via Ollama) a correr localmente.
* **Fluxo de Decisão (LangGraph):** Desenhei um "caminho logico". O Nous segue passos lógicos para não alucinar *Ler -> Classificar -> Decidir Ação -> Executar*.
* **Integrações (APIs):** Conexão direta com as APIs do Google (Gmail e Calendar) para transformar texto em ações.
* **Estruturação de Dados:** O sistema obriga a IA a responder em formatos organizados (JSON), garantindo que não existam erros de interpretação.

---

## Tecnologias Utilizadas
* **Linguagem:** Python
* **Cérebro:** LangChain / LangGraph (Orquestração)
* **Modelo de IA:** Ollama (Local LLM)
* **Interface:** FastAPI
