from pydantic import BaseModel


class PreviewQuery(BaseModel):
    filename: str
    config_name: str


class PreviewRes(BaseModel):
    img: str


class SaveBody(BaseModel):
    input: str
    config: str
    format: str
    dpi: int = 300
    overwrite: bool = False


class SaveRes(BaseModel):
    output: str
