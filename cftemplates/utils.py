from time import sleep

import boto3
from troposphere import Template as template

from cftemplates import aws


def identity(x):
    return x


def merge_dict(o, m):
    def merge_items(io, im):
        merged_item = {}
        if isinstance(io, dict) and isinstance(im, dict):
            merged_item = merge_dict(io, im)
        else:
            merged_item = im if im is not None else io
        return merged_item

    keys = frozenset(list(o.keys()) + list(m.keys()))
    merged = ((o and m) and dict([[k, merge_items(o.get(k, None), m.get(k, None))] for k in keys])) or o or m
    return merged


def cftemplate(description,
               fn=identity):
    t = template()
    t.add_version('2010-09-09')
    t.add_description(description)
    return fn(t).to_json()


def test_cftemplate(region, template_name):
    validated = False
    with open(template_name) as template_file:
        template_body = template_file.read()
        validated = aws.validate_template(template_body, region) and True
    return validated


def test_cfstack(region,
                 template_name,
                 stack_name="cfstacktest",
                 timeout_minutes=5):
    cf_client = boto3.client('cloudformation', region_name=region)
    if filter(lambda x: x['StackName'] == stack_name, cf_client.describe_stacks()['Stacks']):
        cf_client.delete_stack(StackName=stack_name)
        sleep(30)
    with open(template_name) as template_file:
        template_body = template_file.read()
        stack = cf_client.create_stack(StackName=stack_name,
                                       TemplateBody=template_body,
                                       TimeoutInMinutes=timeout_minutes)
    cycles = 6
    stack_status = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while stack_status == "CREATE_IN_PROGRESS" and cycles > 0:
        sleep(timeout_minutes * 60 / cycles)
        cycles -= 1
        stack_status = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    cf_client.delete_stack(StackName=stack_name)
    print(stack_status)
    return stack_status
