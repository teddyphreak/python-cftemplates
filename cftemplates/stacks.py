from time import sleep

import boto3


def test_cfstackbody(region,
                     template_body,
                     stack_name="cfstacktest",
                     timeout_minutes=5):
    """
    Test stack creation in AWS cloudformation

    :param region:  The region for creating the test stack
    :param template_name: The name/filename of the test template
    :param template_body: The template body to test
    :param timeout_minutes: A timeout for stack creation
    :return: String, CREATE_COMPLTETE if stack creation succeeded, undefined otherwise
    """
    cf_client = boto3.client('cloudformation', region_name=region)
    if filter(lambda x: x['StackName'] == stack_name, cf_client.describe_stacks()['Stacks']):
        cf_client.delete_stack(StackName=stack_name)
        sleep(30)
    cf_client.create_stack(StackName=stack_name,
                           TemplateBody=template_body,
                           TimeoutInMinutes=timeout_minutes)
    cycles = 6
    stack_status = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while stack_status == "CREATE_IN_PROGRESS" and cycles > 0:
        sleep(timeout_minutes * 60 / cycles)
        cycles -= 1
        stack_status = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    cf_client.delete_stack(StackName=stack_name)
    return stack_status


def test_cfstack(region,
                 template_name,
                 stack_name="cfstacktest",
                 timeout_minutes=5):
    """
    Test stack creation in AWS cloudformation

    :param region:  The region for creating the test stack
    :param template_name: The name/filename of the test template
    :param stack_name: A name for the test stack
    :param timeout_minutes: A timeout for stack creation
    :return: String, CREATE_COMPLTETE if stack creation succeeded, undefined otherwise
    """
    stack_status = None
    with open(template_name) as template_file:
        template_body = template_file.read()
        stack_status = test_cfstackbody(region, template_name, template_body, stack_name, timeout_minutes)
    return stack_status
