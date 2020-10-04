#! /usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from binc19 import plots_and_tables as pat
from binc19 import binc_util


ap = argparse.ArgumentParser()
ap.add_argument('--set', default='Confirmed,Deaths',
                help="Confirmed and/or Deaths (csv-list)",
                choices=['Confirmed', 'Deaths', 'Confirmed,Deaths'])
ap.add_argument('-g', '--geo', default='County',
                help="One of Country/State/County/Congress/CSA",
                choices=['Country', 'State', 'County', 'Congress', 'CSA',
                         'country', 'state', 'county', 'congress', 'csa'])
ap.add_argument('-r', '--rows-to-plot', dest='rows_to_plot',
                help="Rows to plot.  Functions with <, >, : (see module)",
                default='CA-001,CA-013,CA-041,CA-055,CA-075,CA-081,CA-085,CA-095,CA-097')
ap.add_argument('--stat-type', dest='stat_type', help="One of logslope/slope/row/accel/frac",
                default='slope')
ap.add_argument('--smooth', help="Smoothing factor per stage (if single, use for both)",
                default='7,3')
ap.add_argument('--col', help="Name of column to use for plot.", default=None)
ap.add_argument('--lcol', help="Column name to use for labels.", default=None)
ap.add_argument('--low-clip', dest='low_clip', help="low clip value for logslope", default=1E-4)
ap.add_argument('--ave', help="Flag to include averaged profile over time",
                action='store_true')
ap.add_argument('--tot', help="Flag to include totaled profile over time",
                action='store_true')
ap.add_argument('--same-plot', dest='same_plot', help='put all plots in same figure',
                action='store_true')
ap.add_argument('--save-stats', dest='save_stats', help='Save ave & totals', action='store_true')
ap.add_argument('--loglin', help="log or linear", choices=['log', 'linear', None], default=None)
ap.add_argument('--smooth-schedule', dest='smooth_schedule', help="Smoothing for the two stages.  "
                "Options are Triangle, Box, Gaussian, Trapezoid (basically Box for now)",
                default='Box,Triangle')
ap.add_argument('--smooth-fix', dest='smooth_fix', help="Type of smooth-ending fix for both stages",
                default='none,cull', choices=['none', 'cull', 'redo'])
args = ap.parse_args()

sets = [x.capitalize() for x in args.set.split(',')]
if args.geo.lower() == 'csa':
    args.geo = 'CSA'
else:
    args.geo = args.geo.capitalize()

# Set defaults
if args.col is None:
    if args.geo == 'County':
        args.col = 'Key'
    elif args.geo == 'Country':
        args.col = 'Name'
    elif args.geo == 'State':
        args.col = 'Abbrev'
    elif args.geo == 'Congress':
        args.col = 'District'
    elif args.geo == 'CSA':
        args.col = 'Key'

if args.lcol is None:
    if args.geo == 'County':
        args.lcol = 'Name,State'
    elif args.geo == 'Country':
        args.lcol = 'Name'
    elif args.geo == 'State':
        args.lcol = 'Name'
    elif args.geo == 'Congress':
        args.lcol = 'District'
    elif args.geo == 'CSA':
        args.lcol = 'Name,States'

if args.rows_to_plot == '@':
    args.rows_to_plot = '@P{}.txt'.format(args.geo.lower())

args.smooth = binc_util.fix_lists(args.smooth, 2, float)
args.smooth_fix = binc_util.fix_lists(args.smooth_fix, 2, str)
args.smooth_schedule = binc_util.fix_lists(args.smooth_schedule, 2, str)
for i in range(2):
    print("Smoothing at: {}, {}, {}".format(args.smooth[i],
          args.smooth_schedule[i], args.smooth_fix[i]))
if args.loglin is None:
    loglinauto = {'row': 'log',
                  'logslope': 'log',
                  'slope': 'linear',
                  'accel': 'linear',
                  'frac': 'log'}
    args.loglin = loglinauto[args.stat_type]

pat.time_plot(sets=sets, geo=args.geo,
              rows=args.rows_to_plot, rows_col=args.col,
              label_col=args.lcol, stat_type=args.stat_type,
              smooth=args.smooth, low_clip=args.low_clip, log_or_linear=args.loglin,
              same_plot=args.same_plot, save_stats=args.save_stats,
              average=args.ave, total=args.tot,
              smooth_schedule=args.smooth_schedule, smooth_fix=args.smooth_fix
              )

# import datetime
# event = datetime.datetime(year=2020, month=6, day=20)
# plt.plot(event, 100, 'o')
plt.show()
