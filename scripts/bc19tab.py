#! /usr/bin/env python
import argparse
from binc19 import plots_and_tables as pat


ap = argparse.ArgumentParser()
ap.add_argument('geo', help="One of Country/State/County/Congress/CSA/Native/Urban",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'])
ap.add_argument('-l', '--highlight', help="Rows to highlight.  Must be identical to "
                "value in col.  In not Key col, set --hcol as well.", default=None)
ap.add_argument('--hcol', dest='highlight_col', help="Name of column for highlight.",
                default='Key')
ap.add_argument('--lcol', dest='label_col', help="Column name to use for labels.  'hcol' "
                "will use the highlight column name.", default='hcol')
args = ap.parse_args()

sets = [x.capitalize() for x in args.set.split(',')]
if args.highlight is not None:
    args.highlight = args.highlight.split(',')
if args.label_col == 'hcol':
    args.label_col = args.highlight_col
if args.states is not None:
    if args.geo not in ['State', 'County', 'Congress']:
        print("Can't filter on states for {}".format(args.geo))
        args.states = None
    else:
        args.states = args.states.split(',')

pat.time_table()
