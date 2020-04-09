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
    def __init__(self, filename=None):
        self.filename = filename
        self.header = []
        self.dates = []
        self.data = []
        self.date_fmt = '%m/%d/%y'
        if filename is not None:
            self.load()

    def load(self, filename=None):
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
        plt.figure('USA')
        plt.plot(self.Longitude, self.Latitude, '.')
        plt.axis([-160, -60, 18, 65])
        plt.title(self.filename)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    def plot_row(self, fip):
        ind = self.FIP.index(fip)
        fig = plt.figure(self.header[2])
        lbl = getattr(self, self.header[2])[ind]
        fig.autofmt_xdate()
        plt.plot(self.dates, self.data[ind, :], label=lbl)
        plt.title(self.header[2])

    def plot_col(self, date):
        dati = datetime.strptime(date, self.date_fmt)
        ind = self.dates.index(dati)
        plt.figure('Date')
        plt.semilogy(self.data[:, ind], '.', label=date)
        plt.title('Date')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('filename', nargs='?', help="Name of csv file (include .csv)",
                    default="Bin_Confirmed_County.csv")
    ap.add_argument('-f', '--fip', help="Row plot for FIP (csv-list)", default='06-001,06-013')
    ap.add_argument('-d', '--date', help="Col plot for date (csv-list)", default='4/7/20,3/15/20')
    args = ap.parse_args()
    args.fip = args.fip.split(',')
    args.date = args.date.split(',')
    q = BGBC(args.filename)
    q.plot_scatter()
    for fip in args.fip:
        q.plot_row(fip)
    plt.legend()
    for d in args.date:
        q.plot_col(d)
    plt.legend()
    plt.show()
