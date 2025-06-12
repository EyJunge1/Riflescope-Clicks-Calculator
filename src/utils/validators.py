import re
from typing import Optional, Union

# Try to import logger, but fall back to a mock if not available
try:
    from ..core import utils_validators_logger
except ImportError:
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def warning(self, msg, *args, **kwargs): pass
    utils_validators_logger = MockLogger()

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validators:
    """Centralized validation class with improved error handling"""
    
    @staticmethod
    def validate_number(value: str, allow_empty: bool = False, min_value: Optional[int] = None, max_value: Optional[int] = None) -> bool:
        """Enhanced number validation with range checking"""
        utils_validators_logger.debug(f"Validiere Zahl: '{value}', allow_empty={allow_empty}, min={min_value}, max={max_value}")
        
        if allow_empty and not value:
            utils_validators_logger.debug("Leerer Wert akzeptiert")
            return True
        
        if not re.match(r'^\d+$', value):
            utils_validators_logger.warning(f"Ungültiges Zahlenformat: '{value}'")
            return False
        
        if min_value is not None or max_value is not None:
            try:
                num_value = int(value)
                if min_value is not None and num_value < min_value:
                    utils_validators_logger.warning(f"Wert {num_value} unter Minimum {min_value}")
                    return False
                if max_value is not None and num_value > max_value:
                    utils_validators_logger.warning(f"Wert {num_value} über Maximum {max_value}")
                    return False
            except ValueError:
                return False
        
        utils_validators_logger.debug(f"Zahlvalidierung für '{value}': erfolgreich")
        return True

    @staticmethod
    def validate_decimal(value: str, allow_empty: bool = False, decimal_places: Optional[int] = None) -> bool:
        """Enhanced decimal validation with precision control"""
        utils_validators_logger.debug(f"Validiere Dezimalzahl: '{value}', allow_empty={allow_empty}")
        
        if allow_empty and not value:
            utils_validators_logger.debug("Leerer Wert akzeptiert")
            return True
        
        pattern = r'^\d+(\.\d+)?$'
        if decimal_places is not None:
            pattern = f'^\\d+(\\.\\d{{1,{decimal_places}}})?$'
        
        result = bool(re.match(pattern, value))
        utils_validators_logger.debug(f"Dezimalvalidierung für '{value}': {result}")
        return result

    @staticmethod
    def validate_name(value: str, allow_empty: bool = False, min_length: int = 1, max_length: int = 100) -> bool:
        """Enhanced name validation with length checking"""
        utils_validators_logger.debug(f"Validiere Name: '{value}', allow_empty={allow_empty}")
        
        if allow_empty and not value:
            utils_validators_logger.debug("Leerer Wert akzeptiert")
            return True
        
        if len(value) < min_length or len(value) > max_length:
            utils_validators_logger.warning(f"Name '{value}' hat ungültige Länge: {len(value)}")
            return False
        
        result = bool(re.match(r'^[a-zA-Z0-9\-\s\.]+$', value))
        utils_validators_logger.debug(f"Namevalidierung für '{value}': {result}")
        return result

    @staticmethod
    def validate_caliber(value: str, allow_empty: bool = False) -> bool:
        """Enhanced caliber validation with unit checking"""
        utils_validators_logger.debug(f"Validiere Kaliber: '{value}', allow_empty={allow_empty}")
        
        if allow_empty and not value:
            utils_validators_logger.debug("Leerer Wert akzeptiert")
            return True
        
        # Support both formats: "7.62 mm" and "7.62mm"
        result = bool(re.match(r'^\d+(\.\d+)?\s*(mm|in)$', value))
        utils_validators_logger.debug(f"Kalibervalidierung für '{value}': {result}")
        return result

# Backwards compatibility
validate_number = Validators.validate_number
validate_decimal = Validators.validate_decimal
validate_name = Validators.validate_name
validate_caliber = Validators.validate_caliber
