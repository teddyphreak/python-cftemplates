from configparser import ConfigParser as cp
from ipaddress import ip_network
from os import path

from pkg_resources import resource_filename

from cftemplates import aws
from cftemplates import config
from cftemplates import utils


def base_network(address=config.value('network', 'range'),
                 base_mask=config.value('network', 'range_mask')):
    return ip_network("{0}/{1}".format(address, base_mask))


def assigned_networks(overrides=config.value('config', 'network_overrides'),
                      defaults=config.value('config', 'network_defaults')):
    default_config_file = resource_filename(__name__, defaults)
    assigned_region_networks = {}
    if path.isfile(default_config_file) or path.isfile(overrides):
        config_files = filter(lambda x: path.isfile(x), [default_config_file, overrides])
        assigned_config = cp()
        assigned_config.read([config_files])
        assigned_region_networks = assigned_config.sections()
    return assigned_region_networks


def networks(assigned=dict(),
             regions=aws.regions(),
             address=config.value('network', 'range'),
             base_mask=int(config.value('network', 'range_mask')),
             region_mask=int(config.value('network', 'region_mask')),
             zone_mask=int(config.value('network', 'zone_mask'))):

    def candidate_networks():
        configured_networks = [str(v['region']) for k, v in assigned.items()]
        potential_networks = [str(x) for x in base_network(address, base_mask).subnets(new_prefix=region_mask)]
        candidate_networks = filter(lambda x: x not in configured_networks, potential_networks)
        configured_regions = [k for k in assigned]
        candidate_regions = filter(lambda x: x not in configured_regions, regions)
        return utils.merge_dict(assigned,
                                dict(zip(candidate_regions, map(lambda x: {'region': x}, candidate_networks))))

    def candidate_subnets():
        candidate_networks_cache = candidate_networks()
        configured_zones = [filter(lambda x: x != 'region', v.keys()) for r, v in candidate_networks_cache.items()]
        potential_zones = {r: aws.region_zones(r) for r in regions}
        candidate_zones = {r: z for r, z in potential_zones.items() if z not in configured_zones}
        configured_subnets = {r: [s for z, s in v.items() if z != 'region']
                              for r, v in candidate_networks_cache.items()}
        potential_subnets = {r: [str(x) for x in ip_network(v['region']).subnets(new_prefix=zone_mask)]
                             for r, v in candidate_networks_cache.items()}
        candidate_subnets = {r: filter(lambda x: x not in configured_subnets[r], v)
                             for r, v in potential_subnets.items()}
        return utils.merge_dict(candidate_networks_cache,
                                {r: dict(zip(candidate_zones[r], candidate_subnets[r])) for r in regions})

    return candidate_subnets()

