from troposphere import ec2

from cftemplates import config
from .networks import networks
from .utils import cftemplate
from .utils import identity


def vpc_template(description='Simple VPC template',
                 fn=identity,
                 nets=networks(),
                 azs=config.value('zones', 'default')):
#    network_map = {r: {z: s for z, s in ns.items() if z != 'region'} for r, ns in nets.items()}

    def base_vpc(t):
        vpc = ec2.VPC(
            "vpc",
            CidrBlock="192.168.0.0/24"
#            CidrBlock=FindInMap("NetworkMap", Ref("AWS::Region"), "region"),
        )

#        for z in azs:
#            subnet = ec2.Subnet(AvailabilityZone=Join(Ref("AWS::Region"), z))
#            t.add_resource(subnet)
#
#        t.add_mapping('NetworkMap', network_map)
        t.add_resource(vpc)
#        t.add_output(
#            ec2.Output(
#                "vpcId",
#                Description='id of the new VPC',
#                Value=Ref(vpc)
#            )
#        )
        return t

    return cftemplate(description, lambda t: fn(base_vpc(t)))

