#! /usr/bin/env python
import matplotlib.pyplot as plt
from binc19 import plots_and_tables as pat
from binc19 import args_proc

ap = args_proc.args_setup()
ap.add_argument('-r', '--rows-to-plot', dest='rows_to_plot',
                help="Rows to plot.  Functions with <, >, : (see module)",
                default='CA-001,CA-013,CA-041,CA-055,CA-075,CA-081,CA-085,CA-095,CA-097')
ap.add_argument('--col', help="Name of column to use for plot.", default=None)
ap.add_argument('--lcol', help="Column name to use for labels.", default=None)
ap.add_argument('--ave', help="Flag to include averaged profile over time",
                action='store_true')
ap.add_argument('--tot', help="Flag to include totaled profile over time",
                action='store_true')
ap.add_argument('--same-plot', dest='same_plot', help='put all plots in same figure',
                action='store_true')
ap.add_argument('--save-stats', dest='save_stats', help='Save ave & totals',
                action='store_true')
ap.add_argument('-e', '--extra_dates', help='add these dates', default=None)
ap.add_argument('-y', '--extra_y', help='csv-list of y-values for extra_dates', default=None)
args = ap.parse_args()
args = args_proc.args_prep(args)

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

pat.time_plot(sets=args.set, geo=args.geo,
              rows=args.rows_to_plot, rows_col=args.col,
              label_col=args.lcol, stat_type=args.stat_type,
              smooth=args.smooth, low_clip=args.datamin, log_or_linear=args.loglin,
              same_plot=args.same_plot, save_stats=args.save_stats,
              average=args.ave, total=args.tot,
              smooth_schedule=args.smooth_schedule, smooth_fix=args.smooth_fix
              )

if args.extra_dates is not None:
    import datetime
    use_y = None
    if args.extra_y is not None:
        use_y = [float(_x) for _x in args.extra_y.split(',')]
    for _i, this_date in enumerate(args.extra_dates.split(',')):
        ymd = [int(_x) for _x in this_date.split('-')]
        event = datetime.datetime(year=ymd[0], month=ymd[1], day=ymd[2])
        if use_y is None:
            this_y = 1000
        if len(use_y) == 1:
            this_y = use_y[0]
        else:
            this_y = use_y[_i]
        plt.plot([event, event], [0, this_y], 'k--')
plt.show()
