"""Application constants and configuration values"""

# Validation constants
class ValidationConstants:
    MIN_POSITION_VALUE = -1000
    MAX_POSITION_VALUE = 1000
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 1
    MAX_CALIBER_DECIMAL_PLACES = 3
    
    # Supported units
    DISTANCE_UNITS = ['m', 'yd', 'ft']
    CALIBER_UNITS = ['mm', 'in']
    
    # Regex patterns
    CALIBER_PATTERN = r'^\d+(\.\d{1,3})?\s*(mm|in)$'
    NAME_PATTERN = r'^[a-zA-Z0-9\-\s\.]+$'
    NUMBER_PATTERN = r'^\d+$'
    DECIMAL_PATTERN = r'^\d+(\.\d+)?$'

# Database constants
class DatabaseConstants:
    DEFAULT_DB_NAME = "riflescope_clicks.db"
    BACKUP_EXTENSION = ".bak"
    
    # Table names
    WEAPONS_TABLE = "weapons"
    AMMUNITION_TABLE = "ammunition"
    DISTANCES_TABLE = "distances"
    RESULTS_TABLE = "results"

# GUI constants
class GUIConstants:
    TOOLTIP_DELAY = 500  # milliseconds
    MIN_WINDOW_WIDTH = 400
    MIN_WINDOW_HEIGHT = 500
    
    # Colors
    SUCCESS_COLOR = "#28a745"
    ERROR_COLOR = "#dc3545"
    WARNING_COLOR = "#ffc107"
    INFO_COLOR = "#17a2b8"

# Logging constants
class LoggingConstants:
    DEFAULT_LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
