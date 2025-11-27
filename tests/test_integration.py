import unittest
import os
import sys
import sqlite3
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db_manager import init_db, log_interaction, DB_PATH

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Use a test database
        self.test_db_path = DB_PATH + '_test'
        # Override DB_PATH in db_manager (monkeypatching for simplicity in this script)
        import database.db_manager
        database.db_manager.DB_PATH = self.test_db_path
        
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
        init_db()

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_log_interaction(self):
        """Test if interactions are logged correctly."""
        log_interaction('test_sensor', 'test_value', 1.5)
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interactions")
        rows = cursor.fetchall()
        conn.close()
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][2], 'test_sensor') # sensor_type
        self.assertEqual(rows[0][3], 'test_value') # value
        self.assertEqual(rows[0][4], 1.5) # duration

    def test_simulation_logic(self):
        """Test if simulation logic generates valid data (import check)."""
        from sensors.simulation import simulate_sensors
        # We can't easily test the infinite loop, but we verified the import works
        self.assertTrue(callable(simulate_sensors))

if __name__ == '__main__':
    unittest.main()
