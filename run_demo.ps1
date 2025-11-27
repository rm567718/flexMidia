# Script to run the Flexmedia Totem Demo
Write-Host "Starting Flexmedia Totem Demo..." -ForegroundColor Green

# Start the simulation in a new window (runs for 60 seconds / 1 min)
Start-Process python -ArgumentList "src/sensors/simulation.py --duration 60" -WindowStyle Minimized
Write-Host "Sensor Simulation started (background, 60s duration)..." -ForegroundColor Yellow

# Start the dashboard usando python -m streamlit (garante PATH correto)
$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"
Write-Host "Starting Dashboard..." -ForegroundColor Cyan
python -m streamlit run src/dashboard/app.py --server.headless true
