# Solução (alto nível)
1) **Entrada** por toque/voz (PTT ou wake-word); áudio limpo (AEC/NR/VAD/beamforming).
2) **ASR local** (Whisper.cpp) → **NLU** (intenções/slots por regras).
3) **Navegação indoor**: grafo + A*/Dijkstra; respeita acessibilidade.
4) **Promoções** por contexto (destino/categoria/horário).
5) **Compartilhar**: gera QR/link com expiração; sem PII por padrão.
6) **Métricas** anônimas para melhorias e provas de valor.

## LLM (modelo de linguagem) — estratégia prevista

- **Primário (cloud, baixa latência e tooling):** OpenAI (GPT-4o mini / GPT-4.1 via API) **ou** Azure OpenAI (equivalente corporativo).
- **Alternativas compatíveis:** Anthropic Claude, Google Gemini (dependendo de contrato/custo).
- **Edge (opcional em versão avançada):** LLM pequeno local (ex.: Llama-3.1-instruct 8B quantizado) apenas para rascunhos/UX, mantendo cálculo de rotas e dados em módulos determinísticos.
- **Padrão de uso:** o LLM atua como **orquestrador** e **gerador de linguagem**, sempre com:
  - **Function calling / tool calling** para consultar rotas, diretório de lojas e promoções.
  - **Respostas em JSON válido** conforme *schema* acordado.
  - **Grounding/RAG** quando necessário (catálogo oficial de lojas/promos).
  - **Política anti-alucinação**: se não houver dado, responder “não encontrado” + **sugestões verificáveis**.
- **Privacidade:** nenhuma PII enviada ao LLM sem **consentimento**; prompts só incluem dados anônimos/contextuais (ex.: `totem_id`, `piso`).
