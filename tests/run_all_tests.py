#!/usr/bin/env python3
"""
Complete Test Suite Runner

This script contains the actual test execution logic for the riflescope calculator.
All tests are now organized in the tests/ directory structure.
"""

import unittest
import sys
import os
from io import StringIO
import argparse

def setup_test_environment():
    """Setup proper Python path for testing"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    src_path = os.path.join(project_root, 'src')
    tests_path = os.path.join(project_root, 'tests')
    
    for path in [project_root, src_path, tests_path]:
        if path not in sys.path:
            sys.path.insert(0, path)

def create_test_structure():
    """Create complete test directory structure"""
    print("🏗️ Creating test structure...")
    
    base_dir = os.path.dirname(__file__)
    
    test_dirs = [
        'unit',
        'integration',
        'fixtures',
        'utils'
    ]
    
    debug_dir = os.path.join(os.path.dirname(base_dir), 'debug')
    
    # Create test directories
    for test_dir in test_dirs:
        full_path = os.path.join(base_dir, test_dir)
        os.makedirs(full_path, exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = os.path.join(full_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""{test_dir.title()} package for Riflescope Calculator tests"""\n')
        
        print(f"✓ Created tests/{test_dir}/")
    
    # Create debug directory
    os.makedirs(debug_dir, exist_ok=True)
    debug_init = os.path.join(debug_dir, '__init__.py')
    if not os.path.exists(debug_init):
        with open(debug_init, 'w') as f:
            f.write('"""Debug utilities for Riflescope Calculator"""\n')
    print(f"✓ Created debug/")
    
    print("✅ Test structure created successfully!")
    print("\n💡 Directory structure:")
    print("   tests/unit/        - Unit tests for individual components")
    print("   tests/integration/ - Integration tests")
    print("   tests/fixtures/    - Test data and mock objects")
    print("   tests/utils/       - Test utilities and manual test scripts")
    print("   debug/             - Debug tools and standalone tests")
    print("\n📁 Test utilities available:")
    print("   tests/utils/manual_test.py  - Manual component testing")
    print("   tests/utils/quick_test.py   - Quick functionality check")

def run_tests(verbosity=2, test_pattern="test_*.py"):
    """Run all tests with specified verbosity"""
    print("🧪 Running Complete Test Suite")
    print("=" * 50)
    
    setup_test_environment()
    
    # Import tests package to trigger mock setup
    try:
        import tests
        print("✓ Test environment initialized")
    except ImportError as e:
        print(f"❌ Could not initialize test environment: {e}")
        return False
    
    # Discover and run tests
    loader = unittest.TestLoader()
    tests_dir = os.path.dirname(__file__)
    
    suite = loader.discover(tests_dir, pattern=test_pattern)
    test_count = suite.countTestCases()
    
    if test_count == 0:
        print("⚠️  No tests found.")
        print("💡 Run with --setup to create test structure")
        return False
    
    print(f"📋 Found {test_count} test(s)")
    
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=verbosity)
    result = runner.run(suite)
    
    print(stream.getvalue())
    
    # Summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    
    print(f"\n📊 Results: {tests_run} run, {failures} failures, {errors} errors")
    
    if failures == 0 and errors == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        if result.failures:
            print("\n🔍 Failures:")
            for test, traceback in result.failures:
                print(f"   - {test}")
        if result.errors:
            print("\n🔍 Errors:")
            for test, traceback in result.errors:
                print(f"   - {test}")
    
    return failures == 0 and errors == 0

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description="Run Riflescope Calculator tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--setup", action="store_true", help="Create test directory structure")
    parser.add_argument("--all", action="store_true", help="Run all test types")
    parser.add_argument("--manual", action="store_true", help="Run manual component tests")
    parser.add_argument("--quick", action="store_true", help="Run quick functionality check")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.setup:
        create_test_structure()
        return True
    
    if args.manual:
        # Run manual tests
        import subprocess
        manual_script = os.path.join(os.path.dirname(__file__), 'utils', 'manual_test.py')
        if os.path.exists(manual_script):
            result = subprocess.run([sys.executable, manual_script])
            return result.returncode == 0
        else:
            print("❌ Manual test script not found. Run --setup first.")
            return False
    
    if args.quick:
        # Run quick tests
        import subprocess
        quick_script = os.path.join(os.path.dirname(__file__), 'utils', 'quick_test.py')
        if os.path.exists(quick_script):
            result = subprocess.run([sys.executable, quick_script])
            return result.returncode == 0
        else:
            print("❌ Quick test script not found. Run --setup first.")
            return False
    
    # For now, just run basic test discovery since we don't have many tests yet
    verbosity = 2 if args.verbose else 1
    success = run_tests(verbosity)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        sys.exit(1)
