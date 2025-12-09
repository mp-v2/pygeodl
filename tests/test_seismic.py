"""
Docstring for tests.test_seismic
"""

import pytest
from pygeodl import seismic
import requests
from contextlib import nullcontext as does_not_raise


def test_bgs_request_basic():
    downloader = seismic.bgs()
    df = downloader.request(
        starttime="2025-01-01",
        endtime="2025-02-01",
        minlatitude=49.0,
        maxlatitude=63.0,
        minlongitude=-12.0,
        maxlongitude=5.0,
        mindepth=1.0,
        maxdepth=10.0,
        output="csv",
    )
    assert not df.empty
    assert df.iloc[0]["yyyy-mm-dd"] == "2025-01-01"
    assert df.iloc[0]["magnitude"] == 0.7
    assert df.iloc[0]["locality"] == "MELBOURNE, DERBYSHIRE"
    # for column in ['LAT', 'LON', 'DEPTH', 'MAG', 'NST', 'GAP', 'RMS', 'EVENT_ID']:
    #     assert column in df.columns
