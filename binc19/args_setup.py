def prep_args(args):
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

