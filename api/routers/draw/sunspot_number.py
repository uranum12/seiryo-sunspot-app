import multiprocessing as mp
import tempfile
from base64 import b64encode
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)
from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes
from api.tasks import sunspot_number as task_sunspot_number

router = APIRouter(prefix="/draw")


@router.get("/whole_disk", response_model=PreviewRes)
def sunspot_number_draw_whole_disk(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    input_path = Path(query.filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberWholeDisk.model_validate_json(f.read(), strict=True)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=task_sunspot_number.draw_sunspot_number_whole_disk,
            args=(str(input_path), str(config_path), f_tmp.name),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/whole_disk", response_model=SaveRes)
def sunspot_number_save_whole_disk(body: SaveBody) -> SaveRes:
    input_path = Path(body.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = input_path.with_name(f"whole_disk.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberWholeDisk.model_validate_json(f.read(), strict=True)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=task_sunspot_number.draw_sunspot_number_whole_disk,
        args=(str(input_path), str(config_path), str(output_path)),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))


@router.get("/hemispheric", response_model=PreviewRes)
def sunspot_number_draw_hemispheric(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    input_path = Path(query.filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberHemispheric.model_validate_json(f.read(), strict=True)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=task_sunspot_number.draw_sunspot_number_hemispheric,
            args=(str(input_path), str(config_path), f_tmp.name),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/hemispheric", response_model=SaveRes)
def sunspot_number_save_hemispheric(body: SaveBody) -> SaveRes:
    input_path = Path(body.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = input_path.with_name(f"hemispheric.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberHemispheric.model_validate_json(f.read(), strict=True)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=task_sunspot_number.draw_sunspot_number_hemispheric,
        args=(str(input_path), str(config_path), str(output_path)),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))
