#!/usr/bin/env python3
"""
Test Dispatcher - moved to tests directory

This file acts as a dispatcher to the organized test structure.
All actual test functionality is in the tests/ and debug/ directories.
"""

import sys
import os
import subprocess

def show_help():
    """Show available test commands"""
    print("🧪 Riflescope Calculator - Test Command Dispatcher")
    print("=" * 60)
    print("All tests are now organized in separate directories:")
    print()
    print("📁 Direct Commands (use these):")
    print("   python tests/run_all_tests.py              # Complete test suite")
    print("   python tests/run_all_tests.py --unit       # Unit tests only")
    print("   python tests/run_all_tests.py --integration # Integration tests")
    print("   python tests/run_all_tests.py --manual     # Manual component tests")
    print("   python tests/run_all_tests.py --quick      # Quick functionality check")
    print("   python debug/standalone_tests.py           # Standalone component tests")
    print("   python debug/debug_run.py                  # Debug application runner")
    print("   python debug/diagnostic.py                 # System diagnostic")
    print()
    print("🔧 Setup:")
    print("   python tests/run_all_tests.py --setup      # Create test structure")
    print()
    print("💡 Shortcuts (via this dispatcher):")
    print("   python tests/run_tests.py --unit           # → tests/run_all_tests.py --unit")
    print("   python tests/run_tests.py --manual         # → tests/run_all_tests.py --manual")
    print("   python tests/run_tests.py --quick          # → tests/run_all_tests.py --quick")
    print("   python tests/run_tests.py --debug          # → debug/debug_run.py")
    print("   python tests/run_tests.py --diagnostic     # → debug/diagnostic.py")
    print("   python tests/run_tests.py --standalone     # → debug/standalone_tests.py")
    print("   python tests/run_tests.py --setup          # → tests/run_all_tests.py --setup")
    print()
    print("✅ CLEANUP COMPLETED:")
    print("   🗑️ manual_test.py → DELETED (moved to tests/utils/)")
    print("   🗑️ quick_test.py → DELETED (moved to tests/utils/)")
    print("   📁 run_tests.py → MOVED to tests/run_tests.py")
    print()
    print("✅ Main directory now clean - only run.py remains")

def run_delegated_command(script_path, args=None):
    """Run a delegated script"""
    if args is None:
        args = []
    
    # Adjust paths since we're now in tests/ directory
    if script_path.startswith('tests/'):
        # Remove tests/ prefix since we're already in tests/
        script_path = script_path[6:]
    elif script_path.startswith('debug/'):
        # Go up one level to reach debug/
        script_path = '../' + script_path
    
    full_path = os.path.join(os.path.dirname(__file__), script_path)
    
    if not os.path.exists(full_path):
        print(f"❌ Script not found: {script_path}")
        print("💡 Run 'python tests/run_tests.py --setup' to create the test structure")
        return False
    
    try:
        cmd = [sys.executable, full_path] + args
        result = subprocess.run(cmd, timeout=300)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running {script_path}: {e}")
        return False

def main():
    """Main dispatcher function"""
    if len(sys.argv) == 1:
        show_help()
        return True
    
    arg = sys.argv[1].lower()
    
    # Quick shortcuts
    if arg in ['--unit', '-u']:
        return run_delegated_command('run_all_tests.py', ['--unit'])
    elif arg in ['--integration', '-i']:
        return run_delegated_command('run_all_tests.py', ['--integration'])
    elif arg in ['--manual', '-m']:
        return run_delegated_command('run_all_tests.py', ['--manual'])
    elif arg in ['--quick', '-q']:
        return run_delegated_command('run_all_tests.py', ['--quick'])
    elif arg in ['--standalone', '-s']:
        return run_delegated_command('debug/standalone_tests.py')
    elif arg in ['--debug', '-d']:
        return run_delegated_command('debug/debug_run.py')
    elif arg in ['--diagnostic']:
        return run_delegated_command('debug/diagnostic.py')
    elif arg in ['--setup']:
        return run_delegated_command('run_all_tests.py', ['--setup'])
    elif arg in ['--all', '-a']:
        return run_delegated_command('run_all_tests.py', ['--all'])
    elif arg in ['--help', '-h']:
        show_help()
        return True
    else:
        # Default: run main test suite
        return run_delegated_command('run_all_tests.py', sys.argv[1:])

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        sys.exit(1)
