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
                help="One of Country/State/County/Congress/CSA/Urban/Native",
                choices=['Country', 'State', 'County', 'Congress', 'CSA',
                         'country', 'state', 'county', 'congress', 'csa'])
ap.add_argument('-f', '--foreground', help="Foreground rows.  Functions with <, >, : (see module)",
                default='CA-001,CA-013,CA-041,CA-055,CA-075,CA-081,CA-085,CA-095,CA-097')
ap.add_argument('-p', '--plot-type', dest='stat_type', help="One of logslope/slope/row/accel/frac",
                default='slope')
ap.add_argument('-s', '--smooth', help="Smoothing factor for each stage (if single, use for both)",
                default='7,3')
ap.add_argument('--fcol', dest='fg_col', help="Name of column for foreground.",
                default=None)
ap.add_argument('--lcol', dest='label_col', help="Column name to use for labels.",
                default='default')
ap.add_argument('--low-clip', dest='low_clip', help="low clip value for logslope", default=1E-4)
ap.add_argument('-A', '--fave', dest='fg_ave', help="Flag to include "
                "averaged foreground profile over time", action='store_true')
ap.add_argument('-T', '--ftot', dest='fg_tot', help="Flag to include "
                "totaled foreground profile over time", action='store_true')
ap.add_argument('-X', '--no-fg', dest='fg_incl', help="Flag to turn off "
                "plotting the foreground profiles.", action='store_false')
ap.add_argument('--bstates', dest='bg_states', help="If State/County/Congress "
                "you can choose a csv-list of states to include in 'background', "
                "average and total.  Use 2-letter abbreviations.", default=None)
ap.add_argument('--bave', dest='bg_ave', help="Flag to include "
                "averaged background profile over time", action='store_true')
ap.add_argument('--btot', dest='bg_tot', help="Flag to include "
                "totaled background profile over time", action='store_true')
ap.add_argument('-B', '--background', dest='bg_incl', help="Flag to turn on "
                "plotting the background profiles.", action='store_true')
ap.add_argument('--same-plot', dest='same_plot', help='put all plots in same figure',
                action='store_true')
ap.add_argument('--save-stats', dest='save_stats', help='Save ave & totals', action='store_true')
ap.add_argument('--loglin', help="log or linear", choices=['log', 'linear', 'auto'], default='auto')
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
if args.label_col == 'default':
    if args.geo == 'County':
        args.label_col = 'Name,State'
    elif args.geo in ['Congress', 'Country', 'State']:
        args.label_col = 'Key'
    elif args.geo in ['CSA', 'Urban']:
        args.label_col = 'Name,States'
    elif args.geo == 'Native':
        args.label_col = 'Name'

if args.foreground == '@':
    args.foreground = '@P{}.txt'.format(args.geo.lower())

if args.bg_states is not None:
    if args.geo not in ['State', 'County', 'Congress']:
        print("Can't filter on states for {}".format(args.geo))
        args.bg_states = None
    else:
        args.bg_states = args.states.split(',')

args.smooth = binc_util.fix_lists(args.smooth, 2, float)
args.smooth_fix = binc_util.fix_lists(args.smooth_fix, 2, str)
args.smooth_schedule = binc_util.fix_lists(args.smooth_schedule, 2, str)
for i in range(2):
    print("Smoothing at: {}, {}, {}".format(args.smooth[i],
          args.smooth_schedule[i], args.smooth_fix[i]))
if args.loglin == 'auto':
    loglinauto = {'row': 'log',
                  'logslope': 'log',
                  'slope': 'linear',
                  'accel': 'linear',
                  'frac': 'log'}
    args.loglin = loglinauto[args.stat_type]

pat.time_plot(sets=sets, geo=args.geo,
              foreground=args.foreground, foreground_col=args.fg_col,
              label_col=args.label_col, stat_type=args.stat_type, bg=args.bg_states,
              smooth=args.smooth, low_clip=args.low_clip, log_or_linear=args.loglin,
              same_plot=args.same_plot, save_stats=args.save_stats,
              fg_average=args.fg_ave, fg_total=args.fg_tot, fg_include=args.fg_incl,
              bg_average=args.bg_ave, bg_total=args.bg_tot, bg_include=args.bg_incl,
              smooth_schedule=args.smooth_schedule, smooth_fix=args.smooth_fix
              )

# import datetime
# event = datetime.datetime(year=2020, month=6, day=20)
# plt.plot(event, 100, 'o')
plt.show()
