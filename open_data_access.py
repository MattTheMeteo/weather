import boto3
import botocore
import botocore.client
from datetime import date
import re
from dataclasses import dataclass

@dataclass
class hrrr_request:
    """Helper class that stores some interesting data for a typical HRRR request

    Properties:
        Contains an attribute called get_hrrr_bucket_name that contains the known name for the NODD bucket. 
    
    Returns:
        hrrr_request: a class with some information about initalization hours, forecast hours, and a date for the request.
    """
    init_hrs: tuple[int, ...]
    fcst_hrs: tuple[int, ...]
    day_to_pull: date
 
    @property
    def get_hrrr_bucket_name(self):
        return 'noaa-hrrr-bdp-pds'

def get_nodd_hrrr_idx_file_names(req_obj: hrrr_request):
    """Retrieves the index files from the NODD for the day in question.

    Args:
        req_obj (hrrr_request): a HRRR request object
    """
    # Define bucket and prefix
    bucket_name = req_obj.get_hrrr_bucket_name
    prefix_path = f"hrrr.{req_obj.day_to_pull.strftime('%Y%m%d')}/conus/"
    
    # Open an unsigned connection
    s3_client = boto3.client('s3', config = botocore.client.Config(signature_version=botocore.UNSIGNED))
    
    # Grab the data
    resp = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_path)
    # Early return.
    if not resp.get('IsTruncated'):
        pths = [match.string for file in resp.get('Contents') if (match := re.search("grib2.idx", file['Key']))]
        if pths == []:
            ValueError("No valid grib2.idx files found.")
        return(pths)
    # If paginated, create something we can append to.
    out = []
    while resp.get('IsTruncated'):
        resp = s3_client.list_objects_v2(Bucket=bucket_name, 
                                         Prefix=prefix_path,
                                         ContinuationToken=resp.get('NextContinuationToken'))
        pths = [match.string for file in resp.get('Contents') if (match := re.search("grib2.idx", file['Key']))]
        
        # We're moving nones, but not empties.
        if pths != []:
            out.append(pths) 
    if out == []:
            ValueError("No valid grib2.idx files found.")
    # Flatten the lists
    out = [i for sublist in out for i in sublist]
    return(out)

def filter_hrrr_init_forecast_hours(req_obj: hrrr_request, 
                                    pths: list[str]):
    """Given a valid HRRR request, filter NODD HRRR files down to the ones we'd like to read.
    Args: 
        req_obj (hrrr_request)
        pths (list[str]): a path to files 
    """
    # Need to extract the init and fcst hours from each path, confirm which are the ones I actually want, 
    # then return those. They'll get passed to a byte range function.
    

# Once I have IDX paths, for each:
# - take variables
# - pull byte ranges for each
# - Hit the file itself and download them.
if __name__ == '__main__':
    req = hrrr_request(init_hrs= tuple(range(0,23,1)), fcst_hrs = tuple(range(0,12,1)), day_to_pull=date(2024,8,20))
    pths = get_nodd_hrrr_idx_file_names(req_obj=req)