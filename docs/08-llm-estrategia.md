# Estratégia de uso de LLM (Large Language Model)

## 1. Papel do LLM no Totem Inteligente

O modelo de linguagem (LLM) será responsável por **entender comandos complexos**, **orquestrar agentes especializados** e **gerar respostas curtas e naturais** ao usuário.  
Ele atua como uma camada cognitiva do sistema, interpretando intenções e coordenando as ações entre os módulos de fala, navegação, promoções e interface.

### Funções principais:
1. **Compreensão de linguagem natural (NLU avançada):** interpretar frases abertas e ambiguidades (“Onde fica a Renner?”, “Tem cinema aqui?”).  
2. **Orquestração de agentes:** decidir qual módulo (Navegação, Promoções, Acessibilidade, Ajuda) deve responder.  
3. **Geração de respostas naturais:** transformar a resposta técnica dos agentes em uma frase amigável para o visitante.  
4. **Desambiguação e confirmação:** quando houver dúvida ou baixa confiança, o LLM confirma antes de agir (“Você quis dizer Cinemark no L2?”).

---

## 2. Modelo selecionado

| Ambiente | Modelo | Finalidade | Observações |
|-----------|---------|-------------|--------------|
| **Nuvem (principal)** | OpenAI GPT-4o mini / GPT-4.1 (via API) | Orquestração, linguagem e tool calling | Excelente suporte a PT-BR, JSON válido e baixa latência |
| **Alternativas Cloud** | Azure OpenAI / Anthropic Claude / Google Gemini | Backup corporativo ou custo reduzido | Compatíveis com ferramentas e prompt controlado |
| **Edge (opcional – offline)** | Llama-3.1-Instruct-8B quantizado (GGUF) | Fallback local para respostas simples | Mantém operação básica sem internet |

O modelo será chamado via **API segura (HTTPS)** e receberá apenas **dados contextuais e anônimos** — nunca informações pessoais do usuário.

---

## 3. Fluxo de processamento com o LLM

graph LR
A[Usuario: voz/toque] --> B[ASR local (Whisper.cpp)]
B --> C[NLU e Regras]
C -->|Ambiguo?| D[LLM Orquestrador]
D --> E{Ferramenta necessaria?}
E -->|Rota| F[get_route]
E -->|Promocao| G[list_promos]
F --> H[Resposta JSON]
G --> H
H --> I[LLM gera fala curta e amigavel]
I --> J[UI Totem + QR/link]
J --> K[Logs anonimos -> Nuvem]



Você é o orquestrador de um totem inteligente em um shopping center.
- Seu papel é entender o que o visitante quer e chamar ferramentas conforme a intenção.
- **Nunca invente** nomes de lojas, rotas ou promoções.
- Use sempre as funções disponíveis: `get_route`, `list_promos`, `get_help`, `get_access_route`.
- Responda em **português natural e breve**.
- Saída **sempre em JSON** no formato:
{
  "intent": "...",
  "spoken_reply": "...",
  "route": {...},
  "promos": [...],
  "confirm_needed": false
}


sequenceDiagram
    participant U as Usuario
    participant ASR as ASR (Whisper.cpp)
    participant NLU as NLU/Regras
    participant LLM as LLM Orquestrador
    participant NAV as get_route
    participant PROMO as list_promos
    participant UI as UI/QR
    participant LOG as Logs Nuvem

    U->>ASR: Fala/PTT
    ASR-->>NLU: Texto
    NLU-->>LLM: Intencao/Slots (ou ambiguo)
    LLM->>NAV: get_route(destino, acessibilidade)?
    LLM->>PROMO: list_promos(contexto)?
    NAV-->>LLM: Rota (JSON)
    PROMO-->>LLM: Promocoes (JSON)
    LLM-->>UI: Resposta curta + JSON
    UI-->>LOG: Eventos anonimos
