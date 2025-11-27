# Tecnologias previstas (enxutas)
- Dispositivo: Raspberry Pi 5 / Intel NUC / Jetson Orin (definição posterior conforme POC).
- Áudio: WebRTC (AEC/NR/AGC), Silero VAD; mic array (beamforming).
- ASR PT-BR (local): Whisper.cpp (small/int8). Fallback: Azure/Google STT.
- NLU: Regras + léxico (lojas, andares, categorias; confirmação quando confiança < 0,7).
- Rotas: Grafo JSON + A*/Dijkstra; flag de acessibilidade (evitar escadas).
- Promoções: Sheets/Strapi/Directus → cache local no totem.
- Share: YOURLS/Workers para shortlink + QR; página mobile responsiva.
- Observabilidade: eventos anônimos + Metabase/Grafana.
- Segurança/LGPD: TLS, sessão anônima, tokens curtos, opt-in para qualquer PII.

## Papel do LLM na arquitetura
1) **Entrada**: usuário fala ou digita → ASR local (Whisper) → texto.
2) **NLU/Router**: regras identificam intenção/slots; quando ambíguo, LLM ajuda a desambiguar.
3) **Tool calling (determinístico)**: LLM chama ferramentas:
   - `get_route(destino, acessibilidade)` → A*/Dijkstra (motor de rotas).
   - `list_promos(contexto)` → catálogo oficial de promoções.
4) **Resposta**: LLM gera texto curto e retorna **JSON** com campos obrigatórios para a UI.
5) **Anti-alucinação**: UI só renderiza se o **JSON** validar no *schema*; dados exibidos vêm de ferramentas, nunca “inventados”.
