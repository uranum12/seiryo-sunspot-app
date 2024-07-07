import pytest

from api.libs import check_file


@pytest.mark.parametrize(
    ("in_date", "result"),
    [
        ("2020/8/20", True),
        ("2020/08/20", True),
        ("2020-8-20", True),
        ("2020-08-20", True),
        ("2020.8.20", True),
        ("2020.08.20", True),
        ("2020 8 20", True),
        ("2020 08 20", True),
        ("2020/003/03", False),
        ("2020/9-5", False),
        ("2020/9.5", False),
        ("2020/9 5", False),
        ("2020-9.5", False),
        ("2020-9 5", False),
        ("2020.9 5", False),
        ("20000/2/2", False),
        ("20/12/20", False),
        ("2020/15/4", False),
        ("2020/3/40", False),
        ("2020/2/29", True),
        ("2021/2/29", False),
        ("", False),
    ],
)
def test_validate_date(in_date: str, result: bool) -> None:
    assert check_file.validate_date(in_date) == result


@pytest.mark.parametrize(
    ("in_no", "result"),
    [
        ("0", True),
        ("1", True),
        ("1.2", False),
        ("01", True),
        ("12", True),
        ("123", True),
        ("-1", False),
        ("alpha", False),
        ("", False),
    ],
)
def test_validate_no(in_no: str, result: bool) -> None:
    assert check_file.validate_no(in_no) == result


@pytest.mark.parametrize(
    ("in_lat", "result"),
    [
        ("12", True),
        ("+12", True),
        ("-12", True),
        ("N12", True),
        ("S12", True),
        ("n12", True),
        ("s12", True),
        ("P12", True),
        ("M12", True),
        ("p12", True),
        ("m12", True),
        ("W23", False),
        ("3~5", True),
        ("-3~-5", True),
        ("+3~-3", True),
        ("N3~5", True),
        ("S3~5", True),
        ("N3~N5", True),
        ("3~N5", False),
        ("0~N3", True),
        ("p7~m3", True),
        ("+3~m1", True),
        ("6~-5", True),
        ("S3~-2", False),
        ("12.3", True),
        ("12.3~23.4", True),
        ("S12.4~23.4", True),
        ("p1.2~m2.72", True),
        ("100", False),
        ("ND", True),
        ("nd", True),
        ("md", False),
        ("", False),
    ],
)
def test_validate_lat(in_lat: str, result: bool) -> None:
    assert check_file.validate_lat(in_lat) == result


@pytest.mark.parametrize(
    ("in_lon", "result"),
    [
        ("12", True),
        ("+12", True),
        ("-12", True),
        ("E12", True),
        ("W12", True),
        ("e12", True),
        ("w12", True),
        ("P12", True),
        ("M12", True),
        ("p12", True),
        ("m12", True),
        ("S23", False),
        ("3~5", True),
        ("-3~-5", True),
        ("+3~-3", True),
        ("E3~5", True),
        ("W3~5", True),
        ("E3~E5", True),
        ("3~E5", False),
        ("0~E3", True),
        ("p7~m3", True),
        ("+3~m1", True),
        ("6~-5", True),
        ("W3~-2", False),
        ("12.3", True),
        ("12.3~23.4", True),
        ("E12.4~23.4", True),
        ("p1.2~m2.72", True),
        ("100", False),
        ("ND", True),
        ("nd", True),
        ("md", False),
        ("", False),
    ],
)
def test_validate_lon(in_lon: str, result: bool) -> None:
    assert check_file.validate_lon(in_lon) == result


@pytest.mark.parametrize(
    ("in_num", "result"),
    [
        ("1", True),
        ("1.2", False),
        ("01", True),
        ("12", True),
        ("123", True),
        ("-1", False),
        ("0", False),
        ("", False),
    ],
)
def test_validate_num(in_num: str, result: bool) -> None:
    assert check_file.validate_num(in_num) == result


@pytest.mark.parametrize(
    ("in_row", "in_first", "result"),
    [
        (
            {
                "date": "2020/8/20",
                "no": "1",
                "lat": "N12",
                "lon": "E10",
                "num": "3",
            },
            True,
            [],
        ),
        (
            {
                "date": "2020/8/20",
                "no": "1",
                "lat": "N12",
                "lon": "E10",
                "num": "3",
            },
            False,
            [],
        ),
        (
            {"date": "", "no": "1", "lat": "N12", "lon": "E10", "num": "3"},
            True,
            ["date"],
        ),
        (
            {"date": "", "no": "1", "lat": "N12", "lon": "E10", "num": "3"},
            False,
            [],
        ),
        (
            {
                "date": "20200820",
                "no": "No.1",
                "lat": "W12",
                "lon": "S10",
                "num": "0",
            },
            True,
            ["date", "no"],
        ),
        (
            {
                "date": "2020/8/20",
                "no": "1",
                "lat": "W12",
                "lon": "S10",
                "num": "0",
            },
            True,
            ["lat", "lon", "num"],
        ),
        (
            {"date": "2020/8/20", "no": "0", "lat": "", "lon": "", "num": ""},
            True,
            [],
        ),
        (
            {
                "date": "2020/8/20",
                "no": "0",
                "lat": "12",
                "lon": "",
                "num": "4",
            },
            True,
            ["lat", "num"],
        ),
        (
            {"date": None, "no": "1", "lat": None, "lon": None, "num": None},
            True,
            ["date", "lat", "lon", "num"],
        ),
        (
            {"date": None, "no": None, "lat": "12", "lon": "3", "num": None},
            True,
            ["date", "no"],
        ),
        (
            {"date": None, "no": "0", "lat": None, "lon": None, "num": None},
            True,
            ["date", "lat", "lon", "num"],
        ),
    ],
)
def test_validate_row(
    in_row: dict[str, str | None], in_first: bool, result: list[str]
) -> None:
    assert check_file.validate_row(in_row, first=in_first) == result


@pytest.mark.parametrize(
    ("in_file", "result"),
    [
        (
            [
                "date,no,lat,lon,num\n",
                "2020/8/20,1,N12,E2~5,3\n",
                ",2,N3~6,W2,4\n",
                "2020/9/2,0,,,\n",
            ],
            [],
        ),
        (
            [
                "dat,No,lat,long,num\n",
                "2020/8/20,1,N12,E2~5,3\n",
                ",2,N3~6,W2,4\n",
                "2020/9/2,0,,,\n",
            ],
            [
                {
                    "type": "header",
                    "header": ["dat", "No", "lat", "long", "num"],
                }
            ],
        ),
        ([], [{"type": "header", "header": None}]),
        (
            [
                "date,no,lat,lon,num\n",
                "2020/8/20,1,N12,E2~5,3\n",
                ",2,N3~6,W2,4,foo\n",
                "2020/9/2,0,,,,\n",
            ],
            [
                {"type": "row", "line": 3, "over": ["foo"]},
                {"type": "row", "line": 4, "over": [""]},
            ],
        ),
        (
            [
                "date,no,lat,lon,num\n",
                ",1,N12,E2~5,3\n",
                "2020/8/20,2,N3~6,W2,4\n",
                "2020/9/2,0,,\n",
            ],
            [
                {"type": "field", "line": 2, "fields": ["date"]},
                {"type": "field", "line": 4, "fields": ["num"]},
            ],
        ),
    ],
)
def test_validate_file(in_file: list[str], result: list[dict]) -> None:
    ret = check_file.validate_file(in_file)
    print(ret)
    assert ret == result
