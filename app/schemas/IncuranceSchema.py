from typing import Optional
from pydantic import BaseModel
from telebot import StateMemoryStorage
storage=StateMemoryStorage

class PropertyInsurancePolicy(BaseModel):
    bank: Optional[str]
    debt: str
    birthdate: str
    gender: str
    existing_policy: Optional[str]
    property_address: str
    property_size: float
    floor_and_building_floors: str
    building_year: int
