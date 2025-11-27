# Guia rápido para o vídeo da Sprint 2

> Objetivo: demonstrar em até 5 minutos o ciclo **sensor → banco SQL → análise/visualização + ML supervisionado** do Totem Flexmedia.

## 1. Preparação

1. `pip install --user -r requirements.txt`
2. `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` (se necessário)
3. `python src/sensors/simulation.py --duration 60` (opcional para gerar dados extras antes da gravação)
4. Abra o dashboard (`.\run_demo.ps1`) e deixe o navegador em tela cheia em `http://localhost:8501`.

## 2. Roteiro sugerido

| Bloco | Duração | Ação / Falas |
|-------|---------|--------------|
| Abertura | 20s | Apresente o desafio e mostre rapidamente o repositório/arquitetura (`docs/09-arquitetura-sprint2.md`). |
| Sensores + Banco | 60s | Mostre o `run_demo.ps1` iniciando a simulação e explique que os eventos são gravados no SQLite (`data/totem.db`). |
| Dashboard | 120s | Navegue pelo Streamlit: KPIs, timeline, pizza e tabela. Destaque o indicador “Touch Events %” e como os dados se atualizam. |
| ML Supervisionado | 60s | No terminal, execute `python src/analytics/ml_training.py`. Mostre a acurácia e explique o critério (toque curto < 1s). Em seguida, volte ao dashboard e destaque a seção “ML Insights”. |
| Encerramento | 30s | Reforce que o fluxo sensor → banco → análise → insights inteligentes está operacional e a base pode ser expandida para sensores reais. |

## 3. Capturas e prints

- Realize screenshots do dashboard (KPIs + gráficos + ML Insights) e inclua na documentação técnica.
- Capture o terminal mostrando o relatório do script de ML e anexe à documentação/README.

## 4. Checklist antes de gravar

- [ ] Banco `data/totem.db` contém eventos recentes.
- [ ] Dashboard atualiza métricas em tempo real (sem mensagem de “Waiting for sensor data”).
- [ ] `python src/analytics/ml_training.py` exibe acurácia > 70% (se necessário, deixe a simulação rodar mais tempo).
- [ ] README atualizado com instruções (link do vídeo será incluído após upload “não listado” no YouTube).

Pronto! Siga este guia para garantir que todos os requisitos do enunciado apareçam claramente no vídeo final.*** End Patch

