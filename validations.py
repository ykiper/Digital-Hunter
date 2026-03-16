from pydantic import BaseModel, Field, ValidationError



class Intel(BaseModel):
    timestamp: str
    signal_id: str
    entity_id: str
    reported_lat: float
    reported_lon: float
    signal_type: str = Field()
    priority_level: int = Field(default=99, ge=1, lt=99)

class Attack(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    type_weapon: str

class Damage(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str

