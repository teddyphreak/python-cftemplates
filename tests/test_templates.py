import boto3
from troposphere import ec2

from cftemplates import stacks
from cftemplates import templates


def test_identity():
    """
    Test function cftemplates.templates.identity
    """
    for x in ["test", 0, 1, 10, 100, [], ["test"]]:
        assert templates.empty(x) == x


def test_cftemplatebody(r='us-west-1', d='description'):
    """
    Test function cftemplates.templates.cftemplate

    :param r: The test region name
    :param d: A test description
    """
    def vpc(t):
        t.add_resource(ec2.VPC("vpc", CidrBlock="192.168.0.0/24"))
        return t
    cf_client = boto3.client('cloudformation', region_name=r)
    template = templates.cftemplate(d, lambda t: vpc(t))
    assert stacks.test_cfstackbody(region=r, template_body=template) == "CREATE_COMPLETE"
