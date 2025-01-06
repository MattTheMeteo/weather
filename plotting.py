"""
Testing some ish, but I really want to make a high-res wind-barb plot you can like dynamically scale on.
More realistically, let's try a CONUS map, then the standard NOAA regions. Try to do that without having to pull
the regional files from NOAA maybe? Surely they publish the boundaries somewhere. Getting ahead of myself
""" 

# Let's try the grib2io lib! Seems dope
# https://github.com/NOAA-EMC/NCEPLIBS-g2c/archive/refs/tags/v2.0.0.tar.gz
import grib2io as g2io
fi = "/home/mlivingston/test_data/HRRR_subh_2025010501/hrrr.t01z.wrfsubhf00.grib2"
tst = g2io.open(filename=fi)
tst.read() # !!!!!

