"""
Example: Get GNSS data from UNAVCO repository
"""

import pygeodl.gnss as gnss

downloader = gnss.unavco()

# Find available stations
df_stations = downloader.find(
    minlatitude=43.0,
    maxlatitude=60.0,
    minlongitude=-122.0,
    maxlongitude=-120.0,
    starttime="2012-01-01",
    endtime="2025-01-01",
)

print(df_stations.head())

# Download data
df = downloader.request(station="P201", starttime="2020-01-01", endtime="2020-01-02")

print(df.head())
