import multiprocessing as mp
import tempfile
from base64 import b64encode
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from seiryo_sunspot_lib.observations_config import ObservationsMonthly

from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes
from api.tasks import observations as task_observations

router = APIRouter(prefix="/draw")


@router.get("/monthly", response_model=PreviewRes)
def observations_draw_monthly_preview(
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
            ObservationsMonthly.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=task_observations.draw_monthly_obs_days,
            args=(str(input_path), str(config_path), f_tmp.name),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/monthly", response_model=SaveRes)
def observations_draw_monthly_save(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"monthly.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            ObservationsMonthly.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=task_observations.draw_monthly_obs_days,
        args=(str(input_path), str(config_path), str(output_path)),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))
