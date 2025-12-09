"""
Example: Get GNSS data from UNAVCO repository
"""

import pygeodl.gnss as gnss

downloader = gnss.unavco()
df = downloader.request(station="P201", starttime="2020-01-01", endtime="2020-01-02")

print(df.head())