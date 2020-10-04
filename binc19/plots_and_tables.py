from binc19 import binc, binc_util, stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from argparse import Namespace


SAME_PLOT_NAME = 'binc19'
skipping_geo = {'Congress': [9999], 'County': [0, 9999]}
prepended = ['#', '%', '@', '^', '$', '*']


def parse_rows(rows, rows_col, cset):
    fg = Namespace(proc=True, tstat=[], done=True, rows=rows, col=rows_col, cset=cset)
    if not isinstance(rows, str):
        return fg
    if rows[0] not in prepended:
        fg.rows = rows.split(',')
        return fg
    fg.done = False
    if rows[0] == '*':  # Look for "startswith"
        fg.proc = '*'
        fg.rows = rows.strip('*')
        return fg

    fg.col = 'ID'
    full_pipe = []
    for this_step in rows.split('|'):
        if this_step[0] == '@':
            with open(this_step[1:], 'r') as fp:
                for line in fp:
                    if line[0] == '*':
                        continue
                    for entry in line.split('|'):
                        if entry[0] == ':':
                            if entry[1].lower() == cset[0].lower():
                                full_pipe.append(entry.split()[1])
                        else:
                            full_pipe.append(entry.strip())
        else:
            full_pipe.append(this_step.strip())
    fg.tstat = [''] * len(full_pipe)
    for i, _p in enumerate(full_pipe):
        if '/' in _p:
            fg.tstat[i] = _p.split('/')[-1]
    fg.proc = [_xx.split('/')[0] for _xx in full_pipe]
    return fg


def process_rows(cset, geo, fg, label_col, data):
    """
    Plot command structure: RDX:N/S
        [^#%@$][><][X]:[N]/S|...

    R:
        '^'
            use the list (has to be first - can be first in a file, if @ is first here)
        '#'
            >/< Threshold on X averaged over N using stat S
        '%'
            >/< Difference X over N days using stat S
        '@'
            use the filename - in file can use ':c ' or ':d ' for cset
        '$'
            the top(>) or bottom(<) X (e.g. top 10) ranked entries for N/S
    D:  ><
    X:  either threshold or number of entries
    N:  number of days
    S:  "statistic" (slope, logslope, ...)
    """

    print("---{}---{}---".format(cset, geo))
    if fg.proc[0] == '*':
        rows_to_use = []
        for row in getattr(data, fg.col):
            if row.startswith(fg.rows):
                rows_to_use.append(row)
        fg.rows = rows_to_use
        return fg

    skipping = [0, 0]
    if fg.proc[0][0] == '^':  # Use this as "seed", copy to 'fnd' in case this is all.
        keys_this_loop = fg.proc[0][1:].split(',')
        fnd = {}
        for i, key in enumerate(keys_this_loop):
            this_key = '{:0>14d}{}'.format(i, key)
            fnd[this_key] = (key, 'seed')
        del fg.proc[0], fg.tstat[0]
    else:
        keys_this_loop = data.Key
    for this_pass, this_stat in zip(fg.proc, fg.tstat):
        print("\tProcessing {} for {}".format(this_pass, this_stat))
        fnd = {}
        R = this_pass[0]
        D = 1.0 if this_pass[1] == '>' else -1.0
        X, N = [float(x) for x in this_pass[2:].split(':')]
        Nind = -1 * (int(N) + 1)
        _N = [Nind, -1]
        dN = _N[1] - _N[0]
        if R == '^':
            print("^ must be 1st in 'proc' and can only be 1st.  Skipping {}".format(this_pass))
            continue
        elif R in ['#', '$']:
            _R = 'average'
        elif R == '%':
            _R = 'difference'
        else:
            print("{} not allowed.".format(R))
            continue
        for key in keys_this_loop:
            if geo in skipping_geo.keys():
                _tmp = key.split("-")
                try:
                    _val = int(_tmp[1])
                    if _val in skipping_geo[geo]:  # skipping unassigned
                        skipping[0] += 1
                        skipping[1] += data.row(key)[-1]
                        continue
                except ValueError:
                    pass
            lbl = []
            this_ind = data.rowind(key, colname='Key')
            for lc in label_col:
                lbl.append(getattr(data, lc)[this_ind])
            lbl = ", ".join(lbl)
            V2chk = stats.get_derived_value(_R, _N,
                                            data.st_date[this_stat], data.st_data[this_stat][key])
            _s = "{:30s} {:f} {} {} over {} days".format(lbl, V2chk, data.stats.unit, _R, dN)
            if D * V2chk >= D * X or R == '$':
                fnd["{:0>14d}{}".format(int(10000*V2chk), key)] = (key, _s)
        keys_this_loop = []
        if R == '$':
            if D > 0.0:
                sort_reverse = True
            else:
                sort_reverse = False
            sorted_keys = sorted(list(fnd.keys()), reverse=sort_reverse)
            threshhold_fnd = {}
            for soke in sorted_keys[:int(X)]:
                keys_this_loop.append(fnd[soke][0])
                threshhold_fnd[soke] = fnd[soke]
            fnd = threshhold_fnd
        else:
            for expkey, val in fnd.items():
                keys_this_loop.append(val[0])

    fg.rows = []
    sfk = sorted(list(fnd.keys()), reverse=True)
    for i, this_one in enumerate(sfk):
        fg.rows.append(fnd[this_one][0])
        print("{:02d}  {}".format(i+1, fnd[this_one][1]))
    if skipping[0]:
        print("Skipping:  {}".format(skipping))
    if not len(fg.rows):
        fg.proc = False
    else:
        fg.proc = True
    return fg


