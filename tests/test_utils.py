import boto3
from hypothesis import given
from hypothesis.strategies import text, integers, lists, dictionaries, sampled_from
from troposphere import ec2

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


@given(sampled_from(['us-east-1', 'us-west-1', 'eu-west-1']),
       sampled_from(['test description 1', 'test description 2']))
def test_cftemplate(r, d):
    def vpc(t):
        t.add_resource(ec2.VPC("vpc", CidrBlock="192.168.0.0/24"))
        return t
    cf_client = boto3.client('cloudformation', region_name=r)
    template = utils.cftemplate(d, lambda t: vpc(t))
    cf_client.validate_template(TemplateBody=template)
