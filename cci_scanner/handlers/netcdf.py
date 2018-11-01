import netCDF4
import pprint
from base import HandlerBase


class NetCDFReader(HandlerBase):
    IGNORE_VARS = ('time', 'lat', 'lon')

    def get_display(self, var_data):
        """
        Generate and return the display dictionary
        :param var_data: Data attributed to the variable
        :return: Display dict
        """

        display = {
            "display_max": None,
            "display_min": None,
            "color_map": self.DEFAULT_COLOR_MAP
        }

        # Find display min
        keys = ("valid_min",)
        for key in keys:
            if hasattr(var_data, key):
                display["display_min"] = float(getattr(var_data, key))

        # Find display min
        keys = ("valid_max",)
        for key in keys:
            if hasattr(var_data, key):
                display["display_max"] = float(getattr(var_data, key))

        return display

    def get_variables(self, netcdf_object):
        """
        Take a netcdf object and extract the variables
        :param netcdf_object: Open, netCDF file object
        :return: variable dictionary object
        """

        variables = {}

        for var, data in netcdf_object.variables.iteritems():
            variable = {
                'default': False,
                'units': data.units,
                'max': float(data[:].max()),
                'min': float(data[:].min()),
                'display': self.get_display(data),
                'type': "primary"
            }

            # Add the variable metadata to the main dictionary
            variables[var] = variable

        return variables

    def get_metadata(self):
        """
        Open the file object and extract the variables
        :return: Variables Dict object
        """

        with netCDF4.Dataset(self.filepath) as netcdf_object:
            variables = self.get_variables(netcdf_object)

        return variables
