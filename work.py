import xarray as xr

ds = xr.open_zarr(
    "https://data.dynamical.org/noaa/hrrr/forecast-48-hour/latest.zarr?email=mwl5399@gmail.com"
)
