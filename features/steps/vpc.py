from behave import *

@then('aws cloudformation create-stack {template} will succeed')
def step_impl(context, template):
    pass

@then('aws cloudformation validate-template {template} will succeed')
def step_impl(context, template):
    pass