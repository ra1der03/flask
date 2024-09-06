from typing import Optional, Type

import pydantic
from pydantic import BaseModel


class BaseAdvertisement(BaseModel):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]
    @pydantic.field_validator("owner")
    @classmethod
    def valid_ownerName(cls, value):
        if value is None:
            raise ValueError("password isn't valid")
        return value


class CreateAdvertisement(BaseAdvertisement):
    name: str
    description: Optional[str]
    owner: str


class UpdateAdvertisement(BaseAdvertisement):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]


Schema = Type[CreateAdvertisement] | Type[UpdateAdvertisement]
