"""
Docstring for pygeodl.gnss

This module provides functionalities for downloading GNSS (Global Navigation Satellite System) data.
"""

import pandas as pd
import requests
import io
import typing
from loguru import logger

class unavco():
    """
    A class to handle downloading GNSS data from the UNAVCO repository.
    """

    def __init__(self):
        self.base_url = "https://web-services.unavco.org"
        self.expected_format = "text/csv; charset=utf-8"

    def find(
            self,
            minlatitude: float,
            maxlatitude: float,
            minlongitude: float,
            maxlongitude: float,
            starttime: str,
            endtime: str,
            summary: bool = False
            ) -> pd.DataFrame:
        """
        Method for finding available GNSS stations.
        """
        url = f"{self.base_url}/gps/metadata/sites/v1"
        params = dict(
            minlatitude=minlatitude,
            maxlatitude=maxlatitude,
            minlongitude=minlongitude,
            maxlongitude=maxlongitude,
            starttime=starttime,
            endtime=endtime,
            summary=str(summary).lower()
        )
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)
        logger.info(f"Request URL: {response.request.url}")
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame.from_records(data)
        return df
        

    def request(
                self,
                station: str, 
                starttime: str, #Examples: 2012-01-01T00:00:00 or 2012-01-01 Defaults to first date available.
                endtime: str, #Examples: 2012-03-01T00:00:00 or 2012-03-01 Defaults to last date available.
                analysisCenter: typing.Literal["cwu", "nmt", "pbo"] = "cwu",
                referenceFrame: typing.Literal["nam14", "igs14", "nam08", "igs08"] = "nam14",
                report: typing.Literal["short", "long"] = "short",
                dataPostProcessing: typing.Literal["Uncleaned", "Cleaned"] = "Uncleaned",
                refCoordOption: typing.Literal["from_analysis_center", "first_epoch"] = "from_analysis_center"
            ) -> pd.DataFrame:
        """
        Request GNSS data from the UNAVCO repository.

        Read API query parameters documentation for more details:
            https://www.unavco.org/data/web-services/documentation/documentation.html#!/GNSS47GPS/getPositionByStationId

        An example API request URL:
            https://web-services.unavco.org/gps/data/position/P201/v3?start=2020-01-01&end=2020-01-02
        """
        url = f"{self.base_url}/gps/data/position/{station}/v3"
        params = dict(
            starttime=starttime,
            endtime=endtime,
            analysisCenter=analysisCenter,
            referenceFrame=referenceFrame,
            report=report,
            dataPostProcessing=dataPostProcessing,
            refCoordOption=refCoordOption
        )
        response = requests.get(url, params=params)
        logger.info(f"Request URL: {response.url}")
        # response = requests.get(url)
        response.raise_for_status()

        if response.headers.get('Content-Type') != self.expected_format:
            raise ValueError("Unexpected response format")

        #TODO parse header data as metadata
        df = pd.read_csv(io.StringIO(response.text), comment='#')
        #df.set_index('Datetime', inplace=True)

        # Remove leading/trailing whitespace from column names
        df.columns = [col.strip() for col in df.columns]

        return df

