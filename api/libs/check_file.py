from collections.abc import Iterable
from csv import DictReader
from datetime import date
from re import compile

_pat_case = r"(?i)"
_pat_number = r"\d+"
_pat_date = (
    r"(?P<year>\d{4})"
    r"(?P<sep1>[-/\. ])"
    r"(?P<month>\d{1,2})"
    r"(?P<sep2>[-/\. ])"
    r"(?P<day>\d{1,2})"
)
_pat_lat_left = r"(?P<left>\d{1,2}(?:\.\d+)?)"
_pat_lat_right = r"(?P<right>\d{1,2}(?:\.\d+)?)"
_pat_lon_left = r"(?P<left>\d{1,3}(?:\.\d+)?)"
_pat_lon_right = r"(?P<right>\d{1,3}(?:\.\d+)?)"
_pat_lat_left_sign = r"(?P<left_sign>[nspm+-]?)"
_pat_lat_right_sign = r"(?P<right_sign>[nspm+-]?)"
_pat_lon_left_sign = r"(?P<left_sign>[ewpm+-]?)"
_pat_lon_right_sign = r"(?P<right_sign>[ewpm+-]?)"
_pat_lat = (
    rf"{_pat_lat_left_sign}{_pat_lat_left}"
    rf"(?:~{_pat_lat_right_sign}{_pat_lat_right})?"
)
_pat_lat = rf"{_pat_case}(?P<not_detected>ND|{_pat_lat})"
_pat_lon = (
    rf"{_pat_lon_left_sign}{_pat_lon_left}"
    rf"(?:~{_pat_lon_right_sign}{_pat_lon_right})?"
)
_pat_lon = rf"{_pat_case}(?P<not_detected>ND|{_pat_lon})"
_patterns = {
    "date": compile(_pat_date),
    "no": compile(_pat_number),
    "lat": compile(_pat_lat),
    "lon": compile(_pat_lon),
    "num": compile(_pat_number),
}


def validate_date(s: str) -> bool:
    """日付の文字列が妥当か検査

    Args:
        s (str): 入力された文字列

    Returns:
        bool: 結果

    Examples:
        >>> validate_date("2020/8/10")
        True
        >>> validate_date("2020-08-10")
        True
        >>> validate_date("2020/8-20")
        False
        >>> validate_date("2020/13/42")
        False
    """
    pattern = _patterns["date"]
    if match := pattern.fullmatch(s):
        groups = match.groupdict()
        if groups["sep1"] == groups["sep2"]:
            try:
                date(*map(int, s.split(groups["sep1"])))
            except ValueError:
                pass
            else:
                return True
    return False


def validate_no(s: str) -> bool:
    """黒点群番号が妥当か検査

    Args:
        s (str): 入力された文字列

    Returns:
        bool: 結果

    Examples:
        >>> validate_no("0")
        True
        >>> validate_no("12")
        True
        >>> validate_no("-2")
        False
    """
    pattern = _patterns["no"]
    return bool(pattern.fullmatch(s))


def validate_lat(s: str) -> bool:
    """緯度が妥当か検査

    Args:
        s (str): 入力された文字列

    Returns:
        bool: 結果

    Examples:
        >>> validate_lon("ND")
        True
        >>> validate_lat("12")
        True
        >>> validate_lat("100")
        False
        >>> validate_lat("12.3")
        True
        >>> validate_lat("2~3")
        True
        >>> validate_lat("S12")
        True
        >>> validate_lat("W3")
        False
        >>> validate_lat("N6~12")
        True
        >>> validate_lat("0~N6")
        True
        >>> validate_lat("N6~N12")
        True
        >>> validate_lat("N6~-6")
        False
    """
    pattern = _patterns["lat"]
    lat_max = 90
    if match := pattern.fullmatch(s):
        groups = match.groupdict()
        if groups["not_detected"].lower() == "nd":
            return True
        if groups["right"] is None:
            left = float(groups["left"])
            return 0 <= left <= lat_max
        left_sign = groups["left_sign"].lower()
        right_sign = groups["right_sign"].lower()
        chars_dir = {"n", "s"}
        chars_sign = {"p", "m", "+", "-", ""}
        left = float(groups["left"])
        right = float(groups["right"])
        if left_sign in chars_dir and right_sign in chars_dir | {""}:
            return 0 <= left <= lat_max and 0 <= right <= lat_max
        if left_sign in chars_sign and right_sign in chars_sign:
            return 0 <= left <= lat_max and 0 <= right <= lat_max
        if left_sign == "" and right_sign in chars_dir:
            return left == 0 and 0 <= right <= lat_max
    return False


