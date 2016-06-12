from troposphere import Template as template


def identity(x):
    return x


def merge_dict(o, m):
    def merge_items(io, im):
        merged_item = {}
        if isinstance(io, dict) and isinstance(im, dict):
            merged_item = merge_dict(io, im)
        else:
            merged_item = im or io
        return merged_item
    keys = frozenset(o.keys() + m.keys())
    return dict([[k, merge_items(o[k], m[k])] for k in keys])


def cftemplate(description,
               fn=identity):
    t = template()
    t.add_version('2010-09-09')
    t.add_description(description)
    return fn(t).to_json()