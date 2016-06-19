from ipaddress import ip_network

from cftemplates import networks,config


def test_base_network():
    assert networks.base_network('10.0.0.0', '16') == ip_network('10.0.0.0/16')
    assert networks.base_network() == ip_network("{0}/{1}".format(config.value('network', 'range'),
                                                                  config.value('network', 'range_mask')))


def test_networks_without_assignments():
    nets = networks.networks()
    assert 'us-east-1' in nets
    assert 'region' in nets['us-east-1']
    assert ip_network(nets['us-east-1']['region']).prefixlen == int(config.value('network', 'region_mask'))
    assert 'us-east-1a' in nets['us-east-1']
    assert ip_network(nets['us-east-1']['us-east-1a']).prefixlen == int(config.value('network', 'zone_mask'))


def test_networks_with_assignments():
    nets = networks.networks({'us-west-1': {'region': '10.10.0.0/16', 'us-east-1a': '10.10.1.0/24'}})
    # test new networks
    assert 'us-east-1' in nets
    assert 'region' in nets['us-east-1']
    assert ip_network(nets['us-east-1']['region']).prefixlen == int(config.value('network', 'region_mask'))
    assert 'us-east-1a' in nets['us-east-1']
    assert ip_network(nets['us-east-1']['us-east-1a']).prefixlen == int(config.value('network', 'zone_mask'))
    # test assigned networks
    assert 'us-west-1' in nets
    assert 'region' in nets['us-west-1']
    assert nets['us-west-1']['region'] == "10.10.0.0/16"
    assert nets['us-west-1']['us-east-1a'] == "10.10.1.0/24"
