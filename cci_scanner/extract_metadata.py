"""
CCI Metadata extraction tool.
Extracts metadata from the supplied dataset and returns a JSON file with metadata for each variable.

Usage:
    extract_metadata.py DATASET OUTPUT


"""

from docopt import docopt
import os
from handlers.factory import HandlerFactory
import conf.defaults as defaults
import json
from tqdm import tqdm
from datetime import datetime

class Dataset(object):
    dataset_metadata = {}
    DEFAULT_VARIABLES = defaults.DEFAULT_VARIABLES
    VARIABLE_DISPLAY_SETTINGS = defaults.VARIABLE_DISPLAY_SETTINGS

    def __init__(self, dataset_path):

        self.dataset_path = dataset_path

        self.file_list = self._get_files()

        print ("{} files to scan".format(len(self.file_list)))

        self.handler_factory = HandlerFactory()

    def _get_files(self):
        file_list = []
        for base, _, files in os.walk(self.dataset_path):
            for file in files:
                file_list.append(os.path.join(base, file))

        return file_list

    def merge_metadata(self, file_meta):
        """
        Merge file attributes into the dataset attributes
        :param file_meta:
        :return:
        """

        for key in file_meta:
            if key not in self.dataset_metadata:
                self.dataset_metadata[key] = file_meta[key]

            else:
                # min - Update min
                if self.dataset_metadata[key]['min'] > file_meta[key]['min']:
                    self.dataset_metadata[key]['min'] = file_meta[key]['min']

                # max - Update max
                if self.dataset_metadata[key]['max'] < file_meta[key]['max']:
                    self.dataset_metadata[key]['max'] = file_meta[key]['max']

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
        default_vars = [var for var in self.dataset_metadata if var in self.DEFAULT_VARIABLES]

        for var in default_vars:
            self.dataset_metadata[var].update({'default': True})

    def update_display(self):

        display_defaults = [var for var in self.dataset_metadata if var in self.VARIABLE_DISPLAY_SETTINGS]

        for default in display_defaults:
            self.dataset_metadata[default]['display'].update(self.VARIABLE_DISPLAY_SETTINGS[default])

    def extract_metadata(self):

        for file in tqdm(self.file_list, desc="Extracting metadata"):

            handler = self.handler_factory.get_handler(file)

            if handler:
                file_meta = handler.get_metadata()

                print "File procesed %s" % file

                self.merge_metadata(file_meta)

        self.update_defaults()
        self.update_display()

        self.dataset_metadata["creation_date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
    def write_metadata(self, filename):

        with open(filename, 'w') as writer:
            writer.write(json.dumps(self.dataset_metadata, indent=4))


if __name__ == '__main__':
    args = docopt(__doc__)


    if args["DATASET"].endswith("/"):
        dataset_name = os.path.basename(args['DATASET'][:-1])
    else:
        dataset_name = os.path.basename(args['DATASET'])

    dataset = Dataset(args['DATASET'])

    dataset.extract_metadata()

    dataset.write_metadata(os.path.join(args['OUTPUT'], "{}.json".format(dataset_name)))
