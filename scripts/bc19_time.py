#! /usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from binc19 import viewer


ap = argparse.ArgumentParser()
ap.add_argument('set', help="Confirmed and/or Deaths (csv-list)")
ap.add_argument('geo', help="One of Country/State/County/Congress/CSA/Urban",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban'])
ap.add_argument('-l', '--highlight', help="Rows to highlight.  Must be identical to "
                "value in col.  In not Key col, set --col as well.", default=None)
ap.add_argument('--hcol', dest='highlight_col', help="Name of column for highlight.", default='Key')
ap.add_argument('--lcol', dest='label_col', help="Column name to use for labels.  None "
                "will use the highlight column name.", default=None)
ap.add_argument('-p', '--plot-type', dest='plot_type', help="One of logslope/slope/row",
                choices=['logslope', 'slope', 'row'], default='row')
ap.add_argument('-s', '--states', dest='states', help="If State/County/Congress "
                "you can choose a csv-list of states to include in 'background', "
                "average and total.  Use 2-letter abbreviations.", default=None)
ap.add_argument('-A', '--include-average', dest='include_average', help="Flag to include "
                "averaged profile over time", action='store_true')
ap.add_argument('-T', '--include-total', dest='include_total', help="Flag to include "
                "totaled profile over time", action='store_true')
ap.add_argument('-X', '--no-background', dest='include_background', help="Flag to turn off "
                "the background profiles.", action='store_false')
args = ap.parse_args()

if args.include_average or args.include_total:
    print("Average/total not implemented.")
sets = [x.capitalize() for x in args.set.split(',')]
if args.highlight is not None:
    args.highlight = args.highlight.split(',')
if args.label_col is None:
    args.label_col = args.highlight_col
if args.states is not None:
    if args.geo not in ['State', 'County', 'Congress']:
        print("Can't filter on states for {}".format(args.geo))
        args.states = None
    else:
        args.states = args.states.split(',')
        if args.geo == 'State':
            args.include_background = False

for i, set in enumerate(sets):
    filename = "Bin_{}_{}.csv".format(set, args.geo)
    b = viewer.View(filename)
    plot_func = getattr(b, 'plot_{}'.format(args.plot_type))
    for i, key in enumerate(b.Key):
        if args.states is None or b.State[i] in args.states:
            tot = -1
            # print("COMPUTE AVE/TOT HERE")
            if args.include_background:
                plot_func(key, colname='Key', figname=filename, color='0.5', label=None)
    if args.highlight is not None:
        for hl in args.highlight:
            lbl = getattr(b, args.label_col)[i]
            plot_func(hl, colname=args.highlight_col, figname=filename,
                      linewidth=3, label=lbl)

plt.legend()
plt.yscale('log')
plt.show()
