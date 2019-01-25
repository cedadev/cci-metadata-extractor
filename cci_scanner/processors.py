"""
This file contains classes to aide in processing different sets of information.
There is an ID object to read a CSV mapping file and translate that to a dictionary
and a Dataset object which reads an entire dataset and produces a metadata object for that dataset.

"""
__author__ = "Richard Smith"
__date__ = "26 Oct 2018"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "richard.d.smith@stfc.ac.uk"


import os
import re
from handlers.factory import HandlerFactory
import conf.defaults as defaults
import json
from tqdm import tqdm
from datetime import datetime
from collections import OrderedDict

DEFAULT_ID_MAPPING_FILE = os.path.join(os.path.dirname(__file__),"default_id_mapping/esgf_mappings.csv")
CUSTOM_MAPPING_FILE = os.path.join(os.path.dirname(__file__), "conf/custom_mapping.json")

def mergedicts(dict1, dict2):
    for key in set(dict1.keys()).union(dict2.keys()):
        if key in dict1 and key in dict2:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                yield (key, dict(mergedicts(dict1[key], dict2[key])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (key, dict2[key])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif key in dict1:
            yield (key, dict1[key])
        else:
            yield (key, dict2[key])

class IDMapping(object):
    """
    Class to read the ESGF Mapping file and provide useful endpoints
    """

    filepath_mapping = {}
    esgf_ids = []
    shortest_path = None

    def __init__(self, mapping_file):

        self._process_mapping_file(mapping_file)

    def _process_mapping_file(self, mapping_file):
        """
        Take mapping file and produce a dictionary mapping from path to id
        and a list of ids

        :param mapping_file: Path to file containing mapping between filepath
        and id in format:

            path,id
            path,id
            path,id
            ...
        """

        with open(mapping_file) as input:
            for line in input:
                path, id = line.split(",")

                if path.endswith("/"):
                    path = path[:-1]

                # Store shortest path
                if self.shortest_path is None:
                    self.shortest_path = len(path.split("/"))

                elif len(path.split("/")) < self.shortest_path:
                    self.shortest_path = len(path.split("/"))

                # Create mapping and list of ids
                self.filepath_mapping[path.strip()] = id.strip()
                self.esgf_ids.append(id.strip())

    def get_id(self, filepath):

        path = filepath

        # Recursively remove directories from the path until
        # we finds a match. Exit if we get back to root.
        while len(path.split("/")) >= (self.shortest_path if self.shortest_path else 2):

            # Exit if we have hit the root directory
            if path == "/":
                return

            # Check for match
            if self.filepath_mapping.get(path):
                return self.filepath_mapping.get(path)

            # No match, remove directory and try again
            else:
                path = os.path.dirname(path)

        return

    def match(self, pattern, string):
        return bool(re.match(pattern, string))


class Dataset(object):
    """
    Class to read datasets and produce an aggregated metadata object
    """

    dataset_metadata = OrderedDict()
    file_list = []

    def __init__(self, dataset_path, mapping_file=DEFAULT_ID_MAPPING_FILE):

        self.dataset_path = dataset_path

        # Get files in dataset
        self._get_files()

        # Initialise Handler Factory
        self.handler_factory = HandlerFactory()

        # ID mapping
        self.id = IDMapping(mapping_file).get_id(dataset_path)

        # Load any custom mappings
        with open(CUSTOM_MAPPING_FILE) as reader:
            self.custom_mapping = json.load(reader)

        print ("{} files to scan".format(len(self.file_list)))

    def _get_files(self):
        """
        Generate a list of files for the dataset
        """

        for base, _, files in os.walk(self.dataset_path):
            for file in files:
                self.file_list.append(os.path.join(base, file))

    def merge_metadata(self, file_meta):
        """
        Merge file attributes into the dataset attributes
        :param file_meta:
        """

        for key in file_meta:
            if key not in self.dataset_metadata:
                self.dataset_metadata[key] = file_meta[key]

            else:
                # min - Update min
                if self.dataset_metadata[key]['statistics']['min'] > file_meta[key]['statistics']['min']:
                    self.dataset_metadata[key]['statistics']['min'] = file_meta[key]['statistics']['min']

                # max - Update max
                if self.dataset_metadata[key]['statistics']['max'] < file_meta[key]['statistics']['max']:
                    self.dataset_metadata[key]['statistics']['max'] = file_meta[key]['statistics']['max']

                # units - Overwrite
                self.dataset_metadata[key]['units'] = file_meta[key]['units']

                # type - Overwrite
                self.dataset_metadata[key]['type'] = file_meta[key]['type']

                # display - Update min
                if self.dataset_metadata[key]['display']['display_min'] > file_meta[key]['display']['display_min']:
                    self.dataset_metadata[key]['display']['display_min'] = file_meta[key]['display']['display_min']

                # display - Update max
                if self.dataset_metadata[key]['display']['display_max'] < file_meta[key]['display']['display_max']:
                    self.dataset_metadata[key]['display']['display_max'] = file_meta[key]['display']['display_max']

    def update_defaults(self):
        """
        Update metadata based on default configuration
        """

        # Update variable defaults
        for default_var in (var for var in self.dataset_metadata if var in defaults.DEFAULT_VARIABLES):
            self.dataset_metadata[default_var].update({'default': True})

        # Update coordinate defaults
        for coord_var in (var for var in self.dataset_metadata if var in defaults.COORDINATE_VARIABLES):
            self.dataset_metadata[coord_var].update({"type": "auxiliary"})

        # Update auxilliary defaults
        for aux_var in (var for var in self.dataset_metadata if var in defaults.AUXILIARY_COORDINATES):
            self.dataset_metadata[aux_var].update({"type": "auxiliary"})

        # Update display defaults
        for display_var in (var for var in self.dataset_metadata if var in defaults.VARIABLE_DISPLAY_SETTINGS):
            self.dataset_metadata[display_var]['display'].update(defaults.VARIABLE_DISPLAY_SETTINGS[display_var])

    def update_custom(self):
        """
        Update metadata based on a custom mapping
        """

        custom_mapping = None

        # check to see if there is a custom mapping for the dataset
        if self.id:
            for pattern in self.custom_mapping:
                if re.match(pattern, self.id):
                    custom_mapping = self.custom_mapping[pattern]

        if custom_mapping is not None:
            base = self.dataset_metadata.copy()
            merged_dicts = dict(mergedicts(base, custom_mapping))

            # Re-assign order
            self.dataset_metadata = OrderedDict([(k,merged_dicts[k]) for k in base ])



    def extract_metadata(self):

        for file in tqdm(self.file_list, desc="Extracting metadata"):

            handler = self.handler_factory.get_handler(file)

            if handler:
                file_meta = handler.get_metadata()

                tqdm.write( "File procesed %s" % file)

                self.merge_metadata(file_meta)

        self.update_defaults()
        self.update_custom()

        self.dataset_metadata['metadata'] = {
            'creation_date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'dataset': self.dataset_path
        }

    def write_metadata(self, filename):

        with open(filename, 'w') as writer:
            writer.write(json.dumps(self.dataset_metadata, indent=4))
