from typing import Optional, Type
from pydantic import BaseModel


class BaseAdvertisement(BaseModel):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]


class CreateAdvertisement(BaseAdvertisement):
    name: str
    description: Optional[str]
    owner: str


class UpdateAdvertisement(BaseAdvertisement):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]


Schema = Type[CreateAdvertisement] | Type[UpdateAdvertisement]
