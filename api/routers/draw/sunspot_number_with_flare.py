import multiprocessing as mp
import tempfile
from base64 import b64encode
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from seiryo_sunspot_lib.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)

from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes
from api.tasks import sunspot_number_with_flare as tasks

router = APIRouter(prefix="/draw")


@router.get("/with_flare", response_model=PreviewRes)
def draw_with_flare(query: PreviewQuery = Depends()) -> PreviewRes:
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
            SunspotNumberWithFlare.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=tasks.draw_sunspot_number_with_flare,
            args=(str(input_path), None, str(config_path), f_tmp.name),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/with_flare", response_model=SaveRes)
def save_with_flare(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"with_flare.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberWithFlare.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=tasks.draw_sunspot_number_with_flare,
        args=(str(input_path), None, str(config_path), str(output_path)),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))


@router.get("/with_flare_with_factor", response_model=PreviewRes)
def draw_with_flare_with_factor(query: PreviewQuery = Depends()) -> PreviewRes:
    with_flare_path = Path(query.filename).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            SunspotNumberWithFlare.model_validate_json(f_config.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=tasks.draw_sunspot_number_with_flare,
            args=(
                str(with_flare_path),
                str(factors_path),
                str(config_path),
                f_tmp.name,
            ),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/with_flare_with_factor", response_model=SaveRes)
def save_with_flare_with_factor(body: SaveBody) -> SaveRes:
    with_flare_path = Path(body.input).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = with_flare_path.with_name(
        f"with_flare_with_factor.{body.format}"
    )
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            SunspotNumberWithFlare.model_validate_json(f_config.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=tasks.draw_sunspot_number_with_flare,
        args=(
            str(with_flare_path),
            str(factors_path),
            str(config_path),
            str(output_path),
        ),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))


@router.get("/hemispheric", response_model=PreviewRes)
def draw_hemispheric(query: PreviewQuery = Depends()) -> PreviewRes:
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
            SunspotNumberWithFlareHemispheric.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=tasks.draw_sunspot_number_with_flare_hemispheric,
            args=(str(input_path), None, str(config_path), f_tmp.name),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/hemispheric", response_model=SaveRes)
def save_hemispheric(body: SaveBody) -> SaveRes:
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
            SunspotNumberWithFlareHemispheric.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=tasks.draw_sunspot_number_with_flare_hemispheric,
        args=(str(input_path), None, str(config_path), str(output_path)),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))


@router.get("/hemispheric_with_factors", response_model=PreviewRes)
def draw_hemispheric_with_factors(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    with_flare_path = Path(query.filename).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberWithFlareHemispheric.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=tasks.draw_sunspot_number_with_flare_hemispheric,
            args=(
                str(with_flare_path),
                str(factors_path),
                str(config_path),
                f_tmp.name,
            ),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/hemispheric_with_factors", response_model=SaveRes)
def save_hemispheric_with_factors(body: SaveBody) -> SaveRes:
    with_flare_path = Path(body.input).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = with_flare_path.with_name(
        f"hemispheric_with_factors.{body.format}"
    )
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            SunspotNumberWithFlareHemispheric.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=tasks.draw_sunspot_number_with_flare_hemispheric,
        args=(
            str(with_flare_path),
            str(factors_path),
            str(config_path),
            str(output_path),
        ),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))
