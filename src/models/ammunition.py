class AmmunitionModel:
    """Data model for ammunition entities"""
    
    def __init__(self, ammo_id=None, name=None, caliber=None, created_at=None):
        self.id = ammo_id
        self.name = name
        self.caliber = caliber
        self.created_at = created_at
    
    def __str__(self):
        return f"Ammunition(id={self.id}, name='{self.name}', caliber='{self.caliber}')"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def display_name(self):
        """Returns formatted display name for UI"""
        return f"{self.name} ({self.caliber})"
    
    @classmethod
    def from_tuple(cls, ammo_tuple):
        """Create AmmunitionModel from database tuple"""
        if ammo_tuple and len(ammo_tuple) >= 3:
            created_at = ammo_tuple[3] if len(ammo_tuple) > 3 else None
            return cls(ammo_tuple[0], ammo_tuple[1], ammo_tuple[2], created_at)
        return None
