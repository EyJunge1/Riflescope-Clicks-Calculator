from ..core import models_logger

# Basis-Model für gemeinsame Funktionalität
class BaseModel:
    """Basis-Klasse für alle Datenmodelle"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Konvertiert Model zu Dictionary"""
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_')}
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

class WeaponModel(BaseModel):
    """Model für Waffen-Daten"""
    def __init__(self, id=None, weapon=None, caliber=None, **kwargs):
        self.id = id
        self.weapon = weapon  
        self.caliber = caliber
        super().__init__(**kwargs)
        models_logger.debug(f"WeaponModel erstellt: {self}")

class AmmunitionModel(BaseModel):
    """Model für Munitions-Daten"""
    def __init__(self, id=None, ammunition=None, caliber=None, **kwargs):
        self.id = id
        self.ammunition = ammunition
        self.caliber = caliber
        super().__init__(**kwargs)
        models_logger.debug(f"AmmunitionModel erstellt: {self}")

class DistanceModel(BaseModel):
    """Model für Entfernungs-Daten"""
    def __init__(self, id=None, distance=None, unit=None, **kwargs):
        self.id = id
        self.distance = distance
        self.unit = unit
        super().__init__(**kwargs)
        models_logger.debug(f"DistanceModel erstellt: {self}")

class ResultModel(BaseModel):
    """Model für Ergebnis-Daten"""
    def __init__(self, id=None, weapon_id=None, ammunition_id=None, distance_id=None, result=None, **kwargs):
        self.id = id
        self.weapon_id = weapon_id
        self.ammunition_id = ammunition_id
        self.distance_id = distance_id
        self.result = result
        super().__init__(**kwargs)
        models_logger.debug(f"ResultModel erstellt: {self}")

__all__ = [
    'BaseModel',
    'WeaponModel',
    'AmmunitionModel', 
    'DistanceModel',
    'ResultModel'
]
