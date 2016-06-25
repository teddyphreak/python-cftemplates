import boto3

from cftemplates import config


def validate_template(template, region):
    assert region in regions()
    return boto3.client('cloudformation', region_name=region).validate_template(TemplateBody=template)['Description']


def regions():
    return config.value('regions', 'all').split(',')


def region_zones(region):
    assert region in regions()
    availability_zones = boto3.client('ec2', region_name=region).describe_availability_zones(
        Filters=[{'Name': 'region-name', 'Values': [region]}]
    )['AvailabilityZones']
    return map(lambda x: x['ZoneName'], availability_zones)


def zones():
    return dict(map(lambda r: [r, region_zones(r)], regions()))


def test_regions():
    return config.value('regions', 'test').split(',')
