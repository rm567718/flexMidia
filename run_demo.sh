#!/usr/bin/env bash
# Script para rodar o demo do Totem Flexmedia em ambientes Unix-like.

set -euo pipefail
cd "$(dirname "$0")"

echo "Iniciando simulacao de sensores (60s)..."
python3 src/sensors/simulation.py --duration 60 &
SIM_PID=$!

export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
echo "Abrindo dashboard Streamlit..."
python3 -m streamlit run src/dashboard/app.py --server.headless true

echo "Encerrando simulacao..."
kill $SIM_PID 2>/dev/null || true

