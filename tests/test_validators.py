import unittest
import sys
import os
import types

# Setup mock environment before imports
def setup_mock_environment():
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def warning(self, msg, *args, **kwargs): pass
    
    # Create mock core module
    if 'src.core' not in sys.modules:
        mock_core = types.ModuleType('src.core')
        mock_core.utils_validators_logger = MockLogger()
        sys.modules['src.core'] = mock_core

# Setup environment
setup_mock_environment()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.validators import Validators

class TestValidators(unittest.TestCase):
    """Test cases for input validators"""
    
    def test_validate_number(self):
        """Test number validation"""
        self.assertTrue(Validators.validate_number("123"))
        self.assertTrue(Validators.validate_number("0"))
        self.assertFalse(Validators.validate_number("abc"))
        self.assertFalse(Validators.validate_number("12.5"))
        self.assertFalse(Validators.validate_number("-10"))
        
        # Test with range
        self.assertTrue(Validators.validate_number("50", min_value=0, max_value=100))
        self.assertFalse(Validators.validate_number("150", min_value=0, max_value=100))
    
    def test_validate_decimal(self):
        """Test decimal validation"""
        self.assertTrue(Validators.validate_decimal("123"))
        self.assertTrue(Validators.validate_decimal("12.5"))
        self.assertTrue(Validators.validate_decimal("0.25"))
        self.assertFalse(Validators.validate_decimal("abc"))
        
        # Test decimal places
        self.assertTrue(Validators.validate_decimal("12.5", decimal_places=1))
        self.assertFalse(Validators.validate_decimal("12.555", decimal_places=2))
    
    def test_validate_name(self):
        """Test name validation"""
        self.assertTrue(Validators.validate_name("Remington 700"))
        self.assertTrue(Validators.validate_name("AK-47"))
        self.assertTrue(Validators.validate_name("Test.Name"))
        self.assertFalse(Validators.validate_name("Test@Name"))
        self.assertFalse(Validators.validate_name("Test#Name"))
        
        # Test length limits
        self.assertFalse(Validators.validate_name("", min_length=1))
        self.assertFalse(Validators.validate_name("A" * 101, max_length=100))
    
    def test_validate_caliber(self):
        """Test caliber validation"""
        self.assertTrue(Validators.validate_caliber("7.62 mm"))
        self.assertTrue(Validators.validate_caliber("7.62mm"))
        self.assertTrue(Validators.validate_caliber("0.308 in"))
        self.assertTrue(Validators.validate_caliber("9mm"))
        self.assertFalse(Validators.validate_caliber("7.62"))
        self.assertFalse(Validators.validate_caliber("7.62 cm"))

if __name__ == '__main__':
    unittest.main()
