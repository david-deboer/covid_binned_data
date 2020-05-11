from binc19 import viewer, binc_util, stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime


same_plot_name = 'binc19'


def time_plot(sets=['Confirmed', 'Deaths'], geo='County',
              highlight=['CA-13', 'CA-1', 'CA-37', 'CA-73', 'OH-35', 'OH-55'],
              highlight_col='Key', label_col='Name', plot_type='row', bg=['CA'],
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
        Rows to overplot.    If starts with '>' or '<' it will threshold
        on the following number.
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
    """
    bg_dict = {'bg_average': False, 'bg_include': False, 'bg_total': False}
    bg_average, bg_include, bg_total = binc_util.proc_kwargs(kwargs, bg_dict)
    hl_dict = {'hl_average': False, 'hl_total': False, 'hl_include': True}
    hl_average, hl_include, hl_total = binc_util.proc_kwargs(kwargs, hl_dict)
    other_dict = {'same_plot': False, 'save_stats': False}
    same_plot, save_stats = binc_util.proc_kwargs(kwargs, other_dict)

    bg_proc = bg_average or bg_total or bg_include
    hl_proc = highlight is not None

    if not hl_proc and not bg_proc:
        print("Neither highlight nor background chosen.")
        return

    hl_tdir = None
    if hl_proc and isinstance(highlight, str):
        if highlight[0] in ['<', '>']:
            hl_tdir = 1.0 if highlight[0] == '<' else -1.0
            thold = float(highlight[1:])
            highlight_col = 'Key'
        else:
            highlight = highlight.split(',')

    figname = None
    if same_plot:
        figname = same_plot_name
    for i, set in enumerate(sets):
        data_out = {'dates': [], 'bg_tot': [], 'bg_ave': [], 'hl_tot': [], 'hl_ave': []}
        filename = "Bin_{}_{}.csv".format(set, geo)
        if figname != same_plot_name:
            figname = filename
        b = viewer.View(filename)
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
        if hl_proc:
            hl_vtot = np.zeros(len(b.data[0]))
            hl_vcnt = 0
            if hl_tdir is not None:
                highlight = []
                for i, key in enumerate(b.Key):
                    if hl_tdir * b.row(key)[-1] <= hl_tdir * thold:
                        highlight.append(key)
            if hl_include and len(highlight):
                b.plot(plot_type, highlight, colname=highlight_col, figname=figname, linewidth=3,
                       label=label_col, **kwargs)
            if len(highlight) and (hl_total or hl_average):
                for hl in highlight:
                    hl_vtot += b.row(hl, colname=highlight_col)
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
        plt.title("{}: {}".format(set, plot_type))
        if plot_type == 'row':
            plt.ylabel('Count')
        elif plot_type == 'slope':
            plt.ylabel('count/day')
        elif plot_type == 'logslope':
            plt.ylabel('1/day')
        if plot_type != 'logslope':
            plt.axis(ymin=1.0)
        plt.yscale('log')
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
