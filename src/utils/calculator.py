from typing import Tuple, Optional, Union

# Try to import logger, but fall back to a mock if not available
try:
    from ..core import utils_calc_logger
except ImportError:
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
    utils_calc_logger = MockLogger()

class CalculationError(Exception):
    """Custom exception for calculation errors"""
    pass

# Klasse zur Berechnung der Klicks am Zielfernrohr
class ClickCalculator:
    """Enhanced click calculator with improved error handling and validation"""
    
    @staticmethod
    def calculate_clicks(current_position: Union[str, int], target_position: Union[str, int]) -> Tuple[int, Optional[str]]:
        """
        Calculates clicks and direction with enhanced error handling
        
        Args:
            current_position: Current scope position
            target_position: Target scope position
            
        Returns:
            Tuple of (clicks, direction) where direction is 'up', 'down', or None
            
        Raises:
            CalculationError: If calculation fails
        """
        utils_calc_logger.debug(f"Berechne Klicks: current={current_position}, target={target_position}")
        
        try:
            # Convert inputs to integers with better error handling
            if isinstance(current_position, str):
                current = int(current_position.strip())
            else:
                current = int(current_position)
                
            if isinstance(target_position, str):
                target = int(target_position.strip())
            else:
                target = int(target_position)
            
            utils_calc_logger.debug(f"Konvertierte Werte: current={current}, target={target}")
            
            # Validate ranges (reasonable scope adjustment limits)
            if not (-1000 <= current <= 1000) or not (-1000 <= target <= 1000):
                raise CalculationError("Position values must be between -1000 and 1000 clicks")
            
            clicks = abs(target - current)
            
            if current < target:
                direction = 'rechts'  # Changed from "up" to "rechts"
            elif current > target:
                direction = 'links'   # Changed from "down" to "links" 
            else:
                direction = None
            
            utils_calc_logger.info(f"Klicks berechnet: {clicks} Klicks {direction if direction else 'keine Änderung'}")
            return (clicks, direction)
            
        except ValueError as e:
            error_msg = f"Ungültige Eingabewerte: {e}"
            utils_calc_logger.error(error_msg)
            raise CalculationError(error_msg) from e
        except Exception as e:
            error_msg = f"Unerwarteter Fehler bei der Berechnung: {e}"
            utils_calc_logger.error(error_msg)
            raise CalculationError(error_msg) from e
    
    @staticmethod
    def calculate_moa_adjustment(distance_meters: float, target_size_cm: float) -> float:
        """
        Calculate MOA adjustment for given distance and target size
        
        Args:
            distance_meters: Distance to target in meters
            target_size_cm: Target size in centimeters
            
        Returns:
            MOA adjustment value
        """
        try:
            if distance_meters <= 0:
                raise CalculationError("Distance must be greater than zero")
            
            # 1 MOA = 2.908 cm at 100m
            moa_at_distance = (target_size_cm / distance_meters) * 100 / 2.908
            utils_calc_logger.debug(f"MOA berechnet: {moa_at_distance} für {distance_meters}m und {target_size_cm}cm")
            return round(moa_at_distance, 2)
        except ZeroDivisionError:
            raise CalculationError("Distance cannot be zero")
        except Exception as e:
            raise CalculationError(f"MOA calculation failed: {e}")