def validate_lon(s: str) -> bool:
    """経度が妥当か検査

    Args:
        s (str): 入力された文字列

    Returns:
        bool: 結果

    Examples:
        >>> validate_lon("nd")
        True
        >>> validate_lon("12")
        True
        >>> validate_lon("E12")
        True
        >>> validate_lon("N12")
        False
        >>> validate_lon("W12~15")
        True
        >>> validate_lon("12~-15")
        True
        >>> validate_lon("12~W15")
        False
    """
    pattern = _patterns["lon"]
    lon_max = 360
    if match := pattern.fullmatch(s):
        groups = match.groupdict()
        if groups["not_detected"].lower() == "nd":
            return True
        if groups["right"] is None:
            left = float(groups["left"])
            return 0 <= left <= lon_max
        left_sign = groups["left_sign"].lower()
        right_sign = groups["right_sign"].lower()
        chars_dir = {"e", "w"}
        chars_sign = {"p", "m", "+", "-", ""}
        left = float(groups["left"])
        right = float(groups["right"])
        if left_sign in chars_dir and right_sign in chars_dir | {""}:
            return 0 <= left <= lon_max and 0 <= right <= lon_max
        if left_sign in chars_sign and right_sign in chars_sign:
            return 0 <= left <= lon_max and 0 <= right <= lon_max
        if left_sign == "" and right_sign in chars_dir:
            return left == 0 and 0 <= right <= lon_max
    return False


def validate_num(s: str) -> bool:
    """黒点数が妥当か検査

    Args:
        s (str): 入力された文字列

    Returns:
        bool: 結果

    Examples:
        >>> validate_num("12")
        True
        >>> validate_num("0")
        False
        >>> validate_num("-12")
        False
    """
    pattern = compile(r"\d+")
    if match := pattern.fullmatch(s):
        num = match.group()
        return int(num) > 0
    return False


def validate_row(row: dict[str, str | None], *, first: bool) -> list[str]:
    """入力された行が妥当か検査

    Args:
        row (dict[str, str | None]): 入力された行
        first (bool): 行が一番初めかどうか

    Returns:
        list[str]: 不正と検出された列名
    """
    errors: list[str] = []

    if (
        row["date"] is None
        or not validate_date(row["date"])
        and (first or row["date"] != "")
    ):
        errors.append("date")

    if row["no"] is None or not validate_no(row["no"]):
        errors.append("no")
        return errors

    if int(row["no"]) == 0:
        errors.extend(
            [field for field in ["lat", "lon", "num"] if row[field] != ""]
        )

    else:
        if row["lat"] is None or not validate_lat(row["lat"]):
            errors.append("lat")
        if row["lon"] is None or not validate_lon(row["lon"]):
            errors.append("lon")
        if row["num"] is None or not validate_num(row["num"]):
            errors.append("num")
    return errors


def validate_file(file: Iterable[str]) -> list[dict]:
    """CSVファイル全体が妥当か検査

    Args:
        file (Iterable[str]): CSVファイル

    Returns:
        list[dict]: 不正と検出された箇所と種類
    """
    reader = DictReader(file, restkey="over", strict=True)

    fields = reader.fieldnames
    if fields is None or fields != ["date", "no", "lat", "lon", "num"]:
        return [{"type": "header", "header": fields}]

    first = True
    errors: list[dict[str, str | int | list[str]]] = []
    for row in reader:
        if "over" in row:
            errors.append(
                {
                    "type": "row",
                    "line": reader.line_num,
                    "over": list(row["over"]),
                }
            )

        if len(ret := validate_row(row, first=first)) != 0:
            errors.append(
                {"type": "field", "line": reader.line_num, "fields": ret}
            )

        if first:
            first = False
    return errors
