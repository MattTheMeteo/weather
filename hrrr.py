import s3fs
import xarray as xr
import zarr

s3 = s3fs.S3FileSystem(anon=True)

# So here we definitely need to open the root AND then the dataset we want. That's
# what Brian has done in the past with the old UoU archive.
# https://mesowest.utah.edu/html/hrrr/zarr_documentation/html/zarr_HowToDownload.html

ds = xr.open_zarr(
    store="s3://hrrrzarr/sfc/20240823/20240823_00z_fcst.zarr/80m_above_ground/UGRD",
    consolidated=True,
    storage_options={"anon": True},
)
zr = zarr.open(
    "s3://hrrrzarr/sfc/20240823/20240823_00z_fcst.zarr/80m_above_ground/UGRD",
    mode="r",
    storage_options={"anon": True},
)
zr2 = zarr.open(
    "s3://hrrrzarr/sfc/20240823/20240823_00z_fcst.zarr/80m_above_ground/UGRD/80m_above_ground/UGRD",
    mode="r",
    storage_options={"anon": True},
)

# Why wouldn't this work?
mf = xr.open_mfdataset(
    [
        "s3://hrrrzarr/sfc/20240823/20240823_00z_fcst.zarr/80m_above_ground/UGRD",
        "s3://hrrrzarr/sfc/20240823/20240823_00z_fcst.zarr/80m_above_ground/UGRD/80m_above_ground/UGRD",
    ],
    engine="zarr",
    storage_options={"anon": True},
    consolidated=True,
    mode="r",
)
plt = ds.UGRD.plot()

ax = plt.axes
fig = ax.figure

fig.savefig("hrrr_ugrd.png", dpi=300, bbox_inches="tight")
