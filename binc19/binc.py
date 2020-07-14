import csv
import os.path
import numpy as np
import matplotlib.pyplot as plt
from . import stats, binc_util
"""
This is a csv viewer for the covid_binned_data files.
"""


color_list = ['b', 'g', 'r', 'c', 'm', 'k', 'tab:blue', 'tab:orange', 'tab:brown', 'tab:olive',
              'tab:pink', 'bisque', 'lightcoral', 'goldenrod', 'lightgrey', 'lime', 'lightseagreen']


class Binc:
    """Class for reading csv files."""
    def __init__(self, filename=None):
        self.data_path = os.path.dirname(__file__)
        self.filename = filename
        self.header = []
        self.dates = []
        self.data = []
        self.plot_log = False
        if filename is not None:
            self.load()

    def load(self, filename=None,
             dir='/Users/ddeboer/Documents/ubase/Projects/COVID_analysis/covid_binned_data'):
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
        if dir is not None:
            filename = os.path.join(dir, filename)
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

    def meta(self, val, key, colname):
        ind = self.rowind(key, colname)
        return getattr(self, val)[ind]

    def row(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        try:
            col = self.data[col4ind.index(key)]
        except ValueError:
            col = None
        return col

    def rowind(self, key, colname='Key'):
        col4ind = getattr(self, colname)
        try:
            col = col4ind.index(key)
        except ValueError:
            col = None
        return col

    def plot(self, plot_type, key, colname='Key', figname='key', **kwargs):
        fig = plt.figure(figname)
        if not isinstance(key, list):
            key = key.split(',')
        if 'label' in kwargs.keys():
            label_column = kwargs['label']
            if not isinstance(label_column, list):
                label_column = label_column.split(',')
            for lc in label_column:
                try:
                    x = getattr(self, lc)[0]
                except TypeError:
                    raise TypeError("viewer.plot: "
                                    "label must be a column header name [{}]".format(lc))
        plt_args = binc_util.plot_kwargs(kwargs)
        for ik, k in enumerate(key):
            ind = self.rowind(k, colname=colname)
            if ind is None:
                continue
            if isinstance(label_column, list):
                lbl = []
                for lc in label_column:
                    if lc is not None:
                        lbl.append(getattr(self, lc)[ind])
                plt_args['label'] = ','.join(lbl)
            x, y = stats.stat_dat(self.dates, self.data[ind], plot_type, **kwargs)
            cik = ik % len(color_list)
            plt_args['color'] = color_list[cik]
            plt.plot(x, y, **plt_args)
        fig.autofmt_xdate()
        plt.title(colname)
