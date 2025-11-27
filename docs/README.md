- Interação via **toque ou voz (PTT/wake-word)** com áudio limpo (AEC/NR/VAD/beamforming).  
- **ASR local (Whisper.cpp)** → texto → **NLU (regras + LLM)** para interpretar intenção e slots.  
- **Rotas indoor determinísticas (A*/Dijkstra)** com acessibilidade.  
- **Promoções contextuais** filtradas por loja, horário e categoria.  
- **Envio para celular** via link curto/QR com expiração.  
- **Coleta anônima de métricas** para análise e melhoria contínua.  

> Descricao em [`/docs/02-solucao-em-alto-nivel.md`](/docs/02-solucao-em-alto-nivel.md)

---

## 🧠 4. Estratégia de LLM (Large Language Model)
O **LLM** é o cérebro linguístico que entende o visitante, aciona módulos e produz respostas curtas e naturais.

### Modelos previstos
| Ambiente | Modelo | Função | Observações |
|-----------|---------|---------|--------------|
| **Nuvem (principal)** | GPT-4o mini / GPT-4.1 (Azure OpenAI) | Interpretação, orquestração e linguagem | JSON válido + tool calling + baixa latência |
| **Alternativos** | Claude / Gemini | Backup ou custo reduzido | Compatíveis com JSON e PT-BR |
| **Edge (offline)** | Llama 3.1-Instruct 8B (GGUF) | Fallback local básico | Mantém UX sem internet |

### Funções
- **Compreender** frases abertas (“Onde fica a Renner?”)  
- **Desambiguar/Confirmar** quando confiança < 0.7  
- **Orquestrar** ferramentas (`get_route`, `list_promos`, `get_help`)  
- **Gerar** respostas breves e naturais  

### Fluxo de decisão
graph LR
A[Usuario: voz ou toque] --> B[ASR local (Whisper cpp)]
B --> C[NLU e Regras]
C -->|Ambiguo?| D[LLM Orquestrador]
D --> E{Ferramenta necessaria?}
E -->|Rota| F[get_route]
E -->|Promocao| G[list_promos]
F --> H[Resposta JSON]
G --> H
H --> I[LLM gera fala curta e amigavel]
I --> J[UI Totem + QR ou Link]
J --> K[Logs anonimos -> Nuvem]
