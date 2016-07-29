from hypothesis import given
from hypothesis.strategies import text, dictionaries

from cftemplates import utils


@given(dictionaries(text(), text()), dictionaries(text(), text()))
def test_merge_simple_dict(d1, d2):
    """
    Test cftemplates.utils.merge_dict

    :param d1: A dictionary
    :param d2: A dictionary
    """
    dm = utils.merge_dict(d1, d2)
    for k in list(d1.keys()) + list(d2.keys()):
        assert k in list(dm.keys())
    for k in dm:
        assert k in d2 and d2[k] == dm[k] or k in d1 and d1[k] == dm[k]


@given(dictionaries(text(), dictionaries(text(), text())),
       dictionaries(text(), dictionaries(text(), text())))
def test_merge_nested_dict(d1, d2):
    """
    Test cftemplates.utils.merge_dict

    :param d1: A dictionary
    :param d2: A dictionary
    """
    dm = utils.merge_dict(d1, d2)
    for k in list(d1.keys()) + list(d2.keys()):
        assert k in list(dm.keys())
    for k in dm.keys():
        assert (k in d1 and k in d2) and dm[k] == {**d1[k], **d2[k]} \
               or k in d2 and d2[k] == dm[k] \
               or k in d1 and d1[k] == dm[k]

