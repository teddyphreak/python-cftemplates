from troposphere import ec2, Ref

from .utils import cftemplate
from .utils import identity


def vpc_template(description='Simple VPC template',
                 fn=identity):
    def base_vpc(t):

        vpc = ec2.VPC(
                "vpc",
                CidrBlock='172.16.0.0/16',
            )

        t.add_resource(vpc)
        t.add_output(
            ec2.Output(
                "vpcId",
                Description='id of the new VPC',
                Value=Ref(vpc)
            )
        )
        return t
    return cftemplate(description, lambda x: fn(base_vpc(x)))


print(vpc_template("hello"))
