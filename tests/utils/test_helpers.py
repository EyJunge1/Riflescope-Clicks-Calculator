"""
Test helper functions and utilities
"""

import os
import sys
import tempfile
import shutil
from contextlib import contextmanager
import sqlite3

def create_temp_database():
    """Create a temporary SQLite database for testing"""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")
    return db_path, temp_dir

def cleanup_temp_database(temp_dir):
    """Clean up temporary database"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@contextmanager
def temporary_database():
    """Context manager for temporary database"""
    db_path, temp_dir = create_temp_database()
    try:
        yield db_path
    finally:
        cleanup_temp_database(temp_dir)

def assert_calculation_result(test_case, current, target, expected_clicks, expected_direction):
    """Helper to assert calculation results"""
    from src.utils.calculator import ClickCalculator
    
    clicks, direction = ClickCalculator.calculate_clicks(current, target)
    test_case.assertEqual(clicks, expected_clicks, 
                         f"Expected {expected_clicks} clicks, got {clicks}")
    test_case.assertEqual(direction, expected_direction,
                         f"Expected direction {expected_direction}, got {direction}")

def setup_test_database(db_path):
    """Set up a test database with sample data"""
    from tests.fixtures.sample_data import SAMPLE_WEAPONS, SAMPLE_AMMUNITION, SAMPLE_DISTANCES
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables (simplified schema for testing)
    cursor.execute('''
        CREATE TABLE weapons (
            id INTEGER PRIMARY KEY,
            weapon TEXT NOT NULL,
            caliber TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE ammunition (
            id INTEGER PRIMARY KEY,
            ammunition TEXT NOT NULL,
            caliber TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE distances (
            id INTEGER PRIMARY KEY,
            distance TEXT NOT NULL,
            unit TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    for weapon in SAMPLE_WEAPONS:
        cursor.execute(
            "INSERT INTO weapons (weapon, caliber) VALUES (?, ?)",
            (weapon["weapon"], weapon["caliber"])
        )
    
    for ammo in SAMPLE_AMMUNITION:
        cursor.execute(
            "INSERT INTO ammunition (ammunition, caliber) VALUES (?, ?)",
            (ammo["ammunition"], ammo["caliber"])
        )
    
    for distance in SAMPLE_DISTANCES:
        cursor.execute(
            "INSERT INTO distances (distance, unit) VALUES (?, ?)",
            (distance["distance"], distance["unit"])
        )
    
    conn.commit()
    conn.close()

class TestOutputCapture:
    """Utility class to capture print output during tests"""
    
    def __init__(self):
        self.output = []
    
    def write(self, text):
        self.output.append(text)
    
    def flush(self):
        pass
    
    def get_output(self):
        return ''.join(self.output)
