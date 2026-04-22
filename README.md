# 🧠 Nous

<p align="left">
  <img src="https://img.shields.io/badge/Status-Em%20construção-%23BA7517" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LLM-Local-green" alt="LLM Local">
  <img src="https://img.shields.io/badge/Ollama%20·%20ChromaDB%20·%20Piper%20TTS-purple" alt="Stack">
</p>

Nous é um assistente pessoal que roda inteiramente de forma local. O projeto conecta um modelo LLM a ferramentas de automação, permitindo contexto sobre documentos pessoais, resposta por voz e uma pitada de personalidade.

> **Nota:** Este projeto está em evolução constante. Novas funcionalidades são adicionadas regularmente.

---

## Sobre o projeto

A ideia central é simples: pegar um LLM local e ir adicionando integrações até que ele se torne uma ferramenta de assistência real — não apenas um chatbot genérico, mas algo com contexto, autonomia e jeito próprio.

---

## Funcionalidades

### ✅ Disponíveis agora

- **Resposta por voz e texto** — Nous responde falado (via TTS) e por texto simultaneamente, como um chat com áudio
- **Análise de notas pessoais** — A pedido, Nous itera sobre minhas notas, analisa cada uma e armazena no banco vetorial para uso como contexto futuro
- **Chamada de ferramenta** - Nous é capaz de chamar ferramentas, como marcar eventos no calendário

### 🚧 Em desenvolvimento

- **Memória de conversa** — Antes de responder, Nous decide se precisa de contexto anterior e consulta o ChromaDB automaticamente
- **Pesquisa na web** — Integração com DuckDuckGo para buscar informações quando não souber a resposta ou quando solicitado
- **Aleatoriedade autônoma** — Ao iniciar, horários aleatórios são gerados para disparar funções espontâneas: `curiosidade_aleatoria`, `analisar_tela_atual`, `lembrar_tarefa`

---

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Modelo local | [Ollama](https://ollama.com) |
| Memória vetorial | [ChromaDB](https://www.trychroma.com) |
| Síntese de voz | [Piper TTS](https://github.com/rhasspy/piper) |
