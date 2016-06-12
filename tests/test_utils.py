from hypothesis import given, strategies
from hypothesis.strategies import text, integers, lists, dictionaries

from cftemplates import utils


@given(text(), integers(), lists(), dictionaries(text(), text()))
def test_identity(t, n, l, d):
    for x in [t, n, l, d]:
        assert utils.identity(x) == x


@given(strategies.dictionaries(text(), text()), strategies.dictionaries(text(), text()))
def test_merge_simple_dict(d1, d2):
    dm = utils.merge_dict(d1, d2).keys()
    for k in d1.keys() + d2.keys():
        assert k in dm
    for k in dm:
        assert k in d2 and d1[k] == dm[k] or k in d1 and d1[k] == dm[k]


@given(dictionaries(text(), dictionaries(text(), text())),
       dictionaries(text(), dictionaries(text(), text())))
def test_merge_nested_dict(d1, d2):
    dm = utils.merge_dict(d1, d2).keys()
    for k in d1.keys() + d2.keys():
        assert k in dm
    for k in dm:
        assert k in d2 and d1[k] == dm[k] or k in d1 and d1[k] == dm[k]
        assert dm[k] == {**d1[k], **d2[k]}
