from re import compile
from requests import get
import pandas as pd
import datetime as dt

def pull_hrrr_subh_grib_filter(init_date: dt.date, varis: str, levs: str, init_hour: int, fcst: int):
    '''
    Given a day, some metadata and a forecast length, assemble a valid grib_filter
    url, and pull it. 
    '''
    # Some input validation and formatting.
    init_date = init_date.strftime('%Y%m%d')
    base_url = [f"https://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_sub.pl?dir=%2Fhrrr.{init_date}%2Fconus&file=hrrr.t{init_hour:02d}z.wrfsubhf{hr:02d}.grib2" for hr in fcst]
    dest_path = "~/test_data/f'HRRR_{init_date}{init_hour:02d}'"
    # Build the rest of the URL depending on what was input.
    var_url = assemble_var_url(varis=varis)
    lev_url = assemble_lev_url(levs=levs)
    base_var = [f"{url1}{var_url}" for url1 in base_url]
    base_lev = [f"{url2}{lev_url}" for url2 in base_var]
    
    # Execute the pull
    resp = get(base_lev)
    if resp.status_code == 200:
        with open(dest_path, mode = 'wb') as f:
            f.write(resp.content)
            return(base_lev)
    else:
        print(f"Encountered a {resp.status_code} at {base_lev}")
        return([resp.status_code, base_lev])

def assemble_var_url(varis: str) -> str:
    '''
    Given some variables, check for their validaity and then assemble the piece
    of the url that will tell the grib filter what variables to pull.
    '''
    if not check_noaa_vars:
        return("Variable check failed, check your variables.")
    var_url = [f"&var_{var_out}=on" for var_out in varis]
    return(var_url)

def assemble_lev_url(levs: str) -> str:
    '''
    Given some levels, check their validity and assemble the piece of the grib
    filter url that picks what levels to select.
    '''
    if not check_noaa_levels:
        return("Level check failed, check your levels.")
    lev_url = [f"&lev_{lev_out}=on" for lev_out in levs]
    return(lev_url)

def check_noaa_levels(levs: tuple) -> bool:
    '''
    Takes one or more levels submitted by a user or process and returns whether or not they're valid.
    This does not account for individual models different fields, it just makes sure the query belongs to known
    NOAA values. 
    '''
    # Ensure this object is a list.
    levs = (levs,)
    valid_levels = ["2_m_above_ground", "10_m_above_ground", "80_m_above_ground",
                     "1000_mb", "850_mb", "700_mb", "500_mb", "250_mb"]
    
    if any(lev not in valid_levels for lev in levs):
        return(False)
    else:
        return(True)

def check_noaa_vars(vars: list) -> bool:
    '''
    Takes one or more variables submitted by a user or process and returns whether or not they're valid.
    This does not account for individual models different fields, it just makes sure the query belongs to known
    NOAA values.
    Parameters: a string or array containing some variables to pull from NOAA.
    Returns: a boolean, True when the variables exist, False if one or more does not.
    '''
    valid_vars = ["DPT", "DSWRF", "HGT", "PRES", "TMP", "UGRD", "VGRD", "VBDSF", "VDDSF"]
    if (any(var not in valid_vars for var in vars)):
        return(False)
    else:
        return(True)

    








