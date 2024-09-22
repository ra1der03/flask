from typing import Optional, Type

import pydantic
from pydantic.v1 import BaseModel, validator


class BaseAdvertisement(BaseModel):
    name: str
    description: str
    owner: str

    @validator("owner")
    def valid_owner_name(cls, value):
        flag = False
        flag = value.isdigit()
        if flag:
            raise ValueError("owner name isn't valid")
        return value


class CreateAdvertisement(BaseAdvertisement):
    name: str
    description: str
    owner: str


class UpdateAdvertisement(BaseAdvertisement):
    name: Optional[str]
    description: Optional[str]
    owner: Optional[str]


Schema = Type[CreateAdvertisement] | Type[UpdateAdvertisement]
