from pathlib import Path


def files(path: str, glob: str = "*") -> list[str]:
    return [str(file) for file in Path(path).glob(glob) if file.is_file()]
