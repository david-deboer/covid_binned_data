from binc19 import viewer, binc_util, stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from argparse import Namespace


SAME_PLOT_NAME = 'binc19'


def plot_type_unit(plot_type):
    if plot_type == 'row':
        return 'count'
    elif plot_type == 'slope':
        return 'count/day'
    elif plot_type == 'logslope':
        return '1/day'
    elif plot_type == 'accel':
        return 'count/day/day'


def process_highlight(set, geo, highlight, highlight_col, plot_type, data, **kwargs):
    """
    If starts with '>' or '<' it will threshold on the following number averaged
        over N days as per  <X:N
    If ':p:X:N', it will use if difference is >= X over N days
    If ':n:X:N', it will use if difference is <= X over N days
    """
    hl = Namespace(proc=True, highlight=highlight, col=highlight_col)
    if not isinstance(highlight, str):
        return hl
    if highlight[0] not in ['<', '>', ':']:
        hl.highlight = highlight.split(',')
        return hl
    hl.highlight = []
    hl.col = 'Key'
    print("---{}---".format(set))
    print("Processing {}".format(highlight))
    skipping = [0, 0]
    if highlight[0] in ['<', '>']:
        _u = plot_type_unit(plot_type)
        hldir = 1.0 if highlight[0] == '<' else -1.0
        thold, tave = [float(x) for x in highlight[1:].split(':')]
        for key in data.Key:
            if geo in ['County', 'Congress']:
                _tmp = key.split("-")
                try:
                    _val = int(_tmp[1])
                    if geo == 'Congress' and _val == 9999:  # skipping unassigned
                        skipping[0] += 1
                        skipping[1] += data.row(key)[-1]
                        continue
                    elif geo == 'County' and _val == 0:  # skipping unassigned
                        skipping[0] += 1
                        skipping[1] += data.row(key)[-1]
                        continue
                except ValueError:
                    pass
            A, Y = stats.stat_dat(data.dates, data.row(key), dtype=plot_type, **kwargs)
            get_an_ave = 0.0
            for i in range(int(tave)):
                get_an_ave = Y[-1-i]
            get_an_ave /= tave
            if hldir * get_an_ave <= hldir * thold:
                print("{:20s}  {:.1f}  {}".format(key, get_an_ave, _u))
                hl.highlight.append(key)
    elif highlight[0] == ':':
        _u = plot_type_unit(plot_type) + '/day'
        D, X, N = highlight[1:].split(':')
        D = 1.0 if D == 'p' else -1.0
        N = -1 * (int(N) + 1)
        X = D * float(X)
        for key in data.Key:
            dx = (data.dates[-1] - data.dates[N]).days
            if geo in ['County', 'Congress']:
                _tmp = key.split("-")
                try:
                    _val = int(_tmp[1])
                    if geo == 'Congress' and _val == 9999:  # skipping unassigned
                        skipping[0] += 1
                        skipping[1] += data.row(key)[-1]
                        continue
                    elif geo == 'County' and _val == 0:  # skipping unassigned
                        skipping[0] += 1
                        skipping[1] += data.row(key)[-1]
                        continue
                except ValueError:
                    pass
            A, Y = stats.stat_dat(data.dates, data.row(key), dtype=plot_type, **kwargs)
            dn = D * (Y[-1] - Y[N])
            if dn / dx >= X:
                print("{:20s}  {:f} {}".format(key, dn / dx, _u))
                hl.highlight.append(key)

    if skipping[0]:
        print("Skipping:  {}".format(skipping))
    if not len(hl.highlight):
        hl.proc = False
    else:
        hl.proc = True
    return hl


