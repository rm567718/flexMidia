import time
import random
import sys
import os

# Add src to path to import db_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import log_interaction, init_db

import argparse

def simulate_sensors(duration=None):
    """Simulates random sensor events."""
    print(f"Starting Sensor Simulation... {'Running for ' + str(duration) + 's' if duration else 'Press Ctrl+C to stop.'}")
    init_db()
    
    sensor_types = ['touch', 'presence', 'voice_command']
    start_time = time.time()
    
    try:
        while True:
            # Check duration
            if duration and (time.time() - start_time > duration):
                print("\nSimulation finished (time limit reached).")
                break

            # Randomly pick a sensor event
            sensor = random.choice(sensor_types)
            
            if sensor == 'touch':
                # Simulate touch coordinates or button ID
                value = f"x:{random.randint(0, 1920)},y:{random.randint(0, 1080)}"
                duration_event = random.uniform(0.1, 2.0) # Short vs Long touch
            elif sensor == 'presence':
                # Simulate distance or person count
                value = f"distance:{random.randint(50, 300)}cm"
                duration_event = random.uniform(1.0, 10.0) # Dwell time
            elif sensor == 'voice_command':
                commands = ['mapa', 'lojas', 'banheiro', 'promoções']
                value = random.choice(commands)
                duration_event = random.uniform(1.0, 3.0)
            
            log_interaction(sensor, value, duration_event)
            print(f"[{int(time.time() - start_time)}s] Event: {sensor} | Value: {value}")
            
            # Wait a random time before next event
            time.sleep(random.uniform(0.5, 3.0))
            
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, help="Duration in seconds to run the simulation", default=None)
    args = parser.parse_args()
    
    simulate_sensors(args.duration)
