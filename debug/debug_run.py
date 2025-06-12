#!/usr/bin/env python3
"""
Debug Application Runner

Starts the riflescope calculator with enhanced debugging and error reporting.
This version provides detailed error information without hiding exceptions.

Usage: python debug/debug_run.py [--verbose] [--no-gui]
"""

import sys
import os

# Add project paths
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

def setup_debug_environment():
    """Setup debugging environment"""
    # Enable debug logging
    os.environ['DEBUG'] = '1'
    
    # Add verbose error reporting
    import traceback
    sys.tracebacklimit = None  # Show full traceback

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = ['tkinter', 'sqlite3', 'os', 'logging', 'typing']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            missing.append(module)
            print(f"❌ {module}")
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        return False
    
    print("✓ All dependencies available")
    return True

def check_project_structure():
    """Check if project structure follows best practices"""
    print("\n🏗️ Checking project structure...")
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Modern Python project structure
    expected_structure = {
        'src/': ['__init__.py', 'main.py'],
        'src/config/': ['__init__.py'],
        'src/core/': ['__init__.py', 'logger.py'],
        'src/database/': ['__init__.py'],
        'src/gui/': ['__init__.py'],
        'src/utils/': ['__init__.py'],
        'tests/': ['__init__.py', 'run_all_tests.py'],
        'tests/unit/': [],
        'tests/integration/': [],
        'tests/fixtures/': [],
        'tests/utils/': [],
        'debug/': ['diagnostic.py', 'debug_run.py'],
        'docs/': [],  # Recommended
        'scripts/': [],  # Recommended
    }
    
    professional_files = [
        'requirements.txt',
        'setup.py',
        '.gitignore',
        'LICENSE',
        'CHANGELOG.md'
    ]
    
    all_ok = True
    recommendations = []
    
    # Check directory structure
    for dir_path, required_files in expected_structure.items():
        full_path = os.path.join(project_root, dir_path)
        is_recommended = dir_path in ['docs/', 'scripts/']
        
        if os.path.exists(full_path):
            symbol = "✓"
            print(f"{symbol} {dir_path}")
            
            # Check required files in directory
            for file_name in required_files:
                file_path = os.path.join(full_path, file_name)
                if os.path.exists(file_path):
                    print(f"  ✓ {file_name}")
                else:
                    print(f"  ❌ {file_name} - Missing")
                    if not is_recommended:
                        all_ok = False
        else:
            if is_recommended:
                print(f"⚠️ {dir_path} - Recommended")
                recommendations.append(f"Create {dir_path} for documentation/scripts")
            else:
                print(f"❌ {dir_path} - Missing")
                all_ok = False
    
    # Check professional files
    print(f"\nProfessional project files:")
    for file_name in professional_files:
        file_path = os.path.join(project_root, file_name)
        if os.path.exists(file_path):
            print(f"✓ {file_name}")
        else:
            print(f"⚠️ {file_name} - Recommended")
            recommendations.append(f"Add {file_name} for professional standards")
    
    if recommendations:
        print(f"\n💡 Recommendations for improvement:")
        for rec in recommendations[:5]:  # Limit to top 5
            print(f"   • {rec}")
    
    return all_ok

def run_with_debug():
    """Run the application with debug mode enabled"""
    try:
        print("🚀 Starting Riflescope Calculator in Debug Mode")
        print("=" * 60)
        
        # Setup debug environment
        setup_debug_environment()
        
        # Check dependencies first
        if not check_dependencies():
            return False
        
        # Check project structure
        if not check_project_structure():
            print("\n⚠️ Project structure incomplete. Some features may not work.")
        
        # Import and run main
        from src.main import main
        
        print("\n🔧 Debug mode enabled - detailed logging active")
        print("📝 Logs will be written to logs/ directory")
        print("=" * 60)
        
        main()
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return True
    except Exception as e:
        print(f"\n💥 Application crashed with error: {e}")
        print("\n🔍 Full error details:")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Debug runner for Riflescope Calculator")
    parser.add_argument("--verbose", "-v", action="store_true", help="Extra verbose output")
    parser.add_argument("--no-gui", action="store_true", help="Skip GUI startup (import test only)")
    
    args = parser.parse_args()
    
    if args.verbose:
        print("🔊 Verbose mode enabled")
    
    if args.no_gui:
        print("🚫 GUI disabled - testing imports only")
        # Test imports without starting GUI
        try:
            setup_debug_environment()
            from src import config, utils, database
            print("✓ All core modules imported successfully")
            return True
        except Exception as e:
            print(f"❌ Import test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    success = run_with_debug()
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("   1. Run standalone tests: python debug/standalone_tests.py")
        print("   2. Check logs in logs/ directory")
        print("   3. Try: python debug/debug_run.py --no-gui")
        print("   4. Verify Python version: python --version")
        print("   5. Run system diagnostic: python debug/diagnostic.py")
    
    input("\nPress Enter to exit...")
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
