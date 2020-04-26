import csv
import numpy as np
import matplotlib.pyplot as plt
from . import stats, binc_util
"""
This is a csv viewer for the covid_binned_data files.
"""


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
                    dataslice = slice(len(self.dtype)+1, len(row))
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

    def row(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        return self.data[col4ind.index(key)]

    def rowind(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        return col4ind.index(key)

    def plot(self, plot_type, key, colname='Key', figname='key', **kwargs):
        fig = plt.figure(figname)
        if not isinstance(key, list):
            key = [key]
        plt_args = binc_util.plot_kwargs(**kwargs)
        for k in key:
            ind = self.rowind(k, colname=colname)
            if plt_args['label'] is not None:
                plt_args['label'] = getattr(self, plt_args['label'])[ind]
            if plot_type == 'logslope':
                x, y = stats.logslope(self.dates, self.data[ind])
            elif plot_type == 'slope':
                x, y = stats.slope(self.dates, self.data[ind])
            else:
                x, y = self.dates, self.data[ind]
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
