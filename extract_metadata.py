"""
CCI Metadata extraction tool.
Extracts metadata from the supplied dataset and returns a JSON file with metadata for each variable.

Usage:
    extract_metadata.py DATASET OUTPUT [--mapping MAPPING]


"""

from docopt import docopt
import os

from cci_scanner.processors import Dataset

args = docopt(__doc__)
kwargs = {}

if args['DATASET'].endswith("/"):
    dataset_name = os.path.basename(args['DATASET'][:-1])
else:
    dataset_name = os.path.basename(args['DATASET'])

if args['MAPPING']:
    kwargs["mapping_file"] = args["MAPPING"]

dataset = Dataset(args['DATASET'], **kwargs)

dataset.extract_metadata()

dataset.write_metadata(os.path.join(args['OUTPUT'], "display_metadata_{}.json".format(dataset.id if dataset.id else dataset_name)))
