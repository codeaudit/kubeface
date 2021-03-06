'''
Copy files, including support for google storage buckets.
'''

import sys
import argparse
import logging

from .. import storage
from ..common import configure_logging
from .. import serialization

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument("source")
parser.add_argument("destination")

parser.add_argument(
    "--no-error",
    action="store_true",
    default=False,
    help="")

parser.add_argument(
    "--quiet",
    action="store_true",
    default=False,
    help="")

parser.add_argument(
    "--verbose",
    action="store_true",
    default=False,
    help="")

parser.add_argument(
    "--print-deserialized",
    action="store_true",
    default=False,
    help="")


def run(argv=sys.argv[1:]):
    args = parser.parse_args(argv)
    configure_logging(args)

    logging.info("Reading: %s" % args.source)
    input_handle = storage.get(args.source)

    if args.print_deserialized:
        deserialized = serialization.load(input_handle)
        input_handle.seek(0)
        print(deserialized)

    if args.destination == "-":
        print(input_handle.read())
    else:
        logging.info("Writing: %s" % args.destination)
        storage.put(args.destination, input_handle)

    logging.info("Completed.")
