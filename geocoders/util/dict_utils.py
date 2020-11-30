import collections


def flatten_dict(d, parent_key='', sep='.', suffix=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        new_key = new_key.lower()
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep, suffix=suffix).items())
        else:
            new_key += suffix
            items.append((new_key, v))
    return dict(items)
