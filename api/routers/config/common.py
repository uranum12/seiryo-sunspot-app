import json
from pathlib import Path
from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel

from api.models.config import (
    CreateConfigBody,
    CreateConfigRes,
    GetConfigQuery,
    GetConfigRes,
)

_T = TypeVar("_T", bound=BaseModel)


def get_config(
    query: GetConfigQuery, config_type: type[_T]
) -> GetConfigRes[_T]:
    input_path = Path(query.config_name)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {input_path} not found"
        )
    try:
        with input_path.open("r") as f:
            config = config_type(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {input_path} is broken"
        ) from e
    return GetConfigRes[_T](config=config)


def post_config(
    body: CreateConfigBody[_T], output_dir: Path
) -> CreateConfigRes:
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / f"{body.config_name}.json"
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"config {output_path} already exists"
        )
    with output_path.open("w") as f:
        f.write(body.config.model_dump_json())
    return CreateConfigRes(output=str(output_path))
