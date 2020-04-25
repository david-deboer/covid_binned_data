from binc19 import viewer
import numpy as np
import matplotlib.pyplot as plt


def time(set=['Confirmed', 'Deaths'], geo='County', highlight=['6-13', '6-1', '6-37'],
         highlight_col='Key', label_col='County', plot_type='row', states='CA',
         include_average=True, include_total=True, include_background=True):

    for i, set in enumerate(set):
        filename = "Bin_{}_{}.csv".format(set, geo)
        b = viewer.View(filename)
        plot_func = getattr(b, 'plot_{}'.format(plot_type))
        total = np.zeros(len(b.data[0]))
        counts = np.zeros(len(b.data[0]))
        for i, key in enumerate(b.Key):
            if states is None or b.State[i] in states:
                total += b.row(key, colname='Key')
                counts += 1
                if include_background:
                    plot_func(key, colname='Key', figname=filename, color='0.7', label=None)
        if include_total:
            plt.plot(b.dates, total, color='k', linewidth=4, label='Total', linestyle='--')
        if include_average:
            plt.plot(b.dates, total/counts, color='0.4', linewidth=4, label='Average')
        if highlight is not None:
            for hl in highlight:
                plot_func(hl, colname=highlight_col, figname=filename, linewidth=3, label=label_col)
        plt.legend()
        plt.axis(ymin=1.0)
        plt.yscale('log')
