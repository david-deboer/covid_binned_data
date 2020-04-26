from binc19 import viewer, binc_util
import numpy as np
import matplotlib.pyplot as plt


def time_plot(set=['Confirmed', 'Deaths'], geo='County', highlight=['6-13', '6-1', '6-37'],
              highlight_col='Key', label_col='County', plot_type='row', states=['CA'],
              include_average=True, include_total=True, include_background=True):
    """
    Plot time sequences.

    Parameters
    ----------
    set : list of str
        'Confirmed' and/or 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban'
    highlight : list of str
        Rows to overplot
    highlight : str
        Name of column for above
    label_col : str
        Name of column to use as labels
    plot_type : str
        'row', 'slope', 'logslope'
    states : list of str
        For State, County, or Congress can limit background/stats to states
    include_average : bool
    include_total : bool
    include_background : bool
    """
    for i, set in enumerate(set):
        filename = "Bin_{}_{}.csv".format(set, geo)
        b = viewer.View(filename)
        total = np.zeros(len(b.data[0]))
        counts = np.zeros(len(b.data[0]))
        for i, key in enumerate(b.Key):
            if states is None or b.State[i] in states:
                total += b.row(key, colname='Key')
                counts += 1
                if include_background:
                    b.plot(plot_type, key, colname='Key', figname=filename, color='0.7', label=None)
        if include_total:
            plt.plot(b.dates, total, color='k', linewidth=4, label='Total', linestyle='--')
        if include_average:
            plt.plot(b.dates, total/counts, color='0.4', linewidth=4, label='Average')
        if highlight is not None:
            for hl in highlight:
                b.plot(plot_type, colname=highlight_col, figname=filename,
                       linewidth=3, label=label_col)
        plt.legend()
        plt.axis(ymin=1.0)
        plt.yscale('log')


def time_table(date=14, geo='County', highlight='6-13', highlight_col='Key', label_col='County'):
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
