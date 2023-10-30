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
data = {
    "bank": "Банк",
    "debt": "100000",
    "birthdate": "123",
    "gender": "Мужской",
    "existing_policy": "Полис123",
    "property_address": "Адрес1",
    "property_size": 50.0,
    "floor_and_building_floors": "5/10",
    "building_year": 2001
}

policy = PropertyInsurancePolicy(**data)
(policy)