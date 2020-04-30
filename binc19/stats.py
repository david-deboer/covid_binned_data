import numpy as np
from datetime import datetime, timedelta
from binc19 import binc_util


def slope(x, y, smooth=5):
    if smooth:
        y = smooth_days(y, boxcar=smooth)
    if isinstance(x[0], datetime):
        dx = np.asarray([(x[i+1] - x[i]).days for i in range(len(x)-1)])
        xret = [x[i] + timedelta(days=dx[i] / 2.0) for i in range(len(x) - 1)]
    else:
        dx = np.diff(np.asarray(x))
        xret = np.asarray([x[i] + dx[i] / 2.0 for i in range(len(x) - 1)])
    dy = np.diff(np.asarray(y))
    return xret, dy / dx


def logslope(x, y, smooth=5, low_clip=1e-4):
    z = np.where(y <= 0.0)
    y[z] = low_clip
    return slope(x, np.log(y), smooth=smooth)


def smooth_days(y, boxcar=5):
    from astropy.convolution import convolve, Box1DKernel
    ysm = convolve(y, Box1DKernel(boxcar))
    redo = int(np.floor(boxcar / 2))
    for i in range(redo):
        ysm[-(i+1)] = y[-(i+1)]
    return ysm


def stat_dat(x, y, dtype, **kwargs):
    smooth, low_clip = binc_util.proc_kwargs(kwargs, {'smooth': False, 'low_clip': False})
    if dtype == 'logslope':
        x, y = logslope(x, y, smooth=smooth, low_clip=low_clip)
    elif dtype == 'slope':
        x, y = slope(x, y, smooth=smooth)
    elif 'smooth' in kwargs.keys():
        y = smooth_days(y, boxcar=kwargs['smooth'])
    return x, y
