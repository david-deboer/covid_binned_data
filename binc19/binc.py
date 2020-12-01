import csv
import os.path
import numpy as np
import matplotlib.pyplot as plt
from . import stats, binc_util
from my_utils import state_variable
"""
This handles covid_binned_data files.
"""


color_list = ['b', 'g', 'r', 'c', 'm', 'k', 'tab:blue', 'tab:orange', 'tab:brown', 'tab:olive',
              'tab:pink', 'bisque', 'lightcoral', 'goldenrod', 'lightgrey', 'lime', 'lightseagreen']


class Binc(state_variable.StateVar):
    """Class for reading csv files."""
    def __init__(self, filename=None):
        plt_args = {'alpha': None,
                    'color': None,
                    'linestyle': None,
                    'linewidth': None,
                    'marker': None,
                    'markersize': None,
                    'label': None
                    }
        super().__init__(label='BINC state variables', verbose=False, enforce='loose')
        self.pltpar = state_variable.StateVar(label='Plot kwargs', verbose=False, enforce='nominal')
        self.pltpar.sv_load(plt_args, use_to_init=True, var_type=None)
        self.filename = filename
        self.header = []
        self.dates = []
        self.data = []
        self.stats = stats.Stat(stat_type=None)
        self.st_date = {}
        self.st_data = {}
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
        self.filename = filename
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            for i, row in enumerate(reader):
                if not i:
                    self.header = row
                    self.dtype = [x for x in row[:row.index('Latitude')+1]]
                    for i, _d in enumerate(self.dtype):
                        setattr(self, _d, [])
                    self.ID = []  # This is set to the first col, which should be a unique ID
                    dataslice = slice(len(self.dtype), len(row))
                    self.dates = [binc_util.string_to_date(x) for x in row[dataslice]]
                else:
                    this_row = [float(x) for x in row[dataslice]]
                    if len(this_row) != len(self.dates):
                        continue
                    self.data.append(this_row)
                    for i, _d in enumerate(self.dtype):
                        getattr(self, _d).append(row[i])
                    self.ID.append(row[0])
        self.data = np.asarray(self.data)
        self.Longitude = [float(x) for x in self.Longitude]
        self.Latitude = [float(x) for x in self.Latitude]
        self.Ndata = len(self.data)

    def meta(self, val, key, colname):
        ind = self.rowind(key, colname)
        return getattr(self, val)[ind]

    def row(self, key, colname='ID'):
        col4ind = getattr(self, colname)
        try:
            col = self.data[col4ind.index(key)]
        except ValueError:
            col = None
        return col

    def rowind(self, key, colname='ID'):
        col4ind = getattr(self, colname)
        try:
            col = col4ind.index(key)
        except ValueError:
            col = None
        return col

    def calc(self, stat_type, **kwargs):
        self.stats.set_stat(stat_type, **kwargs)
        self.st_data[stat_type] = {}
        for i in range(self.Ndata):
            key = self.ID[i]
            self.st_date[stat_type], self.st_data[stat_type][key] = self.stats.calc(self.dates,
                                                                                    self.data[i])

    def plot(self, stat_type, key, colname='ID', figname='ID', **kwargs):
        self.pltpar.state(**kwargs)
        self.state(**kwargs)
        self.stats.set_stat(stat_type, **kwargs)
        fig = plt.figure(figname)
        if not isinstance(key, list):
            key = key.split(',')
        if self.label is not None:
            if not isinstance(self.label, list):
                self.label = self.label.split(',')
            for lc in self.label:
                try:
                    x = getattr(self, lc)[0]
                except TypeError:
                    raise TypeError("binc.plot: "
                                    "label must be a column header name [{}]".format(lc))
        for ik, k in enumerate(key):
            ind = self.rowind(k, colname=colname)
            if ind is None:
                continue
            x, y = self.stats.calc(self.dates, self.data[ind])
            if isinstance(self.label, list):
                lbl = []
                for lc in self.label:
                    if lc is not None:
                        lbl.append(getattr(self, lc)[ind])
                self.pltpar.label = ','.join(lbl)
            cik = ik % len(color_list)
            self.pltpar.color = color_list[cik]
            plt.plot(x, y, **self.pltpar.sv_todict())
        fig.autofmt_xdate()
        plt.title(colname)
