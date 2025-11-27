# Script to run the Flexmedia Totem Demo
Write-Host "Starting Flexmedia Totem Demo..." -ForegroundColor Green

# Start the simulation in a new window (runs for 60 seconds / 1 min)
Start-Process python -ArgumentList "src/sensors/simulation.py --duration 60" -WindowStyle Minimized
Write-Host "Sensor Simulation started (background, 60s duration)..." -ForegroundColor Yellow

# Start the dashboard
Write-Host "Starting Dashboard..." -ForegroundColor Cyan
streamlit run src/dashboard/app.py
