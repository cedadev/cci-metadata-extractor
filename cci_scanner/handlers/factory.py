import os
import netcdf


class HandlerFactory(object):

    def __init__(self):
        self.handler_map = {
            ".nc": netcdf.NetCDFReader

        }


    def get_handler(self, filename):
        """

        :param filename:
        :return:
        """

        handler = None

        extension = os.path.splitext(filename)[1]

        if extension in self.handler_map:
            handler = self.handler_map[extension]
            handler = handler(filename)

        return handler