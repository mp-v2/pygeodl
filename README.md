# pygeodl

Download geoscience data with ease.

Currently suopports:
- UNAVCO: GNSS
- BGS: Seismic events

Feel free to request other data sources be added, via [GitHub issues](https://github.com/mp-v2/pygeodl/issues/new).

## Installation

You can install `pygeodl` using pip:

```bash
pip install pygeodl
```

If you want to install it directly from the repository, you can do:

```bash
pip install git+https://github.com/mp-v2/pygeodl.git
```

## Usage

Here is a simple example of how to use `pygeodl` to download GNSS data from the UNAVCO repository.

```python
import pygeodl.gnss as gnss

# Create a downloader instance for UNAVCO
downloader = gnss.unavco()

# Find stations in a bounding box
df_stations = downloader.find(
    minlatitude=43.0,
    maxlatitude=60.0,
    minlongitude=-122.0,
    maxlongitude=-120.0,
    starttime="2012-01-01",
    endtime="2025-01-01",
)

print(df_stations.head())

# Request data for a specific station and time period
df = downloader.request(station="P201", starttime="2020-01-01", endtime="2020-01-02")

# Print the first few rows of the dataframe
print(df.head())
```

This will output a pandas DataFrame with the requested GNSS data.

## Examples

Working example scripts can be found in the examples folder.
- examples/get_unavco_gnss.py
- examples/get_bgs_seismic.py
