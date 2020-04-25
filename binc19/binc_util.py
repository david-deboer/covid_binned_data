from datetime import datetime


def string_to_date(date, strings_to_try=['%m/%d/%y', '%m/%d/%Y', '%Y%m%d'], return_format=False):
    if isinstance(strings_to_try, str):
        strings_to_try = [strings_to_try]
    for fmt in strings_to_try:
        try:
            dt = datetime.strptime(date, fmt)
            if return_format:
                return fmt
            return dt
        except ValueError:
            continue


def plot_kwargs(**kwargs):
    plt_args = {'alpha': None,
                'color': None,
                'linestyle': None,
                'linewidth': None,
                'marker': None,
                'markersize': None,
                'label': None
                }
    for k, v in kwargs.items():
        if k == 'lw':
            k = 'linewidth'
        elif k == 'ls':
            k = 'linestyle'
        elif k == 'ms':
            k = 'markersize'
        try:
            plt_args[k] = v
        except KeyError:
            continue
    return plt_args
