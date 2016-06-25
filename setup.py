from setuptools import setup, find_packages


setup(
    name='cftemplates',
    version='0.1.1',
    description='Cloudformation templates using troposphere',
    author='Ted Cook',
    author_email='teodoro.cook@gmail.com',
    url='https://github.com/teddyphreak/python-cftemplates',
    packages=find_packages(),
    install_requires=[
        'troposphere',
    ],
    tests_require=[
        'boto3',
        'tox',
        'hypothesis',
        'behave',
        'pytest',
        'ipython'
    ],
    entry_points={
        'console_scripts': ['cftemplates=cftemplates:main']
    }
)