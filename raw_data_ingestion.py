import datetime as dt
from dataclasses import dataclass
import os
import re
from requests import get
from typing import Tuple

@dataclass
class noaa_grib_filter:
    """
    This class represents all of the potential modifiers to a grib filter call
    Attributes:
        init_dt (dt.date): the date you want to pull from the filter.
        fcst (tuple[int]): the forecast hour(s) you want to pull
        varis (tuple[str]): the forecast variable(s) you want to pull
        levs (tuple[str]): the forecast level(s) you want to pull
        init_hr (int): the hour of initialization 
    """
    init_dt: dt.date
    fcst:    Tuple[int, ...]
    varis:   Tuple[str, ...]
    levs:    Tuple[str, ...]
    init_hr: int
    model: str

    def check_noaa_vars(self) -> bool:
        """
        Simple validity on the variables passed to the class.
        Returns:
            bool: True if the values are valid
        """
        valid_vars = ["DPT", "DSWRF", "HGT", "PRES", "TMP", "UGRD", "VGRD",
                       "VBDSF", "VDDSF"]
        if (any(var not in valid_vars for var in self.varis)):
            return(False)
        else:
            return(True)
    
    def assemble_var_url(self) -> str:
        """
        Takes a number of levels associated with the grib_filter object and 
        formats it.
        Returns:
            str: returns this chunk of the url as a string
        """
        if not self.check_noaa_vars():
            return("Variable check failed, check your variables.")
        var_url = [f"&var_{var_out}=on" for var_out in self.varis]
        var_url = ''.join(var_url)
        return(var_url)
    
    def check_noaa_levs(self) -> bool:
        """
        Simple validity checker for NOAA levels
        Returns:
            bool: True if the levels are not valid.
        """
        valid_levels = ("2_m_above_ground", "10_m_above_ground", 
                        "80_m_above_ground","1000_mb", "850_mb", "700_mb",
                          "500_mb", "250_mb")
    
        if any(lev not in valid_levels for lev in self.levs):
            return(False)
        else:
            return(True)
    
    def assemble_lev_url(self) -> str:
        """
        Assembles the levels portion of the url given valid inputs.
        Returns:
            str: _description_
        """
        if not self.check_noaa_levs():
            return("Level check failed, check your levels.")
        lev_url = [f"&lev_{lev_out}=on" for lev_out in self.levs]
        lev_url = ''.join(lev_url)
        return(lev_url)
    
    def assemble_base_url(self) -> list[str]:
        """
        Generate the base URL depending on the same model selected.
        Returns:
            str: _description_
        """
        init_date = self.init_dt.strftime('%Y%m%d')
        mod_dict = {
            "HRRR_subh": [f"https://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr"
                          f"_sub.pl?dir=%2Fhrrr.{init_date}%2Fconus&file=hrrr."
                          f"t{self.init_hr:02d}z.wrfsubhf{hr:02d}.grib2"
                            for hr in self.fcst]
        }
        # This will automatically check the keys.
        if self.model in mod_dict:
            base_url = mod_dict[self.model]
            return(base_url)
        else: 
            raise NotImplementedError("Model is not implemented yet.")
    
    def assemble_dest_path(self) -> str:
        """
        Given a model and some dates, find the write place to put the data.
        Returns:
            str: a file path, currently on my local machine.
        """
        # Python does not allow for ~ to mean the user's home. It takes it
        # as a string literal.
        home = os.path.expanduser("~")
        dest_path = f"{home}/test_data/{self.model}_{self.init_dt.strftime('%Y%m%d')}{self.init_hr:02d}.grib2"

        # If it doesn't exist, make the directory.
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        return(dest_path)
    
    def pull_grib_filter(self) -> str:
        """
        Given a day, some metadata and a forecast length, assemble a valid grib_filter
        url, and pull it.

        Returns:
            str: the location of the destination file
        """
        urls = self.assemble_base_url()
        tgts = [f"{x}{self.assemble_lev_url()}{self.assemble_var_url()}" for x in urls]

        # Pull each url.
        for url in tgts:
            resp = get(url = url)
            
            if resp.status_code == 200:
                to_match = r'file=(.*?\.grib2)'
                # Null handling
                match_test = re.search(to_match, url)
                if match_test:
                    f_name = match_test.group(1)
                else:
                    AttributeError("No match found")  
                with open(f"{self.assemble_dest_path()}/{f_name}", mode = 'wb') as f:
                    f.write(resp.content)
                    return(url)
            else:
                print(f"Encountered a {resp.status_code} at {url}")
                return(f"{str(resp.status_code)} at {url}")
        raise RuntimeError("Something has gone very wrong.")
def main():
    tst = noaa_grib_filter(init_dt = dt.datetime.now(),
                           fcst=(0, 1),
                           varis = ("UGRD", "VGRD"),
                           levs = ("80_m_above_ground",),
                           init_hr = 1,
                           model = "HRRR_subh")
    out = tst.pull_grib_filter()
    return(out)

if __name__ == "__main__":
    main()










