import numpy as np
from datetime import datetime
from binc19 import binc_util


class Stat:
    """
    Class to compute stuff on the covid time-series data.
    """
    allowed = ['row', 'slope', 'logslope', 'accel', 'frac']
    params = ['extra_smooth', 'kernel', 'smooth', 'smooth_fix', 'norm', 'low_clip']

    def __init__(self, stat_type=None, **kwargs):
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
        self.extra_smooth = binc_util.proc_kwargs(kwargs, {'extra_smooth': False})
        stats_dict = {'smooth': 7, 'kernel': 'Trap', 'smooth_fix': 'redo'}
        self.kernel, self.smooth, self.smooth_fix = binc_util.proc_kwargs(kwargs, stats_dict)
        self.norm = binc_util.proc_kwargs(kwargs, {'norm': 1.0})
        self.low_clip = binc_util.proc_kwargs(kwargs, {'low_clip': 1E-4})

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
        dy = np.diff(np.asarray(y)) / self.norm
        m = dy / dx
        return xret, m

    def _logslope(self, x, y):
        if self.low_clip:
            z = np.where(y <= 0.0)
            y[z] = self.low_clip
        return self._slope(x, np.log(y))

    def _smooth_days(self, x, y):
        if not self.smooth:
            return x, y
        if self.kernel.upper().startswith('B'):
            from astropy.convolution import convolve, Box1DKernel
            ysm = convolve(y, Box1DKernel(self.smooth), boundary='extend')
        elif self.kernel.upper().startswith('G'):
            from astropy.convolution import convolve, Gaussian1DKernel
            ysm = convolve(y, Gaussian1DKernel(self.smooth), boundary='extend')
        elif self.kernel.upper().startswith('T'):
            from astropy.convolution import convolve, Trapezoid1DKernel
            ysm = convolve(y, Trapezoid1DKernel(self.smooth), boundary='extend')
        else:
            raise ValueError('{} not supported.'.format(self.kernel))
        redo = int(np.floor(self.smooth / 2))
        xsm = x
        if self.smooth_fix == 'cull':
            _sfs = slice(0, len(ysm) - redo)
            xsm = x[_sfs]
            ysm = ysm[_sfs]
        elif self.smooth_fix == 'redo':
            for i in range(len(y) - redo, len(y)):
                ave = 0.0
                cnt = 0
                for j in range(i, len(y)):
                    ave += y[j]
                    cnt += 1
                ysm[i] = (ave / cnt + ysm[i]) / 2.0
        return xsm, ysm

    def calc(self, x, y):
        if self.extra_smooth:
            self.extra_smooth = self.smooth_fix
            self.smooth_fix = 'none'
        xsm, ysm = self._smooth_days(x, y)
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
            xc = xsm
            yc = ysm
        if self.extra_smooth:
            self.smooth_fix = self.extra_smooth
            xc, yc, = self._smooth_days(xc, yc)
        self.x = xc
        self.y = yc
        return xc, yc


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
