import numpy as np
from datetime import datetime
from binc19 import binc_util


def slope(x, y, **kwargs):
    norm = binc_util.proc_kwargs(kwargs, {'norm': 1.0})
    if isinstance(x[0], datetime):
        dx = np.asarray([(x[i+1] - x[i]).days for i in range(len(x)-1)])
        xret = x[1:]
    else:
        dx = np.diff(np.asarray(x))
        xret = np.asarray([x[i] + dx[i] for i in range(len(x) - 1)])
    dy = np.diff(np.asarray(y)) / norm
    m = dy / dx
    return xret, m


def logslope(x, y, **kwargs):
    low_clip = binc_util.proc_kwargs(kwargs, {'low_clip': 1E-4})
    if low_clip:
        z = np.where(y <= 0.0)
        y[z] = low_clip
    return slope(x, np.log(y), **kwargs)


def smooth_days(x, y, **kwargs):
    stats_dict = {'smooth': 7, 'kernel': 'Trap', 'smooth_fix': 'redo'}
    kernel, smooth, smooth_fix = binc_util.proc_kwargs(kwargs, stats_dict)
    if not smooth:
        return x, y
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
    redo = int(np.floor(smooth / 2))
    xsm = x
    if smooth_fix == 'cull':
        _sfs = slice(0, len(ysm) - redo)
        xsm = x[_sfs]
        ysm = ysm[_sfs]
    elif smooth_fix == 'redo':
        for i in range(len(y) - redo, len(y)):
            ave = 0.0
            cnt = 0
            for j in range(i, len(y)):
                ave += y[j]
                cnt += 1
            ysm[i] = (ave / cnt + ysm[i]) / 2.0
    return xsm, ysm


def stat_dat(x, y, dtype, **kwargs):
    extra_smooth = binc_util.proc_kwargs(kwargs, {'extra_smooth': False})
    if extra_smooth:
        kwargs['smooth_fix'] = 'none'
    xsm, ysm = smooth_days(x, y, **kwargs)
    # tmpfile = '{}{}.dat'.format(dtype, str(y[-1] + y[-2]).replace('.', ''))
    # with open(tmpfile, 'w') as fp:
    #     for i in range(len(y)):
    #         print('{},{}'.format(y[i], ysm[i]), file=fp)
    if dtype == 'logslope':
        xc, yc = logslope(xsm, ysm, **kwargs)
    elif dtype in ['slope', 'frac', 'accel']:
        xc, yc = slope(xsm, ysm, **kwargs)
        if dtype == 'accel':
            xc, yc = slope(xsm, ysm, **kwargs)
        elif dtype == 'frac':
            for i in range(len(yc)):
                if ysm[i] < 0.1:
                    yc[i] = 0.0
                else:
                    yc[i] = 100.0 * yc[i] / ysm[i]
    else:
        xc = xsm
        yc = ysm
    if extra_smooth:
        kwargs['smooth_fix'] = 'cull'
        xc, yc, = smooth_days(xc, yc, **kwargs)

    return xc, yc
