import zarr

store = zarr.open("s3://hrrrzarr/", read_only=True, storage_options={"anon": True})
