import argparse
from binc19 import binc_util


def args_setup(**kwargs):
    defaults = {'set': 'Confirmed,Deaths', 'geo': 'County', 'stat_type': 'slope',
                'smooth': '7,7', 'smooth_schedule': 'Box,Triangle', 'smooth_fix': 'none,cull',
                'loglin': None, 'datamin': 1E-4}
    for key, val in kwargs.items():
        defaults[key] = val
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', default=defaults['set'],
                    help="Confirmed and/or Deaths (csv-list; only 1 for Map)",
                    choices=['Confirmed', 'Deaths', 'Confirmed,Deaths',
                             'confirmed', 'deaths', 'confirmed,deaths'])
    ap.add_argument('-g', '--geo', default=defaults['geo'],
                    help="One of Country/State/County/Congress/CSA",
                    choices=['Country', 'State', 'County', 'Congress', 'CSA',
                             'country', 'state', 'county', 'congress', 'csa'])
    ap.add_argument('-p', '--plot-type', dest='stat_type', default=defaults['stat_type'],
                    help="One of logslope/slope/row/accel/frac",
                    choices=['logslope', 'slope', 'row', 'accel', 'frac'])
    ap.add_argument('--smooth', help="Smoothing factor per stage (if single, use for both)",
                    default=defaults['smooth'])
    ap.add_argument('--loglin', help="log or linear", choices=['log', 'linear', None],
                    default=defaults['loglin'])
    ap.add_argument('--datamin', help="minimum value (often used for clipping logslope)",
                    type=float, default=defaults['datamin'])
    ap.add_argument('--smooth-schedule', dest='smooth_schedule',
                    default=defaults['smooth_schedule'],
                    help="Smoothing for the two stages.  Options are Triangle, Box, Gaussian, "
                         "Trapezoid (basically Box for now)")
    ap.add_argument('--smooth-fix', dest='smooth_fix', default=defaults['smooth_fix'],
                    help="Type of smooth-ending fix for both stages",
                    choices=['none', 'cull', 'redo'])
    return ap


def args_prep(args):
    args.set = [x.capitalize() for x in args.set.split(',')]
    if args.geo.lower() == 'csa':
        args.geo = 'CSA'
    else:
        args.geo = args.geo.capitalize()
    args.smooth = binc_util.fix_lists(args.smooth, 2, float)
    args.smooth_fix = binc_util.fix_lists(args.smooth_fix, 2, str)
    args.smooth_schedule = binc_util.fix_lists(args.smooth_schedule, 2, str)
    for i in range(2):
        print("Smoothing stage {}: {}, {}, {}".format(i, args.smooth[i],
              args.smooth_schedule[i], args.smooth_fix[i]))
    if args.loglin is None:
        loglinauto = {'row': 'log',
                      'logslope': 'log',
                      'slope': 'linear',
                      'accel': 'linear',
                      'frac': 'log'}
        args.loglin = loglinauto[args.stat_type]
    return args
