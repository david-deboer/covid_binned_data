from datetime import datetime


def date_to_string(date, fmt='%m/%d/%Y'):
    return datetime.strftime(date, fmt)


def string_to_date(date, strings_to_try=['%m/%d/%y', '%m/%d/%Y', '%Y%m%d'], return_format=False):
    if isinstance(strings_to_try, str):
        strings_to_try = [strings_to_try]
    if isinstance(date, datetime):
        return date
    for fmt in strings_to_try:
        try:
            dt = datetime.strptime(date, fmt)
            if return_format:
                return fmt
            return dt
        except ValueError:
            continue
        except TypeError:
            break
    return None


def proc_kwargs(kwargs, allowed_dict):
    return_values = []
    for k, v in allowed_dict.items():
        if k in kwargs.keys():
            return_values.append(kwargs[k])
        else:
            return_values.append(allowed_dict[k])
    if len(return_values) == 1:
        return return_values[0]
    return return_values


def plot_kwargs(kwargs):
    """
    Specializes proc_kwargs for plots.
    """
    plt_args = {'alpha': None,
                'color': None,
                'linestyle': None,
                'linewidth': None,
                'marker': None,
                'markersize': None,
                'label': None
                }
    for k, v in plt_args.items():
        try:
            plt_args[k] = kwargs[k]
        except KeyError:
            continue
    return plt_args
