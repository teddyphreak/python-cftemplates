import ipaddress

from cftemplates import networks,config


def test_base_network():
    assert networks.base_network('10.0.0.0', '16') == ipaddress.ip_network('10.0.0.0/16')
    assert networks.base_network() == ipaddress.ip_network("{0}/{1}".format(config.value('network', 'range'),
                                                                            config.value('network', 'range_mask')))


def test_networks():
    nets = networks.networks()
    assert 'us-east-1' in nets
    assert 'region' in nets['us-east-1']
    assert nets['us-east-1']['region'].prefixlen == int(config.value('network', 'region_mask'))
    assert 'us-east-1a' in nets['us-east-1']
    assert nets['us-east-1']['us-east-1a'].prefixlen == int(config.value('network', 'zone_mask'))

