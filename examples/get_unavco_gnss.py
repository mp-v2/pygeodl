"""
Example: Get GNSS data from UNAVCO repository
"""

import pygeodl.gnss as gnss

downloader = gnss.unavco()
df = downloader.request(station="P201", start_date="2020-01-01", end_date="2020-01-02")

print(df.head())