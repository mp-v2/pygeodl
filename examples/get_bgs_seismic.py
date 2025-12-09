"""
Example: Get Seismic event data from BGS repository
"""

import pygeodl.seismic as seismic

downloader = seismic.bgs()

# Download data
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

print(df.head())