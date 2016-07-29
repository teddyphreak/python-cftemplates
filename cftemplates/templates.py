from troposphere import Template as template


def empty(x):
    """
    Defines the identity/empty template

    :param x: A base template definition
    :return: trophosphere.Template, the identity/empty template definition
    """
    return x


def cftemplate(description,
               fn=empty):
    """
    Create a JSON representation of the template

    :param description: a description for the template
    :param fn: a function defining template elements
    :return: String, a JSON representation of the template
    """
    t = template()
    t.add_version('2010-09-09')
    t.add_description(description)
    return fn(t).to_json()

