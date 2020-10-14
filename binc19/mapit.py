from . import binc, stats, binc_util
from mymaps import us_map, mm_util
from ddb_util import state_variable
import math


map_args = {
            'log_or_linear': 'linear',
            'clip': None,
            'datamax': None,
            'datamin': 0,
            'drange': 0.0,
            'not_included_color': 'w',
            'per_capita': False,
            'iso_state': None,
            'show_overlay': True
            }


def map(cset='Confirmed', geo='County', stat_type='slope', ind=-1, **kwargs):
    """
    Plot maps.

    Parameters
    ----------
    cset : str
        'Confirmed', 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA'
    stat_type : str
        'row', 'slope', 'logslope', 'accel', 'frac'
    ind : int (add str/datetime options) - if not int, hard-coded week-diff-average
    kwargs : see above and under stats
    """

    par = state_variable.StateVar(label='Map state variables', verbose=False)
    par.sv_load(map_args, use_to_init=True, var_type=None)
    par.state(**kwargs)
    kwargs['smooth'] = 0
    print("Isolating on ", par.iso_state)

    filename = "Bin_{}_{}.csv".format(cset, geo)
    b = binc.Binc(filename)
    b.calc(stat_type, **kwargs)
    data = {}
    for i in range(b.Ndata):
        key, is_state = binc_util.get_key_from_id(geo, b.ID[i])
        if key:
            if isinstance(ind, int):
                this_data = b.st_data[stat_type][b.ID[i]][ind]
            else:
                wk0 = stats.get_derived_value('average', [-15, -8],
                                              b.st_date[stat_type],
                                              b.st_data[stat_type][b.ID[i]])
                wk1 = stats.get_derived_value('average', [-8, -1],
                                              b.st_date[stat_type],
                                              b.st_data[stat_type][b.ID[i]])
                if abs(wk0) < 0.1:
                    wk0 = 1.0
                if ind == 'diff':
                    this_data = wk1 - wk0
                elif ind == 'lastweek':
                    this_data = wk1
                else:
                    this_data = 100.0 * (wk1 - wk0) / wk0
            if par.log_or_linear == 'log':
                this_val = 0.0 if this_data < 1.0 else math.log10(this_data)
            else:
                this_val = this_data
            if par.iso_state:
                if is_state == par.iso_state:
                    data[key] = this_val
                continue
            data[key] = this_val
    colors = mm_util.colormap(data, datamin=par.datamin, datamax=par.datamax, clip=par.clip)
    us_map.areas(geo, colors)
