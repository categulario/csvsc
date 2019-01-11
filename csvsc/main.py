import argparse

from csvsc import Process
from csvsc.mapper import ColSpec


def main():
    parser = argparse.ArgumentParser(description='Organizes csv files')

    # TODO allow single file, single dir, multiple files, multiple dirs or
    # combinations
    parser.add_argument('input', help='directory to analize')
    parser.add_argument('--ie', help='input encoding', default='utf-8', dest='input_encoding')
    # TODO allow file or directory
    parser.add_argument('output', help='where to store the resulting files')

    parser.add_argument(
        '-a --add-columns',
        nargs='+',
        metavar='COL_SPEC',
        dest='add_columns',
        default=[],
        type=ColSpec,
        help="columns to add to the output",
    )

    args = parser.parse_args()

    proc = Process(**vars(args))
    proc()
