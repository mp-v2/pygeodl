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

def test_unavco_request_basic():
    downloader = gnss.unavco()
    df = downloader.request(station="P201", start_date="2020-01-01", end_date="2020-01-02")
    assert not df.empty
    for column in ['Datetime', 'delta N', 'delta E', 'delta U', 'Std Dev N', 'Std Dev E', 'Std Dev U', 'Solution']:
        assert column in df.columns

@pytest.mark.parametrize("station,start_date,end_date,expected", [
    ("P201", "2020-01-01", "2020-01-02", does_not_raise()), #valid request
    ("XXX", "2020-01-01", "2020-01-02", pytest.raises(requests.exceptions.HTTPError)), #incorrect station name
    #("P201", "2020-01-01", "2020-01-02", does_not_raise()),
])
def test_unavco_request(station, start_date, end_date, expected):
    downloader = gnss.unavco()
    with expected:
        df = downloader.request(station=station, start_date=start_date, end_date=end_date)
        assert not df.empty
        for column in ['Datetime', 'delta N', 'delta E', 'delta U', 'Std Dev N', 'Std Dev E', 'Std Dev U', 'Solution']:
            assert column in df.columns


