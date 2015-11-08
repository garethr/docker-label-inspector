from setuptools import setup

setup(
    name='docker-label-inspector',
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
    description='A tool for linting and validating labels '
                'in Dockerfiles.',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)
