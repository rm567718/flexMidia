# Flexmedia Totem IA – Sprint 2

Implementação da PoC que integra sensores (simulados), armazenamento SQL, dashboard em Python e um modelo supervisionado simples para classificar interações de toque (curto x longo). O objetivo é proporcionar uma base completa para gravar a demonstração solicitada no Challenge Flexmedia.

## Estrutura

- `src/sensors`: simulador de eventos físicos (toque, presença, voz).
- `src/database`: operações CRUD sobre o banco SQLite (`data/totem.db`).
- `src/dashboard`: dashboard Streamlit com métricas em tempo real e insights de ML.
- `src/analytics`: utilitários de limpeza/engenharia de dados e script de treinamento.
- `docs`: contexto, arquitetura, estratégia de dados/LLM e **guia de vídeo** (`docs/10-guia-demo.md`).

## Setup rápido

```powershell
cd C:\fiap\Projetos\flexMideaSprint2\flexmedia-totem-ia
pip install --user -r requirements.txt
```

Se o PowerShell bloquear scripts, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Executar a demonstração completa

```powershell
cd C:\fiap\Projetos\flexMideaSprint2\flexmedia-totem-ia
.\run_demo.ps1
```

O script:

1. Inicia a simulação de sensores por 60 s.
2. Abre o dashboard Streamlit em `http://localhost:8501` (headless, sem prompts).

Use o navegador para capturar as métricas, gráficos e a seção “ML Insights” durante o vídeo.

## Pipeline analítico e modelo supervisionado

Após coletar alguns minutos de dados:

```powershell
python src/analytics/ml_training.py
```

O script:

- Limpa e padroniza os registros (remoção de duplicatas, normalização de duração/coordenadas).
- Treina um `LogisticRegression` para prever toques curtos x longos.
- Salva artefatos em `artifacts/` e imprime a acurácia + relatório de classes.

Para reaproveitar os resultados (sem retreinar):

```powershell
python src/analytics/ml_training.py --show-last
```

## Documentação complementar

- Arquitetura Sprint 2: `docs/09-arquitetura-sprint2.md`
- Estratégia de coleta de dados: `docs/07-estrategia-coleta-de-dados.md`
- Estratégia LLM e integrações futuras: `docs/08-llm-estrategia.md`

Cole aqui assim que a gravação (não listada no YouTube) estiver pronta.
