from csv import DictReader
from pathlib import Path
from re import compile

from pydantic import BaseModel


class FinderResult(BaseModel):
    path: str
    lines: list[int]


def finder(
    search_path: Path, year: int, month: int, day: int
) -> list[FinderResult]:
    pattern = compile(
        r"(?P<year>\d{4})"
        r"(?:[-/\. ])"
        r"(?P<month>\d{1,2})"
        r"(?:[-/\. ])"
        r"(?P<day>\d{1,2})"
    )
    result: list[FinderResult] = []
    for path in search_path.glob("*.csv"):
        with path.open("r") as f:
            reader = DictReader(f)
            match_line_num: list[int] = []
            for row in reader:
                if match := pattern.fullmatch(row["date"]):
                    groups = match.groupdict()
                    if (
                        int(groups["year"]) == year
                        and int(groups["month"]) == month
                        and int(groups["day"]) == day
                    ):
                        match_line_num.append(reader.line_num)
        if len(match_line_num) != 0:
            result.append(FinderResult(path=str(path), lines=match_line_num))
    return result
