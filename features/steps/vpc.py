from behave import *

from cftemplates.aws import test_regions
from cftemplates.utils import test_cfstack, test_cftemplate


@then('aws cloudformation create-stack {template_name} will succeed')
def step_impl(context, template_name):
    for r in test_regions():
        assert test_cfstack(region=r, stack_name="vpcstacktest", template_name=template_name) == "CREATE_COMPLETE"


@then('aws cloudformation validate-template {template_name} will succeed')
def step_impl(context, template_name):
    for r in test_regions():
        assert test_cftemplate(r, template_name) is True
