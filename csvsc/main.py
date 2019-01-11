import argparse

from csvsc.process import Process
from csvsc.mapper import ColSpec
from csvsc.reducer import IdGrouping, Grouping, Reducer


def main():
    parser = argparse.ArgumentParser(description='Organizes csv files')

    # TODO allow single file, single dir, multiple files, multiple dirs or
    # combinations
    parser.add_argument('input', help='directory to analize')
    parser.add_argument(
        '-ie --input-encoding',
        help='input encoding',
        default='utf-8',
        dest='input_encoding',
    )
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

    parser.add_argument(
        '-g --group',
        metavar='GROUP_SPEC',
        dest='grouping',
        default=IdGrouping(),
        type=Grouping,
        help="how to group rows to compute aggregates",
    )

    parser.add_argument(
        '-r --reduce',
        nargs='+',
        metavar='REDUCER_SPEC',
        dest='reducer_columns',
        default=[],
        type=Reducer.from_spec,
        help="columns to be computed by reducing or folding other columns",
    )

    args = parser.parse_args()

    proc = Process(**vars(args))
    proc()
