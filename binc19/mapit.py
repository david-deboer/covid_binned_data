from . import binc, stats, binc_util
from mymaps import us_map, mm_util
from my_utils import state_variable
import math


map_args = {
            'log_or_linear': 'linear',
            'clip': None,
            'datamax': None,
            'datamin': None,
            'data_bounds': [[-15, -8], [-8, -1]],
            'drange': 0.0,
            'not_included_color': 'w',
            'per_capita': False,
            'iso_state': None,
            'show_overlay': True
            }


def map(cset='Confirmed', geo='County', stat_type='slope', using=-1, **kwargs):
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
    using : int (add str/datetime options) - if not int, hard-coded week-diff-average
    kwargs : see above and under stats
    """

    sv = state_variable.StateVar(label='Map state variables', verbose=False)
    sv.sv_load(map_args, use_to_init=True, var_type=None)
    sv.state(**kwargs)
    kwargs['smooth'] = 0
    print("Using method {}".format(using))

    filename = "Bin_{}_{}.csv".format(cset, geo)
    b = binc.Binc(filename)
    b.calc(stat_type, **kwargs)
    data = {}
    for i in range(b.Ndata):
        key, is_state = binc_util.get_key_from_id(geo, b.ID[i])
        if key:
            if isinstance(using, int):
                this_data = b.st_data[stat_type][b.ID[i]][using]
            else:
                wk0 = stats.get_derived_value('average', sv.data_bounds[0],
                                              b.st_date[stat_type],
                                              b.st_data[stat_type][b.ID[i]])
                wk1 = stats.get_derived_value('average', sv.data_bounds[1],
                                              b.st_date[stat_type],
                                              b.st_data[stat_type][b.ID[i]])
                if abs(wk0) < 0.1:
                    wk0 = 1.0
                if using == 'diff':
                    this_data = wk1 - wk0
                elif using == 'lastweek':
                    this_data = wk1
                else:
                    this_data = 100.0 * (wk1 - wk0) / wk0
            if sv.log_or_linear == 'log':
                this_val = 0.0 if this_data < 1.0 else math.log10(this_data)
            else:
                this_val = this_data
            if sv.iso_state:
                if is_state == sv.iso_state:
                    data[key] = this_val
                continue
            data[key] = this_val
    colors = mm_util.colormap(data, datamin=sv.datamin, datamax=sv.datamax, clip=sv.clip)
    mapping = None
    if geo == 'CSA':
        mapping = us_map.areas('State')
    us_map.areas(geo, colors, mapping=mapping)
