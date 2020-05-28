import csv
import numpy as np
import matplotlib.pyplot as plt
from . import stats, binc_util
"""
This is a csv viewer for the covid_binned_data files.
"""


color_list = ['b', 'g', 'r', 'c', 'm', 'k', 'tab:blue', 'tab:orange', 'tab:brown', 'tab:olive',
              'tab:pink', 'bisque', 'lightcoral', 'goldenrod', 'lightgrey', 'lime', 'lightseagreen']


class View:
    """Class for reading csv files."""
    def __init__(self, filename=None):
        self.filename = filename
        self.header = []
        self.dates = []
        self.data = []
        self.plot_log = False
        if filename is not None:
            self.load()

    def load(self, filename=None):
        """
        Load csv files.

        Parameters
        ----------
        filename : str or None
            filename of csv
        """
        if filename is None:
            filename = self.filename
        if not filename.endswith('.csv'):
            filename = '{}.csv'.format(filename)
        if not filename.startswith('Bin_'):
            filename = 'Bin_{}'.format(filename)
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            for i, row in enumerate(reader):
                if not i:
                    self.header = row
                    self.dtype = [x for x in row[:row.index('Latitude')+1]]
                    for i, _d in enumerate(self.dtype):
                        setattr(self, _d, [])
                    dataslice = slice(len(self.dtype), len(row))
                    self.dates = [binc_util.string_to_date(x) for x in row[dataslice]]
                else:
                    this_row = [float(x) for x in row[dataslice]]
                    if len(this_row) != len(self.dates):
                        continue
                    self.data.append(this_row)
                    for i, _d in enumerate(self.dtype):
                        getattr(self, _d).append(row[i])
        self.data = np.asarray(self.data)
        self.Longitude = [float(x) for x in self.Longitude]
        self.Latitude = [float(x) for x in self.Latitude]
        self.Ndata = len(self.data)

    def scatter_loc(self, axis=[-160, -60, 18, 65]):
        """Scatter plot of longitude/latitude of cases."""
        plt.figure('USA')
        plt.plot(self.Longitude, self.Latitude, '.')
        if axis is not None:
            plt.axis(axis)
        plt.title(self.filename)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    def meta(self, val, key, colname):
        ind = self.rowind(key, colname)
        return getattr(self, val)[ind]

    def row(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        return self.data[col4ind.index(key)]

    def rowind(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        return col4ind.index(key)

    def plot(self, plot_type, key, colname='Key', figname='key', **kwargs):
        fig = plt.figure(figname)
        if not isinstance(key, list):
            key = key.split(',')
        if 'label' in kwargs.keys():
            label_column = kwargs['label'].split(',')
            for lc in label_column:
                try:
                    x = getattr(self, lc)[0]
                except TypeError:
                    raise TypeError("viewer.plot: "
                                    " label must be a column header name [{}]".format(lc))
        plt_args = binc_util.plot_kwargs(kwargs)
        for ik, k in enumerate(key):
            ind = self.rowind(k, colname=colname)
            if isinstance(label_column, list):
                lbl = []
                for lc in label_column:
                    lbl.append(getattr(self, lc)[ind])
                plt_args['label'] = ','.join(lbl)
            x, y = stats.stat_dat(self.dates, self.data[ind], plot_type, **kwargs)
            cik = ik % len(color_list)
            plt_args['color'] = color_list[cik]
            plt.plot(x, y, **plt_args)
        fig.autofmt_xdate()
        plt.title(colname)

    def plot_col(self, date):
        """
        Column plot of date data.

        Parameter
        ---------
        date : str or list of str
            Dates to plot in e.g. 3/22/20 format
        """
        plt.figure('Date')
        for _d in date:
            dati = binc_util.string_to_date(_d)
            ind = self.dates.index(dati)
            plt.semilogy(self.data[:, ind], '.', label=_d)
        plt.title('Date')
