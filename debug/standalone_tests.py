#!/usr/bin/env python3
"""
Standalone Component Tests

This script tests individual components WITHOUT starting the GUI.
Use this to verify that core functionality works correctly.

Usage: python debug/standalone_tests.py
"""

import sys
import os

# Add project paths
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

def setup_mock_loggers():
    """Setup comprehensive mock loggers"""
    import types
    
    # Create mock logger class
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def warning(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
        def critical(self, msg, *args, **kwargs): pass
        def exception(self, msg, *args, **kwargs): pass
    
    # Create mock core module with all required loggers
    mock_core = types.ModuleType('src.core')
    mock_logger = MockLogger()
    
    # Add all known loggers from logger.py
    logger_names = [
        'main_logger', 'calc_logger', 'db_logger', 'gui_logger',
        'config_logger', 'utils_logger', 'models_logger',
        'db_connection_logger', 'db_manager_logger', 'db_entities_logger',
        'gui_main_logger', 'gui_settings_logger', 'gui_components_logger',
        'utils_calc_logger', 'utils_validators_logger'
    ]
    
    for logger_name in logger_names:
        setattr(mock_core, logger_name, mock_logger)
    
    sys.modules['src.core'] = mock_core
    return mock_core

def test_imports():
    """Test if basic imports work"""
    print("🔍 Testing basic imports...")
    
    try:
        setup_mock_loggers()
        print("✓ Mock loggers created")
        
        from src.utils.calculator import ClickCalculator, CalculationError
        print("✓ Calculator import successful")
        
        from src.utils.validators import Validators
        print("✓ Validators import successful")
        
        from src.config import AppSettings
        print("✓ Config import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calculator_basic():
    """Test basic calculator functionality"""
    print("\n🧮 Testing calculator...")
    
    try:
        setup_mock_loggers()
        
        from src.utils.calculator import ClickCalculator
        
        test_cases = [
            (10, 25, 15, 'up'),
            (25, 10, 15, 'down'),
            (15, 15, 0, None),
            (0, 10, 10, 'up'),
            (-5, 5, 10, 'up')
        ]
        
        for current, target, expected_clicks, expected_direction in test_cases:
            clicks, direction = ClickCalculator.calculate_clicks(current, target)
            assert clicks == expected_clicks, f"Expected {expected_clicks}, got {clicks}"
            assert direction == expected_direction, f"Expected {expected_direction}, got {direction}"
            print(f"✓ Test case ({current} → {target}): {clicks} clicks {direction}")
        
        return True
    except Exception as e:
        print(f"❌ Calculator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validators_basic():
    """Test basic validator functionality"""
    print("\n✅ Testing validators...")
    
    try:
        setup_mock_loggers()
        
        from src.utils.validators import Validators
        
        # Test number validation
        assert Validators.validate_number("123") == True
        assert Validators.validate_number("abc") == False
        print("✓ Number validation works")
        
        # Test decimal validation
        assert Validators.validate_decimal("12.3") == True
        assert Validators.validate_decimal("abc") == False
        print("✓ Decimal validation works")
        
        # Test name validation
        assert Validators.validate_name("Remington 700") == True
        assert Validators.validate_name("") == False
        print("✓ Name validation works")
        
        # Test caliber validation
        assert Validators.validate_caliber("7.62 mm") == True
        assert Validators.validate_caliber("invalid") == False
        print("✓ Caliber validation works")
        
        return True
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        setup_mock_loggers()
        
        from src.config import AppSettings
        
        # Test basic settings
        assert hasattr(AppSettings, 'APP_NAME')
        assert hasattr(AppSettings, 'MAIN_WINDOW_SIZE')
        print("✓ Basic settings available")
        
        # Test path methods
        project_root = AppSettings.get_project_root()
        assert isinstance(project_root, str)
        print(f"✓ Project root: {project_root}")
        
        db_dir = AppSettings.get_db_dir()
        assert isinstance(db_dir, str)
        print(f"✓ Database directory: {db_dir}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all standalone tests"""
    print("🧪 Standalone Component Tests")
    print("=" * 60)
    print("Testing individual components WITHOUT starting the GUI")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Calculator Test", test_calculator_basic),
        ("Validator Test", test_validators_basic),
        ("Config Test", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All standalone tests passed!")
        print("\n💡 Components are working correctly.")
        print("   You can now run the full application with:")
        print("   python run.py")
        return True
    else:
        print("⚠️  Some tests failed")
        print("\n💡 Fix the failing components before running the full application")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("STANDALONE COMPONENT TESTING")
    print("=" * 60)
    success = main()
    print("\n" + "=" * 60)
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
