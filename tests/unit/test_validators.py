"""
Unit tests for the validators module
"""

import unittest
from tests import setup_test_environment
setup_test_environment()

from src.utils.validators import Validators

class TestValidators(unittest.TestCase):
    """Test cases for Validators class"""
    
    def test_validate_number_valid(self):
        """Test validate_number with valid inputs"""
        self.assertTrue(Validators.validate_number("123"))
        self.assertTrue(Validators.validate_number("0"))
        self.assertTrue(Validators.validate_number("-123"))
        self.assertTrue(Validators.validate_number("+456"))
    
    def test_validate_number_invalid(self):
        """Test validate_number with invalid inputs"""
        self.assertFalse(Validators.validate_number("abc"))
        self.assertFalse(Validators.validate_number("12.3"))
        self.assertFalse(Validators.validate_number(""))
        self.assertFalse(Validators.validate_number(" "))
        self.assertFalse(Validators.validate_number("12a3"))
    
    def test_validate_decimal_valid(self):
        """Test validate_decimal with valid inputs"""
        self.assertTrue(Validators.validate_decimal("123"))
        self.assertTrue(Validators.validate_decimal("12.3"))
        self.assertTrue(Validators.validate_decimal("0.5"))
        self.assertTrue(Validators.validate_decimal("-12.3"))
        self.assertTrue(Validators.validate_decimal("+45.6"))
    
    def test_validate_decimal_invalid(self):
        """Test validate_decimal with invalid inputs"""
        self.assertFalse(Validators.validate_decimal("abc"))
        self.assertFalse(Validators.validate_decimal(""))
        self.assertFalse(Validators.validate_decimal("12.3.4"))
        self.assertFalse(Validators.validate_decimal("12a.3"))
    
    def test_validate_name_valid(self):
        """Test validate_name with valid inputs"""
        self.assertTrue(Validators.validate_name("Remington 700"))
        self.assertTrue(Validators.validate_name("Federal Match"))
        self.assertTrue(Validators.validate_name("M24"))
        self.assertTrue(Validators.validate_name("Test-Name_123"))
    
    def test_validate_name_invalid(self):
        """Test validate_name with invalid inputs"""
        self.assertFalse(Validators.validate_name(""))
        self.assertFalse(Validators.validate_name("   "))
        self.assertFalse(Validators.validate_name("a" * 101))  # Too long
        self.assertFalse(Validators.validate_name("Name@#$"))  # Invalid chars
    
    def test_validate_caliber_valid(self):
        """Test validate_caliber with valid inputs"""
        self.assertTrue(Validators.validate_caliber("7.62 mm"))
        self.assertTrue(Validators.validate_caliber("0.308 in"))
        self.assertTrue(Validators.validate_caliber("9 mm"))
        self.assertTrue(Validators.validate_caliber("0.22 in"))
    
    def test_validate_caliber_invalid(self):
        """Test validate_caliber with invalid inputs"""
        self.assertFalse(Validators.validate_caliber("invalid"))
        self.assertFalse(Validators.validate_caliber("7.62"))
        self.assertFalse(Validators.validate_caliber("mm 7.62"))
        self.assertFalse(Validators.validate_caliber("7.62 cm"))

if __name__ == '__main__':
    unittest.main()
