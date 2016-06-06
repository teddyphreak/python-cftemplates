from troposphere import ec2 as ec2

from cftemplates import identity
from cftemplates import template


def vpc_template(description='Simple VPC template',
                 fn=identity):
    def vpc(t):
        t.add_resource(
            ec2.VPC(
                "vpc",
                CidrBlock='172.16.0.0/16'
            )
        )
        return t
    return template(description, lambda x: fn(vpc(x)))


print(vpc_template("hello"))
