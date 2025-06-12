#!/usr/bin/env python3
"""
Quick test script that bypasses import issues
Moved from main directory to tests/utils/
"""

import sys
import os
import types

# Setup paths (adjust for new location)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Create mock logger module
class MockLogger:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

# Mock the core module completely
mock_core = types.ModuleType('core')
logger_names = [
    'main_logger', 'calc_logger', 'db_logger', 'gui_logger',
    'config_logger', 'utils_logger', 'models_logger',
    'utils_calc_logger', 'utils_validators_logger', 'db_connection_logger', 
    'db_manager_logger', 'db_entities_logger', 'gui_main_logger'
]

for logger_name in logger_names:
    setattr(mock_core, logger_name, MockLogger())

sys.modules['core'] = mock_core
sys.modules['src.core'] = mock_core

def test_basic_functionality():
    """Test basic functionality without GUI"""
    print("🔧 Quick Test - Basic Functionality (tests/utils/)")
    print("=" * 50)
    
    try:
        # Test calculator
        from src.utils.calculator import ClickCalculator
        clicks, direction = ClickCalculator.calculate_clicks(10, 25)
        print(f"✅ Calculator: {clicks} clicks {direction}")
        
        # Test validators
        from src.utils.validators import Validators
        valid = Validators.validate_number("123")
        print(f"✅ Validator: Number validation = {valid}")
        
        # Test config
        from src.config.settings import AppSettings
        print(f"✅ Config: App name = {AppSettings.APP_NAME}")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
