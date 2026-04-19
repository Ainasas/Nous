# 🧠 Nous
<p align="left">
<img src="https://img.shields.io/badge/Estado-Em%20constru%C3%A7%C3%A3o-%237B1FA2" alt="Estado">
<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/Local-LLM-green" alt="LLM">
</p>

Nous é um assistente pessoal criado para rodar localmente. O objetivo é integrar um modelo LLM a diversas ferramentas de automação, permitindo que ele possua contexto sobre meus documentos pessoais e interaja de forma agradavel.

Status: O projeto está em desenvolvimento ativo e constante evolução.


## Objetivo
No Projeto Nous, meu objetivo era pegar um LLM rodando localmente e ir integrando funções o suficientes para que possa se tornar uma ferramenta de assistencia (Com um pouco de personalidade)

*Esse projeto está em constante construção.*

## Funcionalidades Atuais:
- Chamada por API = Para facilitar a implementação em GUI e outras ferramentas disponibilizei o Nous dentro de uma API
- Chat com memória = Antes de qualquer resposta, Nous decide se precisa de contexto anterior e se sim dá uma query no banco de dados vetorial do ChromaDB
- Ativação por voz = Por padrão Nous fica desativado e só responde caso o seu script ouça uma palavra de ativação que atualmente é "Nous"
- Resposta por som e texto = Ao falar com Nous ele responderá por voz utilizando TTS e por texto como num chat
- Detecção de mudança no meu centro de documentos (Obsidian) e integração automatica do documento para o banco de dados = utilizando a biblioteca Watchdog, Nous detecta mudanças em arquivos de texto em uma pasta de minha escolha (Meu Vault do Obsidian) e integra essas mudanças dentro do seu banco de dados
- Pesquisa na Web através do DuckDuckGo = Nous pode pesquisar informações na internet caso ele não saiba a resposta ou caso for pedido


### Tecnologias utilizadas
- FastAPI
- Ollama
- ChromaDB
- Piper TTS

### Como rodar
1 - Crie um ambiente virtual e instale os requisitos contidos no Requisitos.txt
2 - Atualmente o Nous não possui interface grafica, ele pode ser chamado para conversa usando "python conversa.py" no terminal
3 - Ative o script "python main.py" para habilitar as funções de chamar o Nous por voz e para que seja possivel a detecção de alterações em documentos
