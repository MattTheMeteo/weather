'''
Let's use this file for some early work on accessing data from the EC
'''
#from utils.auth import get_cds_api_key
import cdsapi
#import httpx

async def get_era5_field():
    '''
    Get the ERA5 field
    '''
    c = cdsapi.Client()
    c.retrieve(
        name = 'reanalysis-era5-single-levels',
        request = {
            'product_type': 'reanalysis',
            'format': 'grib',
            'variable': '2m_temperature',
            'year': '2020',
            'month': '01',
            'day': '01',
            'time': '12:00',
        },
        # This only takes full paths.
        target= '/home/mlivingston/test_data/download.grib')
    return 'download.grib'

def main():
    """
    We're fucking around for a test here.
    """
    out = get_era5_field()
    return out