def time_plot(sets=['Confirmed', 'Deaths'], geo='County',
              rows=['CA-13', 'CA-1', 'CA-37', 'CA-73', 'OH-35', 'OH-55'],
              rows_col='Key', label_col='Name,State', stat_type='row',
              **kwargs):
    """
    Plot time sequences.

    Parameters
    ----------
    sets : list of str
        'Confirmed' and/or 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'
    rows : str, list of str or None
        Rows to plot.  See 'process_rows'
    rows_col : str
        Name of column for above.
    label_col : str
        Name of column to use as labels for rowsed data
    stat_type : str
        'row', 'slope', 'logslope', 'accel', 'frac' (use :two for piped rows)
    kwargs:
        average : bool
        total : bool
        smooth : list
        low_clip : None or float
        kernel : None or str
        same_plot : bool
        save_stats : bool
        log_or_linear : str
    """
    fg_dict = {'average': False, 'total': False}
    average, total = binc_util.proc_kwargs(kwargs, fg_dict)
    other_dict = {'same_plot': False, 'save_stats': False, 'log_or_linear': 'log'}
    log_or_linear, same_plot, save_stats = binc_util.proc_kwargs(kwargs, other_dict)
    if not isinstance(label_col, list):
        label_col = label_col.split(',')

    figname = None
    if same_plot:
        figname = SAME_PLOT_NAME
    for i, cset in enumerate(sets):
        data_out = {'dates': [], 'tot': [], 'ave': []}
        filename = "Bin_{}_{}.csv".format(cset, geo)
        if figname != SAME_PLOT_NAME:
            figname = filename
        b = binc.Binc(filename)
        fg = parse_rows(rows, rows_col, cset)
        for sts in set(fg.tstat + [stat_type]):
            b.calc(sts, **kwargs)
        if not fg.done:
            fg = process_rows(cset, geo, fg, label_col, b)
        fig = plt.figure(figname, figsize=[6, 8])
        vtot = np.zeros(len(b.data[0]))
        vcnt = 0
        b.plot(stat_type, fg.rows, colname=fg.col, figname=figname, linewidth=3,
               label=label_col, **kwargs)
        if total or average:
            for this_fg in fg.rows:
                try:
                    vtot += b.row(this_fg, colname=fg.col)
                except TypeError:
                    continue
                vcnt += 1
            _xx, _yyt = b.stats.calc(b.dates, vtot)
            _xx, _yya = b.stats.calc(b.dates, vtot / vcnt)
            data_out['dates'] = _xx
            if total:
                data_out['tot'] = _yyt
                plt.plot(_xx, _yyt, color='tab:olive', linewidth=4, label='Total', linestyle='--')  # noqa
            if average:
                data_out['ave'] = _yya
                plt.plot(_xx, _yya, color='tab:olive', linewidth=4, label='Average')
        if save_stats:
            with open('{}_stats.dat'.format(cset), 'w') as fp:
                fp.write("Date\t")
                for stat in ['tot', 'ave']:
                    if len(data_out[stat]):
                        fp.write("{}\t".format(stat))
                fp.write('\n')
                for i, date in enumerate(data_out['dates']):
                    fp.write("{}\t".format(datetime.strftime(date, '%Y-%m-%d')))
                    for stat in ['tot', 'ave']:
                        if len(data_out[stat]):
                            fp.write("{}\t".format(data_out[stat][i]))
                    fp.write('\n')
        plt.legend(loc='upper left')
        plt.grid()
        plt.title("{}".format(cset))
        plt.ylabel(b.stats.unit)
        # if log_or_linear == 'log' and this_stat_type != 'logslope':
        #     plt.axis(ymin=1.0)
        plt.yscale(log_or_linear)
        fig.autofmt_xdate()
        save_the_figure = False
        if save_the_figure:
            figfileName = ("{}{}{}.png"
                           .format(cset, geo, datetime.strftime(datetime.now(), "%Y%m%d")))
            figfileName = "{}{}.png".format(cset, geo)
            plt.savefig(figfileName)


