import numpy as np
from datetime import datetime
from ddb_util import state_variable


class Stat:
    """
    Class to compute stuff on the covid time-series data.
    """
    allowed = ['row', 'slope', 'logslope', 'accel', 'frac']

    def __init__(self, stat_type=None, **kwargs):
        params = {'extra_smooth': False,
                  'kernel': 'Trap',
                  'smooth': 3,
                  'smooth_fix': 'none',
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

    def _smooth_days(self, x, y):
        if not self.par.smooth:
            return x, y
        if self.par.kernel.upper().startswith('B'):
            from astropy.convolution import convolve, Box1DKernel
            ysm = convolve(y, Box1DKernel(self.par.smooth), boundary='extend')
        elif self.par.kernel.upper().startswith('G'):
            from astropy.convolution import convolve, Gaussian1DKernel
            ysm = convolve(y, Gaussian1DKernel(self.par.smooth), boundary='extend')
        elif self.par.kernel.upper().startswith('T'):
            from astropy.convolution import convolve, Trapezoid1DKernel
            ysm = convolve(y, Trapezoid1DKernel(self.par.smooth), boundary='extend')
        else:
            raise ValueError('{} not supported.'.format(self.par.kernel))
        redo = int(np.floor(self.par.smooth / 2))
        xsm = x
        if self.par.smooth_fix == 'cull':
            _sfs = slice(0, len(ysm) - redo)
            xsm = x[_sfs]
            ysm = ysm[_sfs]
        elif self.par.smooth_fix == 'redo':
            for i in range(len(y) - redo, len(y)):
                ave = 0.0
                cnt = 0
                for j in range(i, len(y)):
                    ave += y[j]
                    cnt += 1
                ysm[i] = (ave / cnt + ysm[i]) / 2.0
        return xsm, ysm

    def calc(self, x, y):
        if self.par.extra_smooth:
            self.par.extra_smooth = self.par.smooth_fix
            self.par.smooth_fix = 'none'
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
        if self.par.extra_smooth:
            self.par.smooth_fix = self.par.extra_smooth
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
