#!/usr/bin/env python3
"""
System Diagnostic Tool

Performs comprehensive system checks for the riflescope calculator application.
Use this to diagnose environment issues and compatibility problems.

Usage: python debug/diagnostic.py
"""

import sys
import os
import platform
import sqlite3

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Python Version Check")
    print("-" * 30)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python Version: {version_str}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    else:
        print("✓ Python version compatible")
        return True

def check_modules():
    """Check required Python modules"""
    print("\n📦 Module Availability Check")
    print("-" * 30)
    
    modules = {
        'tkinter': 'GUI framework',
        'sqlite3': 'Database support', 
        'os': 'Operating system interface',
        'logging': 'Logging framework',
        'typing': 'Type hints support'
    }
    
    all_available = True
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"✓ {module:12} - {description}")
        except ImportError as e:
            print(f"❌ {module:12} - {description} (ERROR: {e})")
            all_available = False
    
    return all_available

def check_tkinter_detailed():
    """Detailed tkinter check"""
    print("\n🖼️ GUI Framework Check")
    print("-" * 30)
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
        
        # Test basic window creation
        root = tk.Tk()
        root.withdraw()  # Hide window
        print("✓ Basic window creation works")
        
        # Test ttk
        from tkinter import ttk
        print("✓ ttk (themed widgets) available")
        
        # Test messagebox
        from tkinter import messagebox
        print("✓ messagebox available")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ tkinter error: {e}")
        return False

def check_sqlite():
    """Check SQLite functionality"""
    print("\n🗄️ Database Check")
    print("-" * 30)
    
    try:
        # Check SQLite version
        print(f"SQLite Version: {sqlite3.sqlite_version}")
        
        # Test in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
        cursor.execute('INSERT INTO test (name) VALUES (?)', ('test_entry',))
        
        result = cursor.fetchone()
        conn.close()
        
        print("✓ SQLite operations working")
        return True
        
    except Exception as e:
        print(f"❌ SQLite error: {e}")
        return False

