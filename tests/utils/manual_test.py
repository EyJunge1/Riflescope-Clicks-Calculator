#!/usr/bin/env python3
"""
Manual testing script for individual components
Moved from main directory to tests/utils/
"""

import sys
import os
import tempfile
import types

# Add src to path (adjust for new location)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

def setup_mock_loggers():
    """Setup mock loggers to avoid import errors"""
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def warning(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
        def critical(self, msg, *args, **kwargs): pass
        def exception(self, msg, *args, **kwargs): pass
    
    # Create mock core module
    if 'src.core' not in sys.modules:
        mock_core = types.ModuleType('src.core')
        mock_logger = MockLogger()
        
        # Add all logger instances from the actual logger.py
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

def test_calculator():
    """Test calculator functionality"""
    print("🧮 Testing Calculator...")
    
    try:
        setup_mock_loggers()
        from src.utils.calculator import ClickCalculator
        
        # Test basic calculation
        clicks, direction = ClickCalculator.calculate_clicks(10, 25)
        print(f"✅ Basic calculation: {clicks} clicks {direction}")
        assert clicks == 15
        assert direction == 'up'
        
        # Test reverse calculation
        clicks, direction = ClickCalculator.calculate_clicks(25, 10)
        print(f"✅ Reverse calculation: {clicks} clicks {direction}")
        assert clicks == 15
        assert direction == 'down'
        
        # Test MOA calculation
        moa = ClickCalculator.calculate_moa_adjustment(100, 2.908)
        print(f"✅ MOA calculation: {moa} MOA")
        assert abs(moa - 1.0) < 0.1  # Should be approximately 1.0
        
        return True
    except Exception as e:
        print(f"❌ Calculator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validators():
    """Test validator functionality"""
    print("\n✅ Testing Validators...")
    
    try:
        setup_mock_loggers()
        from src.utils.validators import Validators
        
        # Test number validation
        assert Validators.validate_number("123") == True
        assert Validators.validate_number("abc") == False
        print("✅ Number validation works")
        
        # Test decimal validation
        assert Validators.validate_decimal("12.5") == True
        assert Validators.validate_decimal("abc") == False
        print("✅ Decimal validation works")
        
        # Test name validation
        assert Validators.validate_name("Test Rifle") == True
        assert Validators.validate_name("Test@Rifle") == False
        print("✅ Name validation works")
        
        # Test caliber validation
        assert Validators.validate_caliber("7.62 mm") == True
        assert Validators.validate_caliber("invalid") == False
        print("✅ Caliber validation works")
        
        return True
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing Database...")
    
    try:
        setup_mock_loggers()
        from src.database.manager import DatabaseManager
        
        # Create temporary database
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        db_manager = DatabaseManager(temp_db.name)
        db_manager.initialize_database()
        
        # Test adding weapon
        weapon_id = db_manager.add_weapon("Test Rifle", "7.62 mm")
        print(f"✅ Added weapon with ID: {weapon_id}")
        
        # Test adding ammunition
        ammo_id = db_manager.add_ammunition("Test Ammo", "7.62 mm")
        print(f"✅ Added ammunition with ID: {ammo_id}")
        
        # Test adding distance
        distance_id = db_manager.add_distance("100", "m")
        print(f"✅ Added distance with ID: {distance_id}")
        
        # Test getting weapons
        weapons = db_manager.get_weapons()
        print(f"✅ Retrieved {len(weapons)} weapons")
        
        # Test getting ammunition
        ammunition = db_manager.get_ammunition()
        print(f"✅ Retrieved {len(ammunition)} ammunition types")
        
        # Test getting distances
        distances = db_manager.get_distances()
        print(f"✅ Retrieved {len(distances)} distances")
        
        # Cleanup
        os.unlink(temp_db.name)
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_components():
    """Test GUI components (without displaying)"""
    print("\n🖥️ Testing GUI Components...")
    
    try:
        import tkinter as tk
        setup_mock_loggers()
        from src.gui.components import BaseGUIComponent
        
        # Test basic component creation
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        component = BaseGUIComponent(root)
        print("✅ BaseGUIComponent created successfully")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from src.config.settings import AppSettings
        
        # Test basic settings
        assert AppSettings.APP_NAME is not None
        print(f"✅ App name: {AppSettings.APP_NAME}")
        
        assert AppSettings.MAIN_WINDOW_SIZE is not None
        print(f"✅ Window size: {AppSettings.MAIN_WINDOW_SIZE}")
        
        # Test path methods
        app_dir = AppSettings.get_app_dir()
        assert app_dir is not None
        print(f"✅ App directory: {app_dir}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all manual tests"""
    print("🧪 Manual Component Testing (tests/utils/)")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Calculator", test_calculator),
        ("Validators", test_validators),
        ("Database", test_database),
        ("GUI Components", test_gui_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All manual tests passed!")
    else:
        print("⚠️ Some tests failed - check individual components")

if __name__ == "__main__":
    main()