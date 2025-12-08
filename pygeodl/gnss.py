"""
Docstring for pygeodl.gnss

This module provides functionalities for downloading GNSS (Global Navigation Satellite System) data.
"""

import pandas as pd
import requests
import io
import typing

class unavco():
    """
    A class to handle downloading GNSS data from the UNAVCO repository.
    """

    def __init__(self):
        self.base_url = "https://web-services.unavco.org"
        self.expected_format = "text/csv; charset=utf-8"

    def request(self, station: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Request GNSS data from the UNAVCO repository.

        An example API request URL:
            https://web-services.unavco.org/gps/data/position/P201/v3?start=2020-01-01&end=2020-01-02
        """
        url = f"{self.base_url}/gps/data/position/{station}/v3?start={start_date}&end={end_date}"
        response = requests.get(url)
        response.raise_for_status()

        if response.headers.get('Content-Type') != self.expected_format:
            raise ValueError("Unexpected response format")

        #TODO parse header data as metadata
        df = pd.read_csv(io.StringIO(response.text), comment='#')
        #df.set_index('Datetime', inplace=True)

        # Remove leading/trailing whitespace from column names
        df.columns = [col.strip() for col in df.columns]

        return df