def check_file_permissions():
    """Check file system permissions"""
    print("\n📁 File System Check")
    print("-" * 30)
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Test directories that need to be created
    test_dirs = ['database', 'logs', 'icons']
    
    all_ok = True
    
    for test_dir in test_dirs:
        full_path = os.path.join(project_root, test_dir)
        
        try:
            # Try to create directory
            os.makedirs(full_path, exist_ok=True)
            
            # Try to create a test file
            test_file = os.path.join(full_path, 'test_write.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            
            # Clean up
            os.remove(test_file)
            
            print(f"✓ {test_dir:10} - Read/Write OK")
            
        except PermissionError:
            print(f"❌ {test_dir:10} - Permission denied")
            all_ok = False
        except Exception as e:
            print(f"❌ {test_dir:10} - Error: {e}")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Check project file structure with improved organization"""
    print("\n🏗️ Project Structure Check")
    print("-" * 30)
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Essential application structure
    required_structure = {
        'src': {
            'files': ['__init__.py', 'main.py'],
            'dirs': ['config', 'core', 'database', 'gui', 'utils']
        },
        'tests': {
            'files': ['__init__.py', 'run_all_tests.py'],
            'dirs': ['unit', 'integration', 'fixtures', 'utils']
        },
        'debug': {
            'files': ['diagnostic.py', 'debug_run.py', 'standalone_tests.py'],
            'dirs': []
        }
    }
    
    # Recommended professional structure
    recommended_structure = {
        'docs': {
            'files': ['README.md'],
            'dirs': []
        },
        'scripts': {
            'files': [],
            'dirs': []
        }
    }
    
    # Root files
    root_files = {
        'essential': ['run.py', 'README.md'],
        'recommended': ['requirements.txt', 'setup.py', '.gitignore', 'LICENSE']
    }
    
    all_ok = True
    
    # Check essential structure
    print("Essential structure:")
    for main_dir, contents in required_structure.items():
        main_path = os.path.join(project_root, main_dir)
        if os.path.exists(main_path):
            print(f"✓ {main_dir}/")
            
            # Check required files
            for file_name in contents['files']:
                file_path = os.path.join(main_path, file_name)
                if os.path.exists(file_path):
                    print(f"  ✓ {main_dir}/{file_name}")
                else:
                    print(f"  ❌ {main_dir}/{file_name} - Missing")
                    all_ok = False
            
            # Check required subdirectories
            for subdir in contents['dirs']:
                sub_path = os.path.join(main_path, subdir)
                if os.path.exists(sub_path):
                    print(f"  ✓ {main_dir}/{subdir}/")
                    
                    # Check for __init__.py in Python packages
                    if main_dir == 'src':
                        init_file = os.path.join(sub_path, '__init__.py')
                        if os.path.exists(init_file):
                            print(f"    ✓ {main_dir}/{subdir}/__init__.py")
                        else:
                            print(f"    ❌ {main_dir}/{subdir}/__init__.py - Missing")
                            all_ok = False
                else:
                    print(f"  ❌ {main_dir}/{subdir}/ - Missing")
                    all_ok = False
        else:
            print(f"❌ {main_dir}/ - Missing")
            all_ok = False
    
    # Check root files
    print(f"\nRoot files:")
    for file_name in root_files['essential']:
        file_path = os.path.join(project_root, file_name)
        if os.path.exists(file_path):
            print(f"✓ {file_name}")
        else:
            print(f"❌ {file_name} - Missing")
            all_ok = False
    
    print(f"\nRecommended files:")
    missing_recommended = []
    for file_name in root_files['recommended']:
        file_path = os.path.join(project_root, file_name)
        if os.path.exists(file_path):
            print(f"✓ {file_name}")
        else:
            print(f"⚠️ {file_name} - Recommended")
            missing_recommended.append(file_name)
    
    # Check recommended structure
    print(f"\nRecommended directories:")
    for main_dir, contents in recommended_structure.items():
        main_path = os.path.join(project_root, main_dir)
        if os.path.exists(main_path):
            print(f"✓ {main_dir}/")
        else:
            print(f"⚠️ {main_dir}/ - Recommended for professional projects")
    
    if missing_recommended:
        print(f"\n💡 To make your project more professional, consider adding:")
        for item in missing_recommended:
            if item == 'requirements.txt':
                print(f"   - {item}: Define Python dependencies")
            elif item == 'setup.py':
                print(f"   - {item}: Package installation script")
            elif item == '.gitignore':
                print(f"   - {item}: Git ignore patterns")
            elif item == 'LICENSE':
                print(f"   - {item}: License information")
    
    return all_ok

def run_import_test():
    """Test importing main application modules"""
    print("\n🔍 Import Test")
    print("-" * 30)
    
    # Add project to path
    project_root = os.path.dirname(os.path.dirname(__file__))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, project_root)
    sys.path.insert(0, src_path)
    
    # Setup mock loggers first
    from debug.standalone_tests import setup_mock_loggers
    setup_mock_loggers()
    
    modules_to_test = [
        ('src.config', 'Configuration'),
        ('src.utils.calculator', 'Calculator'),
        ('src.utils.validators', 'Validators'),
        ('src.database.connection', 'Database Connection'),
        ('src.gui.components', 'GUI Components')
    ]
    
    all_ok = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {description}")
        except Exception as e:
            print(f"❌ {description} - Error: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Run complete diagnostic"""
    print("🔧 Riflescope Calculator - System Diagnostic")
    print("=" * 60)
    print("This tool checks your system for compatibility issues.")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Modules", check_modules),
        ("GUI Framework", check_tkinter_detailed),
        ("Database Support", check_sqlite),
        ("File Permissions", check_file_permissions),
        ("Project Structure", check_project_structure),
        ("Import Test", run_import_test)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Diagnostic Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{check_name:20} {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 System is ready for the riflescope calculator!")
    else:
        print("\n⚠️ Issues detected. Please resolve the failed checks.")
        print("\n💡 Common solutions:")
        print("   - Run as administrator for permission issues")
        print("   - Install Python 3.7+ if version check failed")
        print("   - Install tkinter: apt-get install python3-tk (Linux)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
