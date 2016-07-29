def merge_dict(o, m):
    """
    Merges two dictionaries. If a key is present in both dictionaries, their corresponding values are merged together
    in the resulting merged dictionary

    :param o: First input dictionary
    :param m: Second input dictionary
    :return: Dictionary, The merged dictionary
    """
    def merge_items(io, im):
        if isinstance(io, dict) and isinstance(im, dict):
            merged_item = merge_dict(io, im)
        else:
            merged_item = im if im is not None else io
        return merged_item

    keys = frozenset(list(o.keys()) + list(m.keys()))
    merged = ((o and m) and dict([[k, merge_items(o.get(k, None), m.get(k, None))] for k in keys])) or o or m
    return merged