def time_plot(sets=['Confirmed', 'Deaths'], geo='County',
              highlight=['CA-13', 'CA-1', 'CA-37', 'CA-73', 'OH-35', 'OH-55'],
              highlight_col='Key', label_col='Name,State', plot_type='row', bg=['CA'],
              **kwargs):
    """
    Plot time sequences.

    Parameters
    ----------
    sets : list of str
        'Confirmed' and/or 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'
    highlight : str, list of str or None
        Rows to overplot.  See 'process_highlight'
    highlight_col : str
        Name of column for above.
    label_col : str
        Name of column to use as labels for highlighted data
    plot_type : str
        'row', 'slope', 'logslope'
    bg : list of str
        For State, County, or Congress can limit background/stats to states.
        If None, background is all.
    kwargs:
        bg_average : bool
        bg_total : bool
        bg_include : bool
        hl_average : bool
        hl_total : bool
        hl_include : bool
        smooth : None or int
        low_clip : None or float
        kernel : None or str
        same_plot : bool
        save_stats : bool
        log_or_linear : str
    """
    bg_dict = {'bg_average': False, 'bg_include': False, 'bg_total': False}
    bg_average, bg_include, bg_total = binc_util.proc_kwargs(kwargs, bg_dict)
    hl_dict = {'hl_average': False, 'hl_total': False, 'hl_include': True}
    hl_average, hl_include, hl_total = binc_util.proc_kwargs(kwargs, hl_dict)
    other_dict = {'same_plot': False, 'save_stats': False, 'log_or_linear': 'log'}
    log_or_linear, same_plot, save_stats = binc_util.proc_kwargs(kwargs, other_dict)

    bg_proc = bg_average or bg_total or bg_include
    if not bg_proc and highlight is None:
        print("Neither highlight nor background chosen.")
        return

    figname = None
    if same_plot:
        figname = SAME_PLOT_NAME
    for i, set in enumerate(sets):
        data_out = {'dates': [], 'bg_tot': [], 'bg_ave': [], 'hl_tot': [], 'hl_ave': []}
        filename = "Bin_{}_{}.csv".format(set, geo)
        if figname != SAME_PLOT_NAME:
            figname = filename
        b = viewer.View(filename)
        hl = process_highlight(set, geo, highlight, highlight_col, plot_type, b, **kwargs)
        fig = plt.figure(figname)
        if bg_proc:
            bg_vtot = np.zeros(len(b.data[0]))
            bg_vcnt = 0
            bg_keys = []
            for i, key in enumerate(b.Key):
                if bg is None or b.State[i] in bg:
                    bg_vtot += b.row(key, colname='Key')
                    bg_vcnt += 1
                    bg_keys.append(key)
            if bg_include and len(bg_keys):
                b.plot(plot_type, bg_keys, colname='Key', figname=figname, color='0.7', label=None,
                       **kwargs)
            if len(bg_keys) and (bg_total or bg_average):
                _xx, _yyt = stats.stat_dat(b.dates, bg_vtot, dtype=plot_type, **kwargs)
                _xx, _yya = stats.stat_dat(b.dates, bg_vtot / bg_vcnt, dtype=plot_type, **kwargs)
                data_out['dates'] = _xx
                if bg_total:
                    data_out['bg_tot'] = _yyt
                    plt.plot(_xx, _yyt, color='k', linewidth=4, label='Total', linestyle='--')
                if bg_average:
                    data_out['bg_ave'] = _yya
                    plt.plot(_xx, _yya / bg_vcnt, color='0.4', linewidth=4, label='Average')
        if hl.proc:
            hl_vtot = np.zeros(len(b.data[0]))
            hl_vcnt = 0
            if hl_include:
                b.plot(plot_type, hl.highlight, colname=hl.col, figname=figname, linewidth=3,
                       label=label_col, **kwargs)
            if hl_total or hl_average:
                for this_hl in hl.highlight:
                    hl_vtot += b.row(this_hl, colname=hl.col)
                    hl_vcnt += 1
                _xx, _yyt = stats.stat_dat(b.dates, hl_vtot, dtype=plot_type, **kwargs)
                _xx, _yya = stats.stat_dat(b.dates, hl_vtot / hl_vcnt, dtype=plot_type, **kwargs)
                data_out['dates'] = _xx
                if hl_total:
                    data_out['hl_tot'] = _yyt
                    plt.plot(_xx, _yyt, color='tab:olive', linewidth=4, label='Total', linestyle='--')  # noqa
                if hl_average:
                    data_out['hl_ave'] = _yya
                    plt.plot(_xx, _yya, color='tab:olive', linewidth=4, label='Average')
        if save_stats:
            with open('{}_stats.dat'.format(set), 'w') as fp:
                fp.write("Date\t")
                for stat in ['hl_tot', 'hl_ave', 'bg_tot', 'bg_ave']:
                    if len(data_out[stat]):
                        fp.write("{}\t".format(stat))
                fp.write('\n')
                for i, date in enumerate(data_out['dates']):
                    fp.write("{}\t".format(datetime.strftime(date, '%Y-%m-%d')))
                    for stat in ['hl_tot', 'hl_ave', 'bg_tot', 'bg_ave']:
                        if len(data_out[stat]):
                            fp.write("{}\t".format(data_out[stat][i]))
                    fp.write('\n')
        plt.legend()
        plt.grid()
        plt.title("{}".format(set))
        plt.ylabel(plot_type_unit(plot_type))
        if log_or_linear == 'log' and plot_type != 'logslope':
            plt.axis(ymin=1.0)
        plt.yscale(log_or_linear)
        fig.autofmt_xdate()


def time_table(highlight='6-13', date=14, geo='County', highlight_col='Key', label_col='County'):
    """
    Table for 'highlight'.

    Parameters
    ----------
    date : int, list-pair of str/datetime
        If int, uses the last 'date' days.
        If pair, start and stop dates
    highlight : list of str
        Rows to overplot
    highlight : str
        Name of column for above
    label_col : str
        Name of column to use as labels
    """
    from tabulate import tabulate
    filename = "Bin_Confirmed_{}.csv".format(geo)
    confirmed = viewer.View(filename)
    filename = "Bin_Deaths_{}.csv".format(geo)
    deaths = viewer.View(filename)

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
    row_confirmed = confirmed.row(highlight, colname=highlight_col)
    row_deaths = deaths.row(highlight, colname=highlight_col)
    title = confirmed.meta(label_col, highlight, highlight_col)
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
