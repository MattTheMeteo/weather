import boto3
from botocore import UNSIGNED
from botocore.client import Config
from os import path
from datetime import date
import re




bucket_name = 'noaa-hrrr-bdp-pds'
# Make these dynamic at some point.
prefix_path = 'hrrr.20240803/conus/'

# These are going to come in paginated.
# We need to define this to start the while?
s3_client = boto3.client('s3', config = Config(signature_version=UNSIGNED))
resp = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_path)

def get_nodd_hrrr_file_names(dayToPull: date):
    """Retrieves the index files from the NODD for the day in question.

    Args:
        date (datetime.date): the day to query
    """
    # Define bucket and prefix
    bucket_name = 'noaa-hrrr-bdp-pds'
    prefix_path = f"hrrr.{dayToPull.strftime('%Y%m%d')}/conus/"
    
    # Open an unsigned connection
    s3_client = boto3.client('s3', config = Config(signature_version=UNSIGNED))
    
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