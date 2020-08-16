from datetime import datetime


def date_to_string(date, fmt='%m/%d/%Y'):
    return datetime.strftime(date, fmt)


def string_to_date(date, strings_to_try=['%m/%d/%y', '%m/%d/%Y', '%Y%m%d', '%Y-%m-%d'],
                   return_format=False):
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


def fix_lists(data, list_len=1, output_type=str, split_on=','):
    if isinstance(data, str):
        data = [output_type(x) for x in data.split(split_on)]
    elif not isinstance(data, list):
        data = [data]
    if len(data) == 1:
        data = data * list_len
    if len(data) != list_len:
        raise ValueError("{} not of length {}".format(data, list_len))
    return data


def read_statfile(filename):
    data = {}
    with open(filename, 'r') as fp:
        for i, line in enumerate(fp):
            if not i:
                header = line.split()
                print(line)
                for hdr in header:
                    data[hdr] = []
                continue
            this_data = line.split()
            for j, d in enumerate(this_data):
                if not j:
                    data['Date'].append(datetime.strptime(d, '%Y-%m-%d'))
                else:
                    data[header[j]].append(float(d))
    return data


def proc_kwargs(kwargs, allowed_dict):
    return_values = []
    sort_keys = sorted(allowed_dict.keys())
    for k in sort_keys:
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
