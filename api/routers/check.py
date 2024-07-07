from pathlib import Path
from typing import Literal, TypeAlias

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.libs import check_file


class CheckFileErrorHeader(BaseModel):
    type: Literal["header"]
    header: list[str] | None


class CheckFileErrorRow(BaseModel):
    type: Literal["row"]
    line: int
    over: list[str]


class CheckFileErrorField(BaseModel):
    type: Literal["field"]
    line: int
    fields: list[str]


CheckFileError: TypeAlias = (
    CheckFileErrorHeader | CheckFileErrorRow | CheckFileErrorField
)


class CheckFileQuery(BaseModel):
    input: str


class CheckFileRes(BaseModel):
    errors: list[CheckFileError]


router = APIRouter(prefix="/check", tags=["check"])


@router.get("/file", response_model=CheckFileRes)
def validate_file(query: CheckFileQuery = Depends()) -> CheckFileRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    with input_path.open("r") as f:
        ret = check_file.validate_file(f)
    errors: list[CheckFileError] = []
    for err in ret:
        match err["type"]:
            case "header":
                errors.append(CheckFileErrorHeader(**err))
            case "row":
                errors.append(CheckFileErrorRow(**err))
            case "field":
                errors.append(CheckFileErrorField(**err))
    return CheckFileRes(errors=errors)
