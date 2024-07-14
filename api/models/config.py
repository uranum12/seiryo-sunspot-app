from typing import Generic, TypeVar

from pydantic import BaseModel

_T = TypeVar("_T", bound=BaseModel)


class GetConfigQuery(BaseModel):
    config_name: str


class GetConfigRes(BaseModel, Generic[_T]):
    config: _T


class CreateConfigBody(BaseModel, Generic[_T]):
    config_name: str
    overwrite: bool = False
    config: _T


class CreateConfigRes(BaseModel):
    output: str


class PreviewBody(BaseModel, Generic[_T]):
    config: _T


class PreviewRes(BaseModel):
    img: str
