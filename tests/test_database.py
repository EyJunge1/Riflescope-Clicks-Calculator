import unittest
import tempfile
import os
import sys
import types
import time

# Setup mock environment before imports
def setup_mock_environment():
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
    
    # Create mock core module
    if 'src.core' not in sys.modules:
        mock_core = types.ModuleType('src.core')
        mock_logger = MockLogger()
        mock_core.db_connection_logger = mock_logger
        mock_core.db_manager_logger = mock_logger
        mock_core.db_entities_logger = mock_logger
        sys.modules['src.core'] = mock_core

# Setup environment
setup_mock_environment()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.database.manager import DatabaseManager
from src.database.connection import Database

class TestDatabase(unittest.TestCase):
    """Test cases for database functionality"""
    
    def setUp(self):
        """Create temporary database for testing"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db_manager = DatabaseManager(self.db_path)
        self.db_manager.initialize_database()
    
    def tearDown(self):
        """Clean up temporary database with proper connection handling"""
        # Ensure database manager is properly closed
        if hasattr(self.db_manager, 'db') and self.db_manager.db:
            if hasattr(self.db_manager.db, 'db_connection') and self.db_manager.db.db_connection:
                try:
                    self.db_manager.db.db_close()
                except:
                    pass
        
        # Give Windows a moment to release file handles
        time.sleep(0.1)
        
        # Attempt to delete the file with retry logic
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                if os.path.exists(self.db_path):
                    os.unlink(self.db_path)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(0.2)  # Wait longer between attempts
                else:
                    # If we still can't delete after all attempts, just pass
                    # The temp file will be cleaned up eventually by the OS
                    pass
    
    def test_add_weapon(self):
        """Test adding weapons"""
        weapon_id = self.db_manager.add_weapon("Test Rifle", "7.62 mm")
        self.assertIsNotNone(weapon_id)
        
        weapons = self.db_manager.get_weapons()
        self.assertEqual(len(weapons), 1)
        self.assertEqual(weapons[0][1], "Test Rifle")
        self.assertEqual(weapons[0][2], "7.62 mm")
        
        # Explicitly close connection after test
        self._close_database_connections()
    
    def test_add_ammunition(self):
        """Test adding ammunition"""
        ammo_id = self.db_manager.add_ammunition("Test Ammo", "7.62 mm")
        self.assertIsNotNone(ammo_id)
        
        ammunition = self.db_manager.get_ammunition()
        self.assertEqual(len(ammunition), 1)
        self.assertEqual(ammunition[0][1], "Test Ammo")
        
        # Explicitly close connection after test
        self._close_database_connections()
    
    def test_add_distance(self):
        """Test adding distances"""
        distance_id = self.db_manager.add_distance("100", "m")
        self.assertIsNotNone(distance_id)
        
        distances = self.db_manager.get_distances()
        self.assertEqual(len(distances), 1)
        self.assertEqual(distances[0][1], "100")
        self.assertEqual(distances[0][2], "m")
        
        # Explicitly close connection after test
        self._close_database_connections()
    
    def test_add_result(self):
        """Test adding results"""
        # First add required data
        self.db_manager.add_weapon("Test Rifle", "7.62 mm")
        self.db_manager.add_ammunition("Test Ammo", "7.62 mm")
        self.db_manager.add_distance("100", "m")
        
        # Add result
        result_id = self.db_manager.add_result("Test Rifle", "Test Ammo", "100m", "25")
        self.assertIsNotNone(result_id)
        
        # Verify result
        result = self.db_manager.get_result_by_weapon_ammo_distance("Test Rifle", "Test Ammo", "100m")
        self.assertIsNotNone(result)
        self.assertEqual(result[5], "25")
        
        # Explicitly close connection after test
        self._close_database_connections()
    
    def test_caliber_matching(self):
        """Test that ammunition matches weapon caliber"""
        # Add weapon and matching ammo
        self.db_manager.add_weapon("Test Rifle", "7.62 mm")
        self.db_manager.add_ammunition("Matching Ammo", "7.62 mm")
        self.db_manager.add_ammunition("Different Ammo", "9 mm")
        
        # Get matching ammunition
        matching = self.db_manager.get_ammunition_by_caliber("7.62 mm")
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0][1], "Matching Ammo")
        
        # Explicitly close connection after test
        self._close_database_connections()
    
    def _close_database_connections(self):
        """Helper method to explicitly close database connections"""
        try:
            if hasattr(self.db_manager, 'db') and self.db_manager.db:
                if hasattr(self.db_manager.db, 'db_connection') and self.db_manager.db.db_connection:
                    self.db_manager.db.db_close()
        except:
            pass

if __name__ == '__main__':
    unittest.main()