def time_table(rows='6-13', date=14, geo='County', rows_col='Key', label_col='County'):
    """
    Table for 'rows'.

    Parameters
    ----------
    date : int, list-pair of str/datetime
        If int, uses the last 'date' days.
        If pair, start and stop dates
    rows : list of str
        Rows to overplot
    rows : str
        Name of column for above
    label_col : str
        Name of column to use as labels
    """
    from tabulate import tabulate
    filename = "Bin_Confirmed_{}.csv".format(geo)
    confirmed = binc.Binc(filename)
    filename = "Bin_Deaths_{}.csv".format(geo)
    deaths = binc.Binc(filename)

    if isinstance(date, list):
        start = binc_util.string_to_date(date[0])
        stop = binc_util.string_to_date(date[1])
    else:
        stop = confirmed.dates[-1]
        start = binc_util.string_to_date(date)
        if start is None:
            num_days = int(date)
            start = stop - timedelta(days=(num_days - 1))
        else:
            num_days = (stop - start).days

    headers = ['Date', 'Confirmed', 'Deaths']
    row_confirmed = confirmed.row(rows, colname=rows_col)
    row_deaths = deaths.row(rows, colname=rows_col)
    title = confirmed.meta(label_col, rows, rows_col)
    table_data = []
    for i in range(num_days):
        this_date = start + timedelta(days=i)
        ind = confirmed.dates.index(this_date)
        table_data.append([binc_util.date_to_string(this_date),
                           row_confirmed[ind], row_deaths[ind]])
    table = tabulate(table_data, headers=headers, tablefmt='orgtbl')
    max_line = 0
    for line in table.splitlines():
        if len(line) > max_line:
            max_line = len(line)
    title_line = int((max_line - len(title)) / 2.0) - 1
    extra = max_line - (title_line * 2 + 2 + len(title))
    print("|{}{}{}{}|".format('_'*title_line, title, '_'*title_line, '_'*extra))
    print("|{}{}|".format(' ' * (title_line * 2 + len(title)), ' '*extra))
    print(table)
