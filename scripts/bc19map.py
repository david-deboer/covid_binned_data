#! /usr/bin/env python
import matplotlib.pyplot as plt
from binc19 import mapit, args_setup

args = args_setup.args_setup()

mapit.map(cset=args.set, geo=args.geo,
          stat_type=args.stat_type, using=args.using,
          smooth=args.smooth, low_clip=args.low_clip, log_or_linear=args.loglin,
          extra_smooth=args.extrasmooth, smooth_fix=args.smoothfix,
          datamax=args.datamax, iso_state=args.iso_state
          )

# import datetime
# event = datetime.datetime(year=2020, month=6, day=20)
# plt.plot(event, 100, 'o')
plt.show()
