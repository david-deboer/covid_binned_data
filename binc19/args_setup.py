import argparse
from binc19 import binc_util


ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser()
ap.add_argument('--set', default='Confirmed',
                help="Confirmed or Deaths (csv-list)",
                choices=['Confirmed', 'Deaths', 'confirmed', 'deaths'])
ap.add_argument('-g', '--geo', default='County',
                help="One of Country/State/County/Congress/CSA/Urban/Native",
                choices=['Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native',
                         'country', 'state', 'county', 'congress', 'csa', 'urban', 'native'])
ap.add_argument('-p', '--plot-type', dest='stat_type', help="One of logslope/slope/row/accel/frac",
                choices=['logslope', 'slope', 'row', 'accel', 'frac'], default='slope')
ap.add_argument('-s', '--smooth', help="Smooth factor (float)", type=float, default=0.0)
ap.add_argument('-u', '--using', help="using data [int, diff, percent, last] "
                " diff/percent/last use bounds from data-bounds", default='percent')
ap.add_argument('--data-bounds', dest='data_bounds',
                help="data bounds for using=diff, percent, last")
ap.add_argument('--datamax', help='Max data for clip.', default=None)
ap.add_argument('--iso_state', help='Isolate on state', default=None)
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

if args.datamax is not None:
    args.datamax = int(args.datamax)

if args.smooth:
    try:
        args.smooth = float(args.smooth)
    except ValueError:
        args.smooth = False
    if args.smooth:
        print("Smoothing at {:.0f}".format(args.smooth))

try:
    args.using = int(args.using)
except ValueError:
    pass
def args_setup():
    args.set = [x.capitalize() for x in args.set.split(',')]
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
    return args
