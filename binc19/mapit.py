from . import binc, stats, binc_util
from mymaps import us_map, get_fip, mm_util, map_overlay
from ddb_util import state_variable
import json
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

    # this_title = '{} {} {}'.format(cset, geo, stat_type)
    #
    # state_based = ['State', 'County', 'Congress']
    # if par.per_capita:
    #     if geo == 'State':
    #         electoral = mm_util.get_electoral()['states']
    #     else:
    #         print("Currently only per capita for state.")
    #         par.per_capita = False
    filename = "Bin_{}_{}.csv".format(cset, geo)
    b = binc.Binc(filename)
    b.calc(stat_type, **kwargs)
    data = {}
    for i in range(b.Ndata):
        key = binc_util.get_key_from_csv(geo, b.ID[i])
        if key is not None:
            data[key] = b.st_data[stat_type][b.ID[i]][ind]
    #     norm = 1.0
    #     if geo in state_based:
    #         if geo == 'State':
    #             sfp = get_fip.state(key)
    #             this_key = sfp.fip
    #             if par.per_capita:
    #                 try:
    #                     norm = electoral[sfp.name][0] / 100000.0
    #                 except KeyError:
    #                     continue
    #         else:
    #             sta, c_c = key.split('-')
    #             sfp = get_fip.state(sta)
    #             this_key = '-'.join([sfp.fip, c_c])
    #
    #     else:
    #         this_key = key
    #     if par.iso_state and geo in state_based and sfp.abbr != par.iso_state:
    #         continue
    #     if b.Name[i] == 'Unassigned':
    #         continue
    #     if isinstance(ind, int):
    #         this_data = b.st_data[stat_type][key][ind]
    #     else:
    #         wk0 = stats.get_derived_value('average', [-15, -8],
    #                                       b.st_date[stat_type], b.st_data[stat_type][key])
    #         wk1 = stats.get_derived_value('average', [-8, -1],
    #                                       b.st_date[stat_type], b.st_data[stat_type][key])
    #         if abs(wk0) < 0.1:
    #             wk0 = 1.0
    #         if ind == 'diff':
    #             this_data = wk1 - wk0
    #         else:
    #             this_data = 100.0 * (wk1 - wk0) / wk0
    #     rkey = '{:09d}{}'.format(int(this_data), b.Name[i])
    #     try:
    #         ranked[rkey] = [this_data, b.Name[i], b.State[i]]
    #     except AttributeError:
    #         ranked[rkey] = [this_data, b.Name[i]]
    #     ave_lat += b.Latitude[i] * this_data
    #     ave_lon += b.Longitude[i] * this_data
    #     tot += this_data
    #     this_data /= norm
    #     if par.log_or_linear == 'log':
    #         if this_data > 0.0:
    #             data[this_key] = math.log10(this_data)
    #         else:
    #             data[this_key] = 0.0
    #     else:
    #         data[this_key] = this_data
    # ave_lon /= tot
    # ave_lat /= tot
    # print("Total: {}".format(tot))
    colors = mm_util.colormap(data)
    this_m = us_map.areas(geo, colors)
    # if par.show_overlay:
    #     map_overlay.overlay(this_m.lo48, this_m.ax, [ave_lon], [ave_lat], label=None, color='b',
    #                         size=tot, alpha=None, max_marker_size=None)
    #
    # for rk, rv in sorted(ranked.items()):
    #     v = rv[0]
    #     loc1 = rv[1]
    #     try:
    #         loc2 = ', {}'.format(rv[2])
    #     except IndexError:
    #         loc2 = ''
    #     print("{:>10.2f}   {}{}".format(v, loc1, loc2))
