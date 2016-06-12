from boto import cloudformation, ec2

from cftemplates import config


def validate_template(region, template):
    return cloudformation.connect_to_region(region).validate_template(template)


def regions():
    blacklist = config
    return [region.name for region in cloudformation.regions() if region.name not in config.value('regions', 'blacklist')]


def region_zones(region):
    return [z.name for z in ec2.connect_to_region(region).get_all_zones()]


def zones():
    return dict([[r, region_zones(r)] for r in regions()])

