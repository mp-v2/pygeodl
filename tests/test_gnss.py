"""
Docstring for tests.test_gnss
"""

import pytest
from pygeodl import gnss
import requests
from contextlib import nullcontext as does_not_raise

# @pytest.mark.parametrize(
#     "example_input,expectation",
#     [
#         (3, does_not_raise()),
#         (2, does_not_raise()),
#         (1, does_not_raise()),
#         (0, pytest.raises(ZeroDivisionError)),
#     ],
# )

def test_unavco_find_basic():
    downloader = gnss.unavco()
    df = downloader.find(
        minlatitude=43.0,
        maxlatitude=60.0,
        minlongitude=-122.0,
        maxlongitude=-120.0,
        starttime="2012-01-01",
        endtime="2025-01-01",
        summary=False
    )
    assert not df.empty
    assert 'id' in df.columns
    assert 'station_name' in df.columns
    assert 'latitude' in df.columns
    assert 'longitude' in df.columns

def test_unavco_request_basic():
    downloader = gnss.unavco()
    df = downloader.request(station="P201", starttime="2020-01-01", endtime="2020-01-02")
    assert not df.empty
    for column in ['Datetime', 'delta N', 'delta E', 'delta U', 'Std Dev N', 'Std Dev E', 'Std Dev U', 'Solution']:
        assert column in df.columns
        assert len(df)==2 #daily data, so this checks 2 days of data were downloaded

@pytest.mark.parametrize("station,starttime,endtime,expected", [
    ("P201", "2020-01-01", "2020-01-02", does_not_raise()), #valid request
    ("XXX", "2020-01-01", "2020-01-02", pytest.raises(requests.exceptions.HTTPError)), #incorrect station name
    #("P201", "2020-01-01", "2020-01-02", does_not_raise()),
])
def test_unavco_request(station, starttime, endtime, expected):
    downloader = gnss.unavco()
    with expected:
        df = downloader.request(station=station, starttime=starttime, endtime=endtime)
        assert not df.empty
        for column in ['Datetime', 'delta N', 'delta E', 'delta U', 'Std Dev N', 'Std Dev E', 'Std Dev U', 'Solution']:
            assert column in df.columns


