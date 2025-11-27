# Arquitetura conceitual (Sprint 1)
## Camadas
- Interação & Sensores (voz/toque; presença)
- Borda (ASR local, NLU leve, regras)
- Serviços (navegação, promoções, share)
- Dados (ingestão, armazenamento leve, métricas)
- Visualização (UI totem + página mobile)
- Segurança/Observabilidade (transversal)

## Fluxo típico
Usuário (voz/toque) → áudio limpo → ASR local → NLU → Navegação/Promo → UI/QR → logs anônimos.

