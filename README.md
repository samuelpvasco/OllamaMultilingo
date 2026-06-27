# OllamaMultilingo

Chatbot multilíngue 100% local, construído sobre o [Ollama](https://ollama.com). O projeto nasceu como exercício prático de integração com APIs de IA e foi evoluindo para um pipeline de tradução multi-modelo, permitindo conversar com modelos otimizados para inglês (que costumam "raciocinar" melhor nesse idioma) sem perder a naturalidade da resposta no idioma original do usuário.

> 🚧 **Projeto em desenvolvimento.** Algumas partes do pipeline (detecção de idioma/região) ainda estão sendo ajustadas — veja a seção [Status atual](#status-atual) abaixo.

## Como funciona

A ideia central: **cada modelo é usado pra aquilo que ele faz de melhor**, em vez de depender de um único modelo generalista para tudo.

```
Pergunta do usuário (qualquer idioma)
        │
        ▼
  Detecção de idioma
        │
        ▼
  Tradução → Inglês          (se necessário)
        │
        ▼
  Modelo de raciocínio       (ex: gpt-oss:20b)
        │
        ▼
  Tradução → Idioma original (se necessário)
        │
        ▼
  Resposta final ao usuário
```

Esse desenho evita uma limitação comum de LLMs: muitos modelos foram treinados majoritariamente em inglês e "pensam" com mais qualidade nesse idioma, mesmo conseguindo responder em outros. Traduzindo a pergunta antes e a resposta depois, o usuário pode conversar livremente no seu idioma sem perder qualidade de raciocínio do modelo.

## Estrutura do projeto

```
.
├── main.py              # Ponto de entrada: seleciona o modelo e inicia o chat
├── functions/
│   ├── chat.py          # Loop de conversa (orquestra todo o pipeline)
│   ├── messages.py      # Comunicação com a API do Ollama (envio de mensagens, listagem de modelos)
│   └── translate.py     # Detecção de idioma e tradução
```

## Pré-requisitos

- [Ollama](https://ollama.com) instalado e rodando localmente (`ollama serve`)
- Pelo menos um modelo de linguagem baixado (ex: `ollama pull llama3.2`)
- Python 3.10+

## Instalação

```bash
git clone https://github.com/samuelpvasco/OllamaMultilingo.git
cd OllamaMultilingo
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com as URLs da API local do Ollama:

```env
OLLAMA_URL="http://localhost:11434/api/chat"
OLLAMA_MODELS_URL="http://localhost:11434/api/tags"
```

## Uso

```bash
python main.py
```

O programa lista os modelos disponíveis no seu Ollama, você escolhe um pelo número, e a conversa começa direto no terminal. Digite `exit` para encerrar a sessão.

## Modelos utilizados no pipeline

| Etapa | Modelo (exemplo) | Motivo |
|---|---|---|
| Detecção de idioma | `llama3.2:(1b ou 3b)` | Classificação leve e rápida |
| Tradução | `translategemma:4b` | Modelo especializado em tradução |
| Raciocínio / resposta | `gpt-oss:20b` | Modelo maior, melhor qualidade de resposta |

Você pode trocar qualquer um desses pelo modelo da sua preferência, desde que esteja disponível no seu Ollama local.

## Status atual

- [x] Chat básico com histórico de conversa e streaming de resposta
- [x] Pipeline de tradução automática (pergunta → inglês → resposta → idioma original)
- [ ] Detecção de **regionalidade** (ex: `pt-BR` vs `pt-PT`) — em ajuste, avaliando uso de [fastText](https://fasttext.cc/) combinado com classificação leve via LLM
- [ ] Agentes especializados por domínio (Python, SQL, AWS, Terraform) roteando para um modelo de raciocínio fixo

## Aprendizados

Este projeto foi construído como prática de integração com IA, e ao longo do caminho trouxe aprendizados sobre:
- Streaming de respostas via API (NDJSON)
- Limitações de modelos pequenos em tarefas de classificação estruturada (ex: seguir formato JSON)
- Trade-offs entre usar um LLM generalista vs. uma ferramenta especializada (ex: fastText) para tarefas de classificação simples
- Gerenciamento de memória/troca de modelos no Ollama em pipelines com múltiplas chamadas

## Licença

MIT