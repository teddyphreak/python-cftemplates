__all__ = ['vpc']

from troposphere import Template


def identity(x):
    return x


def defaults():
    return(
        {
            'author': 'Ted Cook',
            'email': 'teodoro.cook@gmail.com',
        }
    )


def template(description,
             fn=identity):
    t = Template()
    t.add_version('2010-09-09')
    t.add_description(description)
    return fn(t).to_json()
