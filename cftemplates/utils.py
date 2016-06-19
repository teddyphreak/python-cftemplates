from troposphere import Template as template


def identity(x):
    return x


def merge_dict(o, m):
    def merge_items(io, im):
        merged_item = {}
        if isinstance(io, dict) and isinstance(im, dict):
            merged_item = merge_dict(io, im)
        else:
            merged_item = im if im is not None else io
        return merged_item
    keys = frozenset(list(o.keys()) + list(m.keys()))
    merged = ((o and m) and dict([[k, merge_items(o.get(k, None), m.get(k, None))] for k in keys])) or o or m
    return merged


def cftemplate(description,
               fn=identity):
    t = template()
    t.add_version('2010-09-09')
    t.add_description(description)
    return fn(t).to_json()