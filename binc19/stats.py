import numpy as np
from datetime import datetime
from ddb_util import state_variable
from . import binc_util


class Stat:
    """
    Class to compute stuff on the covid time-series data.
    """
    allowed = ['row', 'slope', 'logslope', 'accel', 'frac']

    def __init__(self, stat_type=None, **kwargs):
        params = {'smooth_schedule': ['Custom', 'Custom'],
                  'smooth': [3, 3],
                  'smooth_fix': ['none', 'cull'],
                  'norm': 1.0,
                  'low_clip': 1.0E-4}
        self.par = state_variable.StateVar(label="Stat variables", verbose=False)
        self.par.sv_load(params, use_to_init=True, var_type=None)
        self.set_stat(stat_type, **kwargs)

    def set_stat(self, stat_type, **kwargs):
        if stat_type is not None and stat_type not in self.allowed:
            raise ValueError("{} not allowed - set to None".format(stat_type))
        self.type = stat_type
        self._what_unit_and_kwargs(**kwargs)

    def show_params(self):
        print("Stat:  {}  {}".format(self.type, self.unit))
        for p in self.params:
            print("\t{}:  {}".format(p, getattr(self, p)))

    def _what_unit_and_kwargs(self, **kwargs):
        self.par.state(**kwargs)
        self.par.smooth_schedule = binc_util.fix_lists(self.par.smooth_schedule, 2, str)
        self.par.smooth = binc_util.fix_lists(self.par.smooth, 2, float)
        self.par.smooth_fix = binc_util.fix_lists(self.par.smooth_fix, 2, str)

        if self.type is None:
            self.unit = None
        elif self.type == 'row':
            self.unit = 'count'
        elif self.type == 'slope':
            self.unit = 'count/day'
        elif self.type == 'logslope':
            self.unit = '1/day'
        elif self.type == 'accel':
            self.unit = 'count/day/day'
        elif self.type == 'frac':
            self.unit = '%'

    def _slope(self, x, y):
        if isinstance(x[0], datetime):
            dx = np.asarray([(x[i+1] - x[i]).days for i in range(len(x)-1)])
            xret = x[1:]
        else:
            dx = np.diff(np.asarray(x))
            xret = np.asarray([x[i] + dx[i] for i in range(len(x) - 1)])
        dy = np.diff(np.asarray(y)) / self.par.norm
        m = dy / dx
        return xret, m

    def _logslope(self, x, y):
        if self.par.low_clip:
            z = np.where(y <= 0.0)
            y[z] = self.par.low_clip
        return self._slope(x, np.log(y))

    def calc(self, x, y):
        # Stage 1
        xsm, ysm = smooth_days(x, y,
                               kernel=self.par.smooth_schedule[0],
                               ksize=self.par.smooth[0],
                               fix=self.par.smooth_fix[0])
        # Calculate data values
        if self.type == 'logslope':
            xc, yc = self._logslope(xsm, ysm)
        elif self.type in ['slope', 'frac', 'accel']:
            xc, yc = self._slope(xsm, ysm)
            if self.type == 'accel':
                xc, yc = self._slope(xsm, ysm)
            elif self.type == 'frac':
                for i in range(len(yc)):
                    if ysm[i] < 0.1:
                        yc[i] = 0.0
                    else:
                        yc[i] = 100.0 * yc[i] / ysm[i]
        else:
            xc, yc = xsm, ysm
        # Stage 2
        xc, yc = smooth_days(xc, yc,
                             kernel=self.par.smooth_schedule[1],
                             ksize=self.par.smooth[1],
                             fix=self.par.smooth_fix[1])
        self.x, self.y = xc, yc
        return xc, yc


def smooth_days(x, y, kernel, ksize, fix):
    """Smooth data (x, y) given parameters kernel, ksize, fix"""
    kernel = kernel.lower()
    if kernel == 'none' or not ksize:
        return x, y
    if kernel == 'box':
        from astropy.convolution import convolve, Box1DKernel
        ysm = convolve(y, Box1DKernel(ksize), boundary='extend')
    elif kernel == 'gaussian':
        from astropy.convolution import convolve, Gaussian1DKernel
        ysm = convolve(y, Gaussian1DKernel(ksize), boundary='extend')
    elif kernel == 'trapezoid':
        from astropy.convolution import convolve, Trapezoid1DKernel
        ysm = convolve(y, Trapezoid1DKernel(ksize), boundary='extend')
    elif kernel == 'triangle':
        from astropy.convolution import convolve, CustomKernel
        f = triangle(ksize)
        ysm = convolve(y, CustomKernel(f), boundary='extend')
    else:
        raise ValueError('{} not supported.'.format(kernel))
    redo = int(np.floor(ksize / 2))
    xsm = x
    if fix == 'cull':
        _sfs = slice(0, len(ysm) - redo)
        xsm = x[_sfs]
        ysm = ysm[_sfs]
    elif fix == 'redo':
        for i in range(len(y) - redo, len(y)):
            ave = 0.0
            cnt = 0
            for j in range(i, len(y)):
                ave += y[j]
                cnt += 1
            ysm[i] = (ave / cnt + ysm[i]) / 2.0
    return xsm, ysm


def triangle(b):
    b = 2.0 * np.floor(b / 2.0) + 1.0
    b2 = (b - 1.0) / 2.0
    f = []
    for i in range(int(b)):
        if i <= b2:
            f.append(i * (1.0 / b2)**2)
        else:
            f.append(2.0 / b2 - i * (1.0 / b2)**2)
    return f


def get_derived_value(R, N, x, y):
    if R == 'average':
        get_an_ave = 0.0
        for i in range(N[0], N[1]):
            get_an_ave += y[i]
        get_an_ave /= (N[1] - N[0])
        return get_an_ave
    elif R == 'difference':
        dx = (x[N[1]] - x[N[0]]).days  # noqa
        dn = (y[N[1]] - y[N[0]])
        return dn
