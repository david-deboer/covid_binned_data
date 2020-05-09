#! /usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from binc19 import plots_and_tables as pat


ap = argparse.ArgumentParser()
ap.add_argument('set', nargs='?', default='Confirmed,Deaths',
                help="Confirmed and/or Deaths (csv-list)",
                choices=['Confirmed', 'Deaths', 'Confirmed,Deaths'])
ap.add_argument('geo', nargs='?', default='County',
                help="One of Country/State/County/Congress/CSA/Urban",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'])
ap.add_argument('-l', '--highlight', help="Rows to highlight.  Must be identical to "
                "value in col.  In not Key col, set --col as well.",
                default='CA-13,CA-1,CA-37,CA-73,OH-35,OH-55')
ap.add_argument('--hcol', dest='highlight_col', help="Name of column for highlight.",
                default='Key')
ap.add_argument('--lcol', dest='label_col', help="Column name to use for labels.  'hcol' "
                "will use the highlight column name.", default='Key')
ap.add_argument('-p', '--plot-type', dest='plot_type', help="One of logslope/slope/row",
                choices=['logslope', 'slope', 'row'], default='slope')
ap.add_argument('-s', '--states', dest='states', help="If State/County/Congress "
                "you can choose a csv-list of states to include in 'background', "
                "average and total.  Use 2-letter abbreviations.", default=None)
ap.add_argument('--smooth', help="Smooth factor (int)", default=7)
ap.add_argument('--low-clip', dest='low_clip', help="low clip value for logslope", default=1E-4)
ap.add_argument('--hl-ave', dest='hl_average', help="Flag to include "
                "averaged highlight profile over time", action='store_true')
ap.add_argument('--hl-tot', dest='hl_total', help="Flag to include "
                "totaled highlight profile over time", action='store_true')
ap.add_argument('--bg-ave', dest='bg_average', help="Flag to include "
                "averaged background profile over time", action='store_true')
ap.add_argument('--bg-tot', dest='bg_total', help="Flag to include "
                "totaled background profile over time", action='store_true')
ap.add_argument('-B', '--background', dest='bg_include', help="Flag to turn on "
                "plotting the background profiles.", action='store_true')
ap.add_argument('--same-plot', dest='same_plot', help='put all plots in same figure',
                action='store_true')
args = ap.parse_args()

sets = [x.capitalize() for x in args.set.split(',')]
if args.label_col == 'hcol':
    args.label_col = args.highlight_col
if args.states is not None:
    if args.geo not in ['State', 'County', 'Congress']:
        print("Can't filter on states for {}".format(args.geo))
        args.states = None
    else:
        args.states = args.states.split(',')
if args.smooth:
    try:
        args.smooth = float(args.smooth)
    except ValueError:
        args.smooth = False

pat.time_plot(sets=sets, geo=args.geo, highlight=args.highlight, highlight_col=args.highlight_col,
              label_col=args.label_col, plot_type=args.plot_type, bg=args.states,
              smooth=args.smooth, low_clip=args.low_clip, hl_average=args.hl_average,
              hl_total=args.hl_total, bg_average=args.bg_average,
              bg_total=args.bg_total, bg_include=args.bg_include,
              same_plot=args.same_plot)
plt.show()
