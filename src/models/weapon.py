class WeaponModel:
    """Data model for weapon entities"""
    
    def __init__(self, weapon_id=None, name=None, caliber=None):
        self.id = weapon_id
        self.name = name
        self.caliber = caliber
    
    def __str__(self):
        return f"Weapon(id={self.id}, name='{self.name}', caliber='{self.caliber}')"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def display_name(self):
        """Returns formatted display name for UI"""
        return f"{self.name} ({self.caliber})"
    
    @classmethod
    def from_tuple(cls, weapon_tuple):
        """Create WeaponModel from database tuple"""
        if weapon_tuple and len(weapon_tuple) >= 3:
            return cls(weapon_tuple[0], weapon_tuple[1], weapon_tuple[2])
        return None
