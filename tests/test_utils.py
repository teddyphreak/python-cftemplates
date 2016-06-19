from hypothesis import given
from hypothesis.strategies import text, integers, lists, dictionaries

from cftemplates import utils


@given(text(), integers(), lists(text()), dictionaries(text(), text()))
def test_identity(t, n, l, d):
    for x in [t, n, l, d]:
        assert utils.identity(x) == x


@given(dictionaries(text(), text()), dictionaries(text(), text()))
def test_merge_simple_dict(d1, d2):
    dm = utils.merge_dict(d1, d2)
    for k in list(d1.keys()) + list(d2.keys()):
        assert k in list(dm.keys())
    for k in dm:
        assert k in d2 and d2[k] == dm[k] or k in d1 and d1[k] == dm[k]


@given(dictionaries(text(), dictionaries(text(), text())),
       dictionaries(text(), dictionaries(text(), text())))
def test_merge_nested_dict(d1, d2):
    dm = utils.merge_dict(d1, d2)
    for k in list(d1.keys()) + list(d2.keys()):
        assert k in list(dm.keys())
    for k in dm.keys():
        assert (k in d1 and k in d2) and dm[k] == {**d1[k], **d2[k]} \
               or k in d2 and d2[k] == dm[k] \
               or k in d1 and d1[k] == dm[k]
