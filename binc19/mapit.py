from . import viewer, stats, binc_util
from mymaps import us_map, get_fip, mm_util
import math


def setmap(set='Confirmed', geo='County', plot_type='slope', ind=-1, **kwargs):
    """
    Plot time sequences.

    Parameters
    ----------
    set : str
        'Confirmed', 'Deaths'
    geo : str
        'Country', 'State', 'County', 'Congress', 'CSA', 'Urban', 'Native'
    plot_type : str
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
        range : float
        not_included_color : None/str
        per_capita : True/False
        iso_state : None/str
    """
    data_d = {'clip': None, 'datamax': None, 'datamin': 0.0, 'range': 0.0}
    clip, datamax, datamin, range = binc_util.proc_kwargs(kwargs, data_d)
    other_d = {'log_or_linear': 'linear', 'not_included_color': 'w',
               'per_capita': False, 'iso_state': None}
    iso_state, log_or_linear, not_included_color, per_capita = binc_util.proc_kwargs(kwargs, other_d)  # noqa
    this_title = '{} {} {}'.format(set, geo, plot_type)

    state_based = ['State', 'County', 'Congress']
    if per_capita:
        if geo == 'State':
            electoral = mm_util.get_electoral()['states']
        else:
            print("Currently only per capita for state.")
            per_capita = False
    filename = "Bin_{}_{}.csv".format(set, geo)
    b = viewer.View(filename)
    data = {}
    for key in b.Key:
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
        calcit = True
        if iso_state and geo in state_based and sfp.abbr != iso_state:
            calcit = False
            data[this_key] = '0.6'
        if calcit:
            this_data = b.row(key, colname='Key')
            _xx, _yyt = stats.stat_dat(b.dates, this_data, dtype=plot_type, **kwargs)
            this_data = _yyt[ind] / norm
            if log_or_linear == 'log':
                if this_data > 0.0:
                    data[this_key] = math.log10(this_data)
                else:
                    data[this_key] = 0.0
            else:
                data[this_key] = this_data
    geocl, info = us_map.prep_map_data(geo, data, datamin, datamax, clip, range)
    us_map.map_area(geocl, info, not_included_color=not_included_color, title=this_title)
