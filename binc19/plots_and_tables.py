from binc19 import viewer, binc_util, stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from argparse import Namespace


SAME_PLOT_NAME = 'binc19'
skipping_geo = {'Congress': [9999], 'County': [0, 9999]}


def _parse_highlight(highlight, plot_type, set):
    full_pipe = []
    for this_step in highlight.split('|'):
        if this_step[0] == '@':
            with open(this_step[1:], 'r') as fp:
                for line in fp:
                    if line[0] == '*':
                        continue
                    for entry in line.split('|'):
                        if entry[0] == ':':
                            if entry[1].lower() == set[0].lower():
                                full_pipe.append(entry.split()[1])
                        else:
                            full_pipe.append(entry.strip())
        else:
            full_pipe.append(this_step.strip())
    tstat = [plot_type] * len(full_pipe)
    for i, _p in enumerate(full_pipe):
        if '/' in _p:
            tstat[i] = _p.split('/')[-1]
    proc = [_xx.split('/')[0] for _xx in full_pipe]
    return proc, tstat


def process_highlight(set, geo, highlight, highlight_col, label_col,
                      plot_type, data, **kwargs):
    """
    Highlight command structure: RDX:N/S
        [^#%@$][><][X]:[N]/S|...
    If highlight startswith:
    '^'
        use the list (has to be first - can be first in a file, if @ is first)
    '#'
        >/< Threshold on X averaged over N using stat S
    '%'
        >/< Difference X over N days using stat S
    '@'
        use the filename - in file can use ':c ' or ':d ' for set
    '$'
        the top(>) or bottom(<) X (e.g. top 10) ranked entries for N/S
    """
    prepended = ['#', '%', '@', '^', '$']
    hl = Namespace(proc=True, highlight=highlight, col=highlight_col)
    if not isinstance(highlight, str):
        return hl
    if highlight[0] not in prepended:
        hl.highlight = highlight.split(',')
        return hl

    proc, tstat = _parse_highlight(highlight, plot_type, set)
    hl.col = 'Key'
    print("---{}---{}---{}---".format(set, geo, plot_type))
    skipping = [0, 0]

    if proc[0][0] == '^':  # Use this as "seed", copy to 'fnd' in case this is all.
        keys_this_loop = proc[0][1:].split(',')
        fnd = {}
        for i, key in enumerate(keys_this_loop):
            this_key = '{:0>14d}{}'.format(i, key)
            fnd[this_key] = (key, 'seed')
        del proc[0], tstat[0]
    else:
        keys_this_loop = data.Key
    for this_pass, this_stat in zip(proc, tstat):
        print("\tProcessing {} for {}".format(this_pass, this_stat))
        fnd = {}
        R = this_pass[0]
        D = 1.0 if this_pass[1] == '>' else -1.0
        X, N = [float(x) for x in this_pass[2:].split(':')]
        Nind = -1 * (int(N) + 1)
        _N = [Nind, -1]
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
            V2chk, _s = stats.get_derived_value(_R, _N, key, data, this_stat, label_col, **kwargs)
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

    hl.highlight = []
    sfk = sorted(list(fnd.keys()), reverse=True)
    for i, this_one in enumerate(sfk):
        hl.highlight.append(fnd[this_one][0])
        print("{:02d}  {}".format(i+1, fnd[this_one][1]))
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
        'row', 'slope', 'logslope', 'accel', 'frac' (use :two for piped highlight)
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
    if not isinstance(label_col, list):
        label_col = label_col.split(',')

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
        hl = process_highlight(set, geo, highlight, highlight_col, label_col,
                               plot_type, b, **kwargs)
        fig = plt.figure(figname, figsize=[6, 8])
        if bg_proc:
            bg_vtot = np.zeros(len(b.data[0]))
            bg_vcnt = 0
            bg_keys = []
            for ibk, key in enumerate(b.Key):
                if bg is None or b.State[ibk] in bg:
                    bg_vtot += b.row(key, colname='Key')
                    bg_vcnt += 1
                    bg_keys.append(key)
            if bg_include and len(bg_keys):
                b.plot(plot_type, bg_keys, colname='Key', figname=figname, color='0.7',
                       label=None, **kwargs)
            if len(bg_keys) and (bg_total or bg_average):
                _xx, _yyt = stats.stat_dat(b.dates, bg_vtot,
                                           dtype=plot_type, **kwargs)
                _xx, _yya = stats.stat_dat(b.dates, bg_vtot / bg_vcnt,
                                           dtype=plot_type, **kwargs)
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
                    try:
                        hl_vtot += b.row(this_hl, colname=hl.col)
                    except TypeError:
                        continue
                    hl_vcnt += 1
                _xx, _yyt = stats.stat_dat(b.dates, hl_vtot,
                                           dtype=plot_type, **kwargs)
                _xx, _yya = stats.stat_dat(b.dates, hl_vtot / hl_vcnt,
                                           dtype=plot_type, **kwargs)
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
        plt.legend(loc='upper left')
        plt.grid()
        plt.title("{}".format(set))
        plt.ylabel(stat.stat_type_unit(plot_type))
        # if log_or_linear == 'log' and this_plot_type != 'logslope':
        #     plt.axis(ymin=1.0)
        plt.yscale(log_or_linear)
        fig.autofmt_xdate()
        figfileName = "{}{}{}.png".format(set, geo, datetime.strftime(datetime.now(), "%Y%m%d"))
        figfileName = "{}{}.png".format(set, geo)
        plt.savefig(figfileName)


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
