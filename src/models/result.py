class ResultModel:
    """Data model for result entities"""
    
    def __init__(self, result_id=None, weapon_name=None, ammunition_name=None, 
                 distance_value=None, distance_unit=None, result_value=None):
        self.id = result_id
        self.weapon_name = weapon_name
        self.ammunition_name = ammunition_name
        self.distance_value = distance_value
        self.distance_unit = distance_unit
        self.result_value = result_value
    
    def __str__(self):
        return f"Result(id={self.id}, weapon='{self.weapon_name}', ammo='{self.ammunition_name}', distance='{self.distance_display}', result='{self.result_value}')"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def distance_display(self):
        """Returns formatted distance display"""
        return f"{self.distance_value}{self.distance_unit}"
    
    @property
    def display_name(self):
        """Returns formatted display name for UI"""
        return f"{self.weapon_name} + {self.ammunition_name} @ {self.distance_display} = {self.result_value}"
    
    @classmethod
    def from_tuple(cls, result_tuple):
        """Create ResultModel from database tuple"""
        if result_tuple and len(result_tuple) >= 6:
            return cls(
                result_tuple[0],  # id
                result_tuple[1],  # weapon_name
                result_tuple[2],  # ammunition_name
                result_tuple[3],  # distance_value
                result_tuple[4],  # distance_unit
                result_tuple[5]   # result_value
            )
        return None
