#! /usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from binc19 import mapit

ap = argparse.ArgumentParser()
ap.add_argument('--set', default='Confirmed',
                help="Confirmed or Deaths (csv-list)",
                choices=['Confirmed', 'Deaths'])
ap.add_argument('-g', '--geo', default='County',
                help="One of Country/State/County/Congress/CSA/Urban/Native",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native',
                         'country', 'state', 'county', 'congress', 'csa', 'urban', 'native'])
ap.add_argument('-p', '--plot-type', dest='stat_type', help="One of logslope/slope/row/accel/frac",
                default='slope')
ap.add_argument('-s', '--smooth', help="Smooth factor (int)", default=0)
ap.add_argument('-i', '--ind', help='index type to plot', default=-1)
ap.add_argument('--low-clip', dest='low_clip', help="low clip value for logslope", default=1E-4)
ap.add_argument('--loglin', help="log or linear", choices=['log', 'linear', 'auto'], default='auto')
ap.add_argument('--no-extrasmooth', dest='extrasmooth', help="Remove second smoothing on slope",
                action='store_false')
ap.add_argument('--smoothfix', help="Type of smooth-ending fix", choices=['none', 'cull', 'redo'],
                default='cull')
args = ap.parse_args()

args.set = args.set.capitalize()
if args.geo.lower() == 'csa':
    args.geo = 'CSA'
else:
    args.geo = args.geo.capitalize()

if args.smooth:
    try:
        args.smooth = float(args.smooth)
    except ValueError:
        args.smooth = False
    if args.smooth:
        print("Smoothing at {:.0f}".format(args.smooth))

try:
    args.ind = int(args.ind)
except ValueError:
    pass

mapit.map(cset=args.set, geo=args.geo,
          stat_type=args.stat_type, ind=args.ind,
          smooth=args.smooth, low_clip=args.low_clip, log_or_linear=args.loglin,
          extra_smooth=args.extrasmooth, smooth_fix=args.smoothfix
          )

# import datetime
# event = datetime.datetime(year=2020, month=6, day=20)
# plt.plot(event, 100, 'o')
plt.show()
