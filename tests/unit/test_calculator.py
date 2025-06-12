"""
Unit tests for the calculator module
"""

import unittest
import sys
import os

# Ensure test environment is set up
from tests import setup_test_environment
setup_test_environment()

from src.utils.calculator import ClickCalculator, CalculationError

class TestClickCalculator(unittest.TestCase):
    """Test cases for ClickCalculator class"""
    
    def test_calculate_clicks_up(self):
        """Test calculation when target is higher than current"""
        clicks, direction = ClickCalculator.calculate_clicks(10, 25)
        self.assertEqual(clicks, 15)
        self.assertEqual(direction, 'up')
    
    def test_calculate_clicks_down(self):
        """Test calculation when target is lower than current"""
        clicks, direction = ClickCalculator.calculate_clicks(25, 10)
        self.assertEqual(clicks, 15)
        self.assertEqual(direction, 'down')
    
    def test_calculate_clicks_same_position(self):
        """Test calculation when current equals target"""
        clicks, direction = ClickCalculator.calculate_clicks(15, 15)
        self.assertEqual(clicks, 0)
        self.assertIsNone(direction)
    
    def test_calculate_clicks_negative_numbers(self):
        """Test calculation with negative numbers"""
        clicks, direction = ClickCalculator.calculate_clicks(-10, 5)
        self.assertEqual(clicks, 15)
        self.assertEqual(direction, 'up')
        
        clicks, direction = ClickCalculator.calculate_clicks(5, -10)
        self.assertEqual(clicks, 15)
        self.assertEqual(direction, 'down')
    
    def test_calculate_clicks_zero_values(self):
        """Test calculation with zero values"""
        clicks, direction = ClickCalculator.calculate_clicks(0, 10)
        self.assertEqual(clicks, 10)
        self.assertEqual(direction, 'up')
        
        clicks, direction = ClickCalculator.calculate_clicks(10, 0)
        self.assertEqual(clicks, 10)
        self.assertEqual(direction, 'down')
    
    def test_calculate_clicks_invalid_types(self):
        """Test calculation with invalid input types"""
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks("abc", 10)
        
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks(10, "xyz")
        
        with self.assertRaises(CalculationError):
            ClickCalculator.calculate_clicks(None, 10)

if __name__ == '__main__':
    unittest.main()
