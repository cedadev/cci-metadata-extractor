import netCDF4
import pprint
from base import HandlerBase
from collections import OrderedDict
import math


class NetCDFReader(HandlerBase):

    def get_display(self, var_data, var_max, var_min):
        """
        Generate and return the display dictionary
        :param var_data: Data attributed to the variable
        :return: Display dict
        """

        display = {
            "display_max": None,
            "display_min": None,
            "color_map": self.DEFAULT_COLOR_MAP,
            "scale": "linear"
        }

        display_min = None
        display_max = None

        # Find display min
        keys = ("valid_min",)
        for key in keys:
            if hasattr(var_data, key):
                display_min = float(getattr(var_data, key))

                if display_min is not None:
                    if display_min < var_min:
                        display_min = math.floor(var_max)
            else:
                display_min = math.floor(var_min)

        # Find display max
        keys = ("valid_max",)
        for key in keys:
            if hasattr(var_data, key):
                display_max = float(getattr(var_data, key))

                if display_max is not None:
                    if display_max > var_max:
                        display_max = math.ceil(var_max)
            else:
                display_max = math.ceil(var_max)

        display["display_min"] = display_min
        display["display_max"] = display_max

        return display

    def get_type(self, data):
        """
        Get the variable type. If long_name and standard_name are the same.
        It is a coordinate
        :param data: The variable data
        :return: "primary" (default) | "coordinate"
        """

        if hasattr(data, "long_name") and hasattr(data, "standard_name"):

            if getattr(data, "long_name") == getattr(data, "standard_name"):
                return "coordinate"

        return "primary"

    def get_variables(self, netcdf_object):
        """
        Take a netcdf object and extract the variables
        :param netcdf_object: Open, netCDF file object
        :return: variable dictionary object
        """

        variables = OrderedDict()

        for var, data in netcdf_object.variables.iteritems():
            var_max = float(data[:].max())
            var_min = float(data[:].min())

            variable = {
                'default': False,
                'units': data.units,
                'statistics': {
                    'max': var_max,
                    'min': var_min
                },
                'display': self.get_display(data, var_max, var_min),
                'type': self.get_type(data)
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
