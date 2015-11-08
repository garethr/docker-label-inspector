from setuptools import setup

setup(
    name='dli',
    author='Gareth Rushgrove',
    author_email='gareth@morethanseven.net',
    url='http://github.com/garethr/dli',
    version='0.1',
    py_modules=['dli'],
    install_requires=[
        'click',
        'jsonschema',
        'colorama',
        'dockerfile-parse',
    ],
    entry_points='''
        [console_scripts]
        dli=dli:cli
    ''',
)
