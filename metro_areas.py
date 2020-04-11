import json
from . import get_fip, mymaps_utils


def get(area_type):
    metro_area_file = mymaps_utils.datafn('metro_areas.json')
    with open(metro_area_file, 'r') as fp:
        metro = json.load(fp)
    arty = {'districts': ['Congress_District', 'cd116fp'],
            'counties': ['Counties', 'countyfp']}
    for ay, aylist in arty.items():
        if area_type in aylist:
            area_type = ay
            break
    else:
        print("{} not found.".format(area_type))
    pma = {}
    for abbr, data in metro.items():
        pma[abbr] = []
        is_state = get_fip.state(data['state'])
        if not is_state:
            print("Not finding {}: {}".format(abbr, data['state']))
            continue
        statefp = is_state[0]
        for distr in data[area_type]:
            if area_type == "districts":
                pma[abbr].append('{}-{:02d}'.format(statefp, distr))
            elif area_type == 'counties':
                pma[abbr].append('{}-{:03d}'.format(statefp, distr))
    return pma
