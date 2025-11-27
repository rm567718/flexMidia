@echo off
REM Script para rodar o demo do Totem Flexmedia em Windows (.bat)
cd /d %~dp0

echo Iniciando simulacao de sensores (60s)...
start /min "" python src\sensors\simulation.py --duration 60

set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
echo Abrindo dashboard Streamlit...
python -m streamlit run src\dashboard\app.py --server.headless true

