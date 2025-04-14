from dataclasses import dataclass
from typing import List

@dataclass
class Drug:
    id: int
    name: str
    active_ingredients: List[str]
    usage_instructions: str
    side_effects: List[str]
    dosage: str
    interactions: List[str]
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            name=data['name'],
            active_ingredients=data['active_ingredients'],
            usage_instructions=data['usage_instructions'],
            side_effects=data['side_effects'],
            dosage=data['dosage'],
            interactions=data['interactions']
        ) 