from . import binc, binc_util, stats
from mymaps import us_map, get_fip, mm_util, map_overlay
import json
import math


def setmap(cset='Confirmed', geo='County', stat_type='slope', ind=-1, **kwargs):
    """
    Plot maps.

    Parameters
    ----------
    cset : str
        'Confirmed', 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'
    stat_type : str
        'row', 'slope', 'logslope', 'accel', 'frac'
    ind : int (add str/datetime options)
    kwargs:
        smooth : None or int
        low_clip : None or float
        kernel : None or str
        same_plot : bool
        save_stats : bool
        log_or_linear : str
        clip : None/float
        datamax : None/float
        datamin : None/float
        drange : float
        not_included_color : None/str
        per_capita : True/False
        iso_state : None/str
    """
    data_d = {'clip': None, 'datamax': None, 'datamin': 0.0, 'drange': 0.0}
    clip, datamax, datamin, drange = binc_util.proc_kwargs(kwargs, data_d)
    other_d = {'log_or_linear': 'linear', 'not_included_color': 'w',
               'per_capita': False, 'iso_state': None}
    iso_state, log_or_linear, not_included_color, per_capita = binc_util.proc_kwargs(kwargs, other_d)  # noqa
    this_title = '{} {} {}'.format(cset, geo, stat_type)

    state_based = ['State', 'County', 'Congress']
    if per_capita:
        if geo == 'State':
            electoral = mm_util.get_electoral()['states']
        else:
            print("Currently only per capita for state.")
            per_capita = False
    filename = "Bin_{}_{}.csv".format(cset, geo)
    b = binc.Binc(filename)
    b.calc(stat_type, **kwargs)
    data = {}
    if iso_state and geo in state_based:
        with open(get_fip.sfp_file, 'r') as fp:
            states = json.load(fp)
        for sv in states.values():
            if sv[1] == iso_state or int(sv[0]) > 59:
                continue
            if geo == 'County':
                scs = get_fip.get_all_county_fip(sv[0])
            elif geo == 'Congress':
                scs = get_fip.get_all_congress_fip(sv[0])
            else:
                scs = [-1]
            for sc in scs:
                if scs == -1:
                    key = sv[0]
                else:
                    key = '{}-{}'.format(sv[0], sc)
                data[key] = '0.6'
    ave_lat = 0.0
    ave_lon = 0.0
    tot = 0.0
    ranked = {}
    for i in range(b.Ndata):
        key = b.Key[i]
        norm = 1.0
        if geo in state_based:
            if geo == 'State':
                sfp = get_fip.state(key)
                this_key = sfp.fip
                if per_capita:
                    try:
                        norm = electoral[sfp.name][0] / 100000.0
                    except KeyError:
                        continue
            else:
                sta, c_c = key.split('-')
                sfp = get_fip.state(sta)
                this_key = '-'.join([sfp.fip, c_c])

        else:
            this_key = key
        if iso_state and geo in state_based and sfp.abbr != iso_state:
            continue
        if b.Name[i] == 'Unassigned':
            continue
        # this_data = b.st_data[stat_type][key][ind]
        wk0 = stats.get_derived_value('average', [-15, -8],
                                      b.st_date[stat_type], b.st_data[stat_type][key])
        wk1 = stats.get_derived_value('average', [-8, -1],
                                      b.st_date[stat_type], b.st_data[stat_type][key])
        if abs(wk0) < 0.1:
            wk0 = 1.0
        this_data = wk1 - wk0
        # this_data = 100.0 * (wk1 - wk0) / wk0
        rkey = '{:09d}{}'.format(int(this_data), b.Name[i])
        ranked[rkey] = [this_data, b.Name[i], b.State[i]]
        ave_lat += b.Latitude[i] * this_data
        ave_lon += b.Longitude[i] * this_data
        tot += this_data
        this_data /= norm
        if log_or_linear == 'log':
            if this_data > 0.0:
                data[this_key] = math.log10(this_data)
            else:
                data[this_key] = 0.0
        else:
            data[this_key] = this_data
    ave_lon /= tot
    ave_lat /= tot
    print("Total: {}".format(tot))
    geocl, info = us_map.prep_map_data(geo, data, datamin, datamax, clip, drange)
    this_m = us_map.map_area(geocl, info, not_included_color=not_included_color, title=this_title)
    map_overlay.overlay(this_m.lo48, this_m.ax, [ave_lon], [ave_lat], label=None, color='b',
                        size=tot, alpha=None, max_marker_size=None)

    for rk, rv in sorted(ranked.items()):
        print(rv)
