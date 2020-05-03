from binc19 import viewer, binc_util, stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta


same_plot_name = 'binc19'


def time_plot(sets=['Confirmed', 'Deaths'], geo='County', highlight=['CA-13', 'CA-1', 'CA-37'],
              highlight_col='Key', label_col='Key', plot_type='row', states=['CA'], **kwargs):
    """
    Plot time sequences.

    Parameters
    ----------
    sets : list of str
        'Confirmed' and/or 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'
    highlight : list of str
        Rows to overplot
    highlight : str
        Name of column for above.  If starts with '>' or '<' it will threshold
        on the following number.
    label_col : str
        Name of column to use as labels
    plot_type : str
        'row', 'slope', 'logslope'
    states : list of str
        For State, County, or Congress can limit background/stats to states.
        If None, background is all.
    kwargs:
        include_average : bool
        include_total : bool
        include_background : bool
        smooth : None or int
        low_clip : None or float
        same_plot : bool
    """
    allowed_dict = {'include_average': True, 'include_total': True, 'include_background': True}
    include_average, include_total, include_background = binc_util.proc_kwargs(kwargs, allowed_dict)
    smooth, low_clip, same_plot = binc_util.proc_kwargs(kwargs, {'smooth': 5, 'low_clip': 1E-4,
                                                        'same_plot': False})
    dir = None
    if isinstance(highlight, str):
        if highlight[0] in ['<', '>']:
            dir = 1.0 if highlight[0] == '<' else -1.0
            thold = float(highlight[1:])
            highlight_col = 'Key'
        else:
            highlight = highlight.split(',')
    figname = None
    if same_plot:
        figname = same_plot_name
    for i, set in enumerate(sets):
        if dir is not None:
            highlight = []
        filename = "Bin_{}_{}.csv".format(set, geo)
        if figname != same_plot_name:
            figname = filename
        b = viewer.View(filename)
        total = np.zeros(len(b.data[0]))
        counts = np.zeros(len(b.data[0]))
        for i, key in enumerate(b.Key):
            if dir is not None:
                if dir * b.row(key)[-1] <= dir * thold:
                    highlight.append(key)
            if states is None or b.State[i] in states:
                total += b.row(key, colname='Key')
                counts += 1
                if include_background:
                    b.plot(plot_type, key, colname='Key', smooth=smooth, low_clip=low_clip,
                           figname=figname, color='0.7', label=None)
        _xx, total = stats.stat_dat(b.dates, total, dtype=plot_type, **kwargs)
        if include_total:
            plt.figure(figname)
            plt.plot(_xx, total, color='k', linewidth=4, label='Total', linestyle='--')
        if include_average:
            plt.plot(_xx, total/counts, color='0.4', linewidth=4, label='Average')
        if highlight is not None:
            for hl in highlight:
                b.plot(plot_type, hl, colname=highlight_col, smooth=smooth, low_clip=low_clip,
                       figname=figname, linewidth=3, label=label_col)
        plt.legend()
        plt.title(set)
        if plot_type != 'logslope':
            plt.axis(ymin=1.0)
        plt.yscale('log')


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
