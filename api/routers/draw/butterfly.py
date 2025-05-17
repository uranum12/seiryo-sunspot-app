import multiprocessing as mp
import tempfile
from base64 import b64encode
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from seiryo_sunspot_lib.butterfly_config import ButterflyDiagram

from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes
from api.tasks import butterfly as task_butterfly

router = APIRouter(prefix="/draw")


@router.get("/butterfly", response_model=PreviewRes)
def draw_butterfly(query: PreviewQuery = Depends()) -> PreviewRes:
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
            ButterflyDiagram.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with tempfile.NamedTemporaryFile() as f_tmp:
        ctx = mp.get_context("spawn")
        p = ctx.Process(
            target=task_butterfly.draw_butterfly_diagram,
            args=(
                str(input_path.with_suffix(".npz")),
                str(input_path.with_suffix(".json")),
                str(config_path),
                f_tmp.name,
            ),
        )
        p.start()
        p.join()
        img = b64encode(f_tmp.read()).decode()
    return PreviewRes(img=img)


@router.post("/butterfly", response_model=SaveRes)
def save_butterfly(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"{input_path.stem}.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            ButterflyDiagram.model_validate_json(f.read())
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    ctx = mp.get_context("spawn")
    p = ctx.Process(
        target=task_butterfly.draw_butterfly_diagram,
        args=(
            str(input_path.with_suffix(".npz")),
            str(input_path.with_suffix(".json")),
            str(config_path),
            str(output_path),
        ),
        kwargs={"fmt": body.format, "dpi": body.dpi},
    )
    p.start()
    p.join()
    return SaveRes(output=str(output_path))
