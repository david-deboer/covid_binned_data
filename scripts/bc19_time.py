#! /usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from binc19 import viewer


ap = argparse.ArgumentParser()
ap.add_argument('set', help="Confirmed and/or Deaths")
ap.add_argument('geo', help="Country/State/County/Congress/CSA/Urban",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban'])
ap.add_argument('--highlight', help='Highlight.', default=None)
ap.add_argument('--col', dest='highlight_col', help="Name of column for highlight.", default='Key')
ap.add_argument('-p', '--plot-type', dest='plot_type', help="logslope/slope/row",
                choices=['logslope', 'slope', 'row'], default='row')
args = ap.parse_args()

sets = [x.capitalize() for x in args.set.split(',')]
if args.highlight is not None:
    args.highlight = args.highlight.split(',')


for i, set in enumerate(sets):
    filename = "Bin_{}_{}.csv".format(set, args.geo)
    b = viewer.View(filename)
    plot_func = getattr(b, 'plot_{}'.format(args.plot_type))
    for key in b.Key:
        plot_func(key, colname='Key', figname=filename, color='0.5', label=None)
    if args.highlight is not None:
        for hl in args.highlight:
            plot_func(hl, colname=args.highlight_col, figname=filename,
                      linewidth=3, label=hl)

plt.legend()
plt.yscale('log')
plt.show()
