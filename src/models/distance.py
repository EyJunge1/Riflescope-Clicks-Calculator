class DistanceModel:
    """Data model for distance entities"""
    
    def __init__(self, distance_id=None, value=None, unit=None):
        self.id = distance_id
        self.value = value
        self.unit = unit
    
    def __str__(self):
        return f"Distance(id={self.id}, value='{self.value}', unit='{self.unit}')"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def display_name(self):
        """Returns formatted display name for UI"""
        return f"{self.value}{self.unit}"
    
    @classmethod
    def from_tuple(cls, distance_tuple):
        """Create DistanceModel from database tuple"""
        if distance_tuple and len(distance_tuple) >= 3:
            return cls(distance_tuple[0], distance_tuple[1], distance_tuple[2])
        return None
