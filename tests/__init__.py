"""
Test package for Riflescope Clicks Calculator

This package contains all unit tests, integration tests, and test utilities
for the riflescope clicks calculator application.

Directory structure:
- unit/: Unit tests for individual components
- integration/: Integration tests for component interactions
- fixtures/: Test data and mock objects
- utils/: Test utilities and helpers
"""

import sys
import os
import types

# Add project root to Python path for test imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def setup_test_environment():
    """Setup test environment with mock loggers and dependencies"""
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
    
    # Add all loggers from the actual logger.py
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

# Auto-setup when importing tests package
setup_test_environment()

__version__ = "1.0.0"
__author__ = "Riflescope Calculator Team"
