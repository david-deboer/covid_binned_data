#! /usr/bin/env python
import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
"""
This is a simple csv reader for the covid_binned_data files.
"""


class BGBC:
    """Class for reading csv files."""
    def __init__(self, filename=None):
        self.filename = filename
        self.header = []
        self.dates = []
        self.data = []
        self.date_fmt = '%m/%d/%y'
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
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            for i, row in enumerate(reader):
                if not i:
                    self.header = row
                    self.dtype = [x for x in row[:row.index('Latitude')+1]]
                    for i, _d in enumerate(self.dtype):
                        setattr(self, _d, [])
                    dataslice = slice(len(self.dtype)+1, len(row))
                    self.dates = [datetime.strptime(x, self.date_fmt) for x in row[dataslice]]
                else:
                    self.data.append([float(x) for x in row[dataslice]])
                    for i, _d in enumerate(self.dtype):
                        getattr(self, _d).append(row[i])
        self.data = np.array(self.data)
        self.Longitude = [float(x) for x in self.Longitude]
        self.Latitude = [float(x) for x in self.Latitude]

    def plot_scatter(self):
        """Scatter plot of longitude/latitude of cases."""
        plt.figure('USA')
        plt.plot(self.Longitude, self.Latitude, '.')
        plt.axis([-160, -60, 18, 65])
        plt.title(self.filename)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    def plot_row(self, fip):
        """
        Row plot of fip data.

        Parameter
        ---------
        fip : str of list of str
            fip codes of row
        """
        if not isinstance(fip, list):
            fip = [fip]
        fig = plt.figure(self.header[2])
        for _f in fip:
            ind = self.Key.index(_f)
            lbl = getattr(self, self.header[2])[ind]
            plt.plot(self.dates, self.data[ind, :], label=lbl)
        fig.autofmt_xdate()
        plt.title(self.header[2])

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
            dati = datetime.strptime(_d, self.date_fmt)
            ind = self.dates.index(dati)
            plt.semilogy(self.data[:, ind], '.', label=_d)
        plt.title('Date')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('filename', nargs='?', help="Name of csv file (include .csv)",
                    default="Bin_Confirmed_County.csv")
    ap.add_argument('-f', '--fip', help="Row plot for FIP (csv-list)", default='6-1,6-13')
    ap.add_argument('-d', '--date', help="Col plot for date (csv-list)", default='4/7/20,3/15/20')
    args = ap.parse_args()
    args.fip = args.fip.split(',')
    args.date = args.date.split(',')
    q = BGBC(args.filename)
    q.plot_scatter()
    q.plot_row(args.fip)
    plt.legend()
    # q.plot_col(args.date)
    # plt.legend()
    plt.show()
