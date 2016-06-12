import ipaddress
from configparser import ConfigParser as cp
from os import path

from pkg_resources import resource_filename

from cftemplates import aws
from cftemplates import config


def base_network(address=config.value('network', 'range'),
                 base_mask=config.value('network', 'range_mask')):
    return ipaddress.ip_network("{0}/{1}".format(address, base_mask))


def assigned_networks(override_config_file='~/.cftemplates/networks.ini'):
    default_config_file = resource_filename(__name__, '../networks.ini')
    assigned_region_networks = {}
    if path.isfile(default_config_file) or path.isfile(override_config_file):
        config_files = filter(lambda x: path.isfile(x), [default_config_file, override_config_file])
        assigned_config = cp()
        assigned_config.read([config_files])
        assigned_region_networks = assigned_config.sections()
    return assigned_region_networks


def networks():
    return assigned_networks()


def candidate_networks(regions=aws.regions(),
                       address=config.value('network', 'range'),
                       base_mask=int(config.value('network', 'range_mask')),
                       region_mask=int(config.value('network', 'region_mask')),
                       zone_mask=int(config.value('network', 'zone_mask'))):
    assigned_region_networks = networks()
    available_regions = filter(lambda x: x not in assigned_region_networks, regions)
    candidate_region_networks = base_network(address, base_mask).subnets(new_prefix=region_mask)
    available_region_networks = filter(lambda x: assigned_region_networks[x]['config'], candidate_region_networks)
    def region_networks():
        region2net = dict(zip(available_regions, available_region_networks))
        return {**dict(assigned_region_networks), **dict([[r, {'region': region2net[r]}] for r in region2net])}

    def region_subnets():
        assigned_zones = [z
                          for z in assigned_region_networks[r] if z != 'region'
                          for r in assigned_region_networks]
        candidate_zones = [[r, aws.region_zones(r)] for r in regions]
        available_zones = [[r, filter(lambda x: x not in assigned_zones, candidate_zones[r])]]
        assigned_subnets = [assigned_region_networks[r][z]
                            for z in assigned_region_networks[r] if z != 'region'
                            for r in assigned_region_networks]
        candidate_subnets = dict([[r, assigned_region_networks[r]['region'].subnets(new_prefix=zone_mask)]
                                  for r in region_networks()])
        available_subnets = dict([[r, filter(lambda x: x not in assigned_subnets, candidate_subnets[r])]
                                  for r in candidate_subnets])
        available_region_subnets = dict([[r, dict(zip(available_zones, available_subnets))] for r in regions])
        return dict([[r, {**available_region_subnets[r], **assigned_region_networks[r]}] for r in regions])

    return region_subnets()

