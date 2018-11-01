import cci_scanner.conf.defaults as defaults
from abc import ABCMeta, abstractmethod

class HandlerBase:

    __metaclass__ = ABCMeta

    DEFAULT_COLOR_MAP = defaults.DEFAULT_COLOR_MAP

    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def get_metadata(self):
        pass