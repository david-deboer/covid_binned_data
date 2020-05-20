import numpy as np
from datetime import datetime, timedelta
from binc19 import binc_util


def slope(x, y, **kwargs):
    norm = binc_util.proc_kwargs(kwargs, {'norm': 1.0})
    if isinstance(x[0], datetime):
        dx = np.asarray([(x[i+1] - x[i]).days for i in range(len(x)-1)])
        xret = [x[i] + timedelta(days=dx[i] / 2.0) for i in range(len(x) - 1)]
    else:
        dx = np.diff(np.asarray(x))
        xret = np.asarray([x[i] + dx[i] / 2.0 for i in range(len(x) - 1)])
    dy = np.diff(np.asarray(y)) / norm
    m = smooth_days(dy / dx, **kwargs)
    return xret, m


def logslope(x, y, **kwargs):
    low_clip = binc_util.proc_kwargs(kwargs, {'low_clip': 1E-4})
    if low_clip:
        z = np.where(y <= 0.0)
        y[z] = kwargs['low_clip']
    return slope(x, np.log(y), **kwargs)


def smooth_days(y, **kwargs):
    stats_dict = {'smooth': 7, 'kernel': 'Trap', 'apply_redo': True}
    apply_redo, kernel, smooth = binc_util.proc_kwargs(kwargs, stats_dict)
    if not smooth:
        return y
    if kernel.upper().startswith('B'):
        from astropy.convolution import convolve, Box1DKernel
        ysm = convolve(y, Box1DKernel(smooth), boundary='extend')
    elif kernel.upper().startswith('G'):
        from astropy.convolution import convolve, Gaussian1DKernel
        ysm = convolve(y, Gaussian1DKernel(smooth), boundary='extend')
    elif kernel.upper().startswith('T'):
        from astropy.convolution import convolve, Trapezoid1DKernel
        ysm = convolve(y, Trapezoid1DKernel(smooth), boundary='extend')
    else:
        raise ValueError('{} not supported.'.format(kernel))
    if apply_redo:
        redo = int(np.floor(smooth / 2))
        for i in range(len(y) - redo, len(y)):
            ave = 0.0
            cnt = 0
            for j in range(i, len(y)):
                ave += y[j]
                cnt += 1
            ysm[i] = (ave / cnt + ysm[i]) / 2.0
    return ysm


def stat_dat(x, y, dtype, **kwargs):
    if dtype == 'logslope':
        x, y = logslope(x, y, **kwargs)
    elif dtype == 'slope' or dtype == 'accel':
        x, y = slope(x, y, **kwargs)
        if dtype == 'accel':
            x, y = slope(x, y, **kwargs)
    else:
        y = smooth_days(y, **kwargs)
    return x, y
