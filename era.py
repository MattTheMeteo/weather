'''
Let's use this file for some early work on accessing data from the EC
I don't like OOP - just make everything a function until you need the overhead
'''
#from utils.auth import get_cds_api_key
import cdsapi
import asyncio
#import httpx
import xarray as xr

async def get_era5_field(year: int, month: int):
    """_summary_

    Args:
        year (int): the year to pull
        month (int): the month to pull

    Returns:
        a file containing the ERA5 fields from the CDS API
    Get the ERA5 field given a year a month input (let's start with monthly chunks)
    Grab the netcdf data instead of the grib data. Why? Well - the grib data is
    - Not grib2
    - of no discernable format
    - netcdf4 can turn into a ZARR format easily.
    """
    c = cdsapi.Client()
    c.retrieve(
        name = 'reanalysis-era5-single-levels',
        request = {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': [
                "100m_u_component_of_wind",
                "100m_v_component_of_wind",
                "surface_solar_radiation_downwards",
                "total_cloud_cover"
            ],
            'year': '2020',
            'month': '01',
            "day": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12",
                "13", "14", "15",
                "16", "17", "18",
                "19", "20", "21",
                "22", "23", "24",
                "25", "26", "27",
                "28", "29", "30",
                "31"
            ],
            'time': [
                "00:00", "01:00", "02:00",
                "03:00", "04:00", "05:00",
                "06:00", "07:00", "08:00",
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00",
                "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"
            ],
        },
        # This only takes full paths.
        target= '/home/mlivingston/test_data/download.nc')
    return 'download.nc4'

def read_era5_nc4(pth:str):
    """Given a path to a grib file, return the metadata and form data of that file

    Args:
        pth (str): a path to the grib file in question
    """
    data = xr.open_dataset(pth, engine='cfgrib', chunks="auto")
    

def read_era5_netcdf(pth:str):
    """Given a path to a netcdf file, return the metadata and form data of that file

    Args:
        pth (str): a path to the netcdf file in question
    """
    data = xr.open_dataset(pth, engine='netcdf4', chunks="auto")
    return data

async def main():
    """
    We're fucking around for a test here.
    """
    out = await get_era5_field(year=2020, month=1)
    return out
asyncio.run(main())


