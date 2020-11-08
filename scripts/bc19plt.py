#! /usr/bin/env python
import matplotlib.pyplot as plt
from binc19 import plots_and_tables as pat
from binc19 import args_setup

args = args_setup.args_setup()


pat.time_plot(sets=args.set, geo=args.geo,
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
