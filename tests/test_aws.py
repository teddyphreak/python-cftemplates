import urllib.request

from cftemplates import aws


def test_validate_template():
    template_url = 'https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2' + \
                   '/EC2InstanceWithSecurityGroupSample.template'
    with urllib.request.urlopen(template_url) as response:
        template_body = response.read().decode('utf-8')
    assert type(aws.validate_template(template_body, 'us-west-2')).__name__ == 'str'


def test_regions():
    assert aws.regions()
    for r in aws.test_regions():
        assert r in aws.regions()


def test_region_zones():
    for r in aws.test_regions():
        assert "{0}a".format(r) in aws.region_zones(r)


def test_zones():
    for r in aws.test_regions():
        assert "{0}a".format(r) in aws.zones()[r]
