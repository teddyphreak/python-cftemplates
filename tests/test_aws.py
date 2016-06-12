import urllib.request

from cftemplates import aws


def test_validate_template():
    template_url = 'https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2' + \
        '/EC2InstanceWithSecurityGroupSample.template'
    with urllib.request.urlopen(template_url) as response:
        assert type(aws.validate_template('us-west-2', response.read())).__name__ == 'Template'


def test_regions():
    assert aws.regions()
    assert 'us-east-1' in aws.regions()


def test_region_zones():
    assert 'us-east-1a' in aws.region_zones('us-east-1')


def test_zones():
    assert 'us-east-1a' in aws.zones()['us-east-1']
