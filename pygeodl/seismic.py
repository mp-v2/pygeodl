"""
Docstring for pygeodl.seismic

This module provides functionalities for downloading seismic data.
"""

import pandas as pd
import requests
import io
import typing
from loguru import logger
from bs4 import BeautifulSoup

class bgs():
    """
    A class to handle downloading seismic data from the BGS repository.
    """

    def __init__(self):
        self.base_url = "https://earthquakes.bgs.ac.uk/cgi-bin"
        self.expected_format = "text/html; charset=ISO-8859-1"
        # Additional initialization code can go here

    def find(self, *args, **kwargs):
        """
        Method for finding available seismic stations.
        """
        pass  # Implementation goes here

    def request(
        self,
        starttime: str,
        endtime: str,
        minlatitude: typing.Optional[float] = None,
        maxlatitude: typing.Optional[float] = None,
        minlongitude: typing.Optional[float] = None,
        maxlongitude: typing.Optional[float] = None,
        centrelatitude: typing.Optional[float] = None,
        centrelongitude: typing.Optional[float] = None,
        radius: typing.Optional[float] = None,
        mindepth: typing.Optional[float] = None,
        maxdepth: typing.Optional[float] = None,
        minmag: typing.Optional[float] = None,
        maxmag: typing.Optional[float] = None,
        minnstations: typing.Optional[int] = None,
        maxnstations: typing.Optional[int] = None,
        output: typing.Literal["csv"] = "csv",
    ) -> pd.DataFrame:
        """
        Request seismic events from the BGS repository.

        For parameters, see the documentation:
        https://earthquakes.bgs.ac.uk/earthquakes/data/data_search.html

        An example API request URL:
            https://earthquakes.bgs.ac.uk/cgi-bin/get_events?lat1=49&lat2=63&lon1=-12&lon2=5&lat0=&lon0=&radius=&date1=2024-11-29&date2=2025-12-09&dep1=1&dep2=10&mag1=&mag2=&nsta1=&nsta2=&output=csv
        """
        url = f"{self.base_url}/get_events"
        params = {
            "lat1": minlatitude,
            "lat2": maxlatitude,
            "lon1": minlongitude,
            "lon2": maxlongitude,
            "lat0": centrelatitude,
            "lon0": centrelongitude,
            "radius": radius,
            "date1": starttime,
            "date2": endtime,
            "dep1": mindepth,
            "dep2": maxdepth,
            "mag1": minmag,
            "mag2": maxmag,
            "nsta1": minnstations,
            "nsta2": maxnstations,
            "output": output,
        }
        # Remove None values so they are not sent as empty parameters
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(url, params=params)
        logger.info(f"Request URL: {response.request.url}")
        response.raise_for_status()

        if response.headers.get('Content-Type') != self.expected_format:
            raise ValueError("Unexpected response format")
        
        soup = BeautifulSoup(response.text, "html.parser")
        csv_text = soup.body.get_text()
        
        known_columns = ["yyyy-mm-dd", "hh:mm:ss.ss", "lat", "lon", "depth", "magnitude", "induced", "locality", "locality2"]
        df = pd.read_csv(io.StringIO(csv_text), skipinitialspace=True, names=known_columns, skiprows=2)
        # skipinitialspace=True helps with leading spaces after commas in column names
        # skiprows=2 to skip the empty top line and the actual header line

        # Locality contains commas, so parsed as locality and locality2 columns, then combined
        df['locality'] =df['locality'].str.strip() + ", " + df['locality2'].str.strip()
        df.drop("locality2", axis=1, inplace=True)

        return df
