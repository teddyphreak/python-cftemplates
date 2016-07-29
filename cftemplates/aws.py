import boto3

from cftemplates import config


def validate_template(template, region):
    '''
    Perform template validation with aws service

    :param template: template body
    :param region: region name
    :return: see [VALIDATE_TEMPLATE]

    .. [VALIDATE_TEMPLATE] http://bit.ly/2a8BB4G
    '''
    assert region in regions()
    return boto3.client('cloudformation', region_name=region).validate_template(TemplateBody=template)['Description']


def regions():
    '''
    Retrieve all valid region names as defined in configuration files

    :return: List[String], all valid region names
    '''
    return config.value('regions', 'all').split(',')


def region_zones(region):
    '''
    Retrieve all zones for a single region

    :param region: a region name
    :return: List[String] a list of zones for the input region
    '''
    assert region in regions()
    availability_zones = boto3.client('ec2', region_name=region).describe_availability_zones(
        Filters=[{'Name': 'region-name', 'Values': [region]}]
    )['AvailabilityZones']
    return map(lambda x: x['ZoneName'], availability_zones)


def zones():
    '''
    Retrieve zones for all regions

    :return: Dictionary[String, String], a dictionary of (region, zone) tuples
    '''
    return dict(map(lambda r: [r, region_zones(r)], regions()))


def test_regions():
    '''
    Retrieve all test regions

    :return: List[String], a list of test regions as defined in configuration files
    '''
    return config.value('regions', 'test').split(',')
