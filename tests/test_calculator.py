import unittest
import sys
import os
import types

# Setup mock environment before imports
def setup_mock_environment():
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
    
    # Create mock core module
    if 'src.core' not in sys.modules:
        mock_core = types.ModuleType('src.core')
        mock_core.utils_calc_logger = MockLogger()
        sys.modules['src.core'] = mock_core

# Setup environment
setup_mock_environment()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.calculator import ClickCalculator, CalculationError

class TestClickCalculator(unittest.TestCase):
    """Test cases for ClickCalculator"""
    
    def test_calculate_clicks_basic(self):
        """Test basic click calculation"""
        clicks, direction = ClickCalculator.calculate_clicks(10, 20)
        self.assertEqual(clicks, 10)
        self.assertEqual(direction, 'up')
        
        clicks, direction = ClickCalculator.calculate_clicks(20, 10)
        self.assertEqual(clicks, 10)
        self.assertEqual(direction, 'down')
        
        clicks, direction = ClickCalculator.calculate_clicks(15, 15)
        self.assertEqual(clicks, 0)
        self.assertIsNone(direction)
    
    def test_calculate_clicks_string_input(self):
        """Test with string inputs"""
        clicks, direction = ClickCalculator.calculate_clicks("10", "25")
        self.assertEqual(clicks, 15)
        self.assertEqual(direction, 'up')
    
    def test_calculate_clicks_invalid_input(self):
        """Test with invalid inputs"""
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks("abc", "10")
        
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks("10", "xyz")
    
    def test_calculate_clicks_range_validation(self):
        """Test range validation"""
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks(-2000, 10)
        
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks(10, 2000)
    
    def test_moa_calculation(self):
        """Test MOA calculation"""
        moa = ClickCalculator.calculate_moa_adjustment(100, 2.908)
        self.assertAlmostEqual(moa, 1.0, places=1)
        
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_moa_adjustment(0, 10)

if __name__ == '__main__':
    unittest.main()
