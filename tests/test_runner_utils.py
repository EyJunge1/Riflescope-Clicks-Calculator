"""
Utility functions and mock objects for testing without full application imports
"""
import sys
import os

def setup_test_environment():
    """Setup test environment for proper imports"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    src_path = os.path.join(project_root, 'src')
    
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

class MockLogger:
    """Mock logger for testing without full logging setup"""
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
    def critical(self, msg): pass

def patch_loggers():
    """Patch logger imports for testing"""
    # Create mock loggers
    mock_logger = MockLogger()
    
    # Inject into sys.modules to avoid import errors
    if 'src.core' not in sys.modules:
        import types
        mock_core = types.ModuleType('src.core')
        mock_core.utils_calc_logger = mock_logger
        mock_core.utils_validators_logger = mock_logger
        mock_core.db_connection_logger = mock_logger
        mock_core.db_manager_logger = mock_logger
        mock_core.db_entities_logger = mock_logger
        sys.modules['src.core'] = mock_core

# Apply patches when module is imported
setup_test_environment()
patch_loggers()
