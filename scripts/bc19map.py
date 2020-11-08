#! /usr/bin/env python
import matplotlib.pyplot as plt
from binc19 import mapit, args_proc, binc_util

ap = args_proc.args_setup(set='Confirmed', low_clip=None)
ap.add_argument('-u', '--using', help="using data [int, diff, percent, last] "
                " diff/percent/last use bounds from data-bounds", default='percent')
ap.add_argument('--data-bounds', dest='data_bounds', default='7',
                help="data bounds for using=diff, percent, last")
ap.add_argument('--datamax', help='Max data for clip.', default=None)
ap.add_argument('--iso_state', help='Isolate on state', default=None)
args = ap.parse_args()
args = args_proc.args_prep(args)

if args.datamax is not None:
    args.datamax = float(args.datamax)

try:
    args.using = int(args.using)
except ValueError:
    pass

if args.using in ['diff', 'percent', 'last']:
    db = binc_util.fix_lists(args.data_bounds, 0, int)
    if len(db) == 1:
        args.data_bounds = [[-1-2*db[0], -1-db[0]], [-1-db[0], -1]]
    elif len(db) == 2:
        args.data_bounds = [[-1-(db[0]+db[1]), -1-db[0]], [-1-db[0], -1]]
    elif len(db) == 4:
        args.data_bounds = [[db[3], db[2]], [db[1], db[0]]]
    else:
        raise ValueError("Incorrect data_bounds {}".format(args.data_bounds))
    print("Using data_bounds: {}".format(args.data_bounds))

mapit.map(cset=args.set[0], geo=args.geo, stat_type=args.stat_type, using=args.using,
          smooth=args.smooth, smooth_fix=args.smooth_fix, smooth_schedule=args.smooth_schedule,
          low_clip=args.low_clip, log_or_linear=args.loglin,
          datamax=args.datamax, iso_state=args.iso_state, data_bounds=args.data_bounds)

# import datetime
# event = datetime.datetime(year=2020, month=6, day=20)
# plt.plot(event, 100, 'o')
plt.show()
