Docker Label Inspector is a tool to help ensure you're providing your
Docker images with the metadata they will need out in the wilds of the
internet.

It provides two useful tools; a label linter and a label validator.


## Usage

The package includes a single executable, called `dli`. You can pass
`--help` to individual commands for additional instructions and options.

```bash
$ dli
Usage: dli [OPTIONS] COMMAND [ARGS]...

  Utilities for ensuring LABELS in Dockerfiles are well maintained

Options:
  --help  Show this message and exit.

Commands:
  lint      Check for common issues with Dockerfile...
  validate  Validate Dockerfile LABELS based on a JSON...
```

## Linter

The linter checks your labels against the [official LABEL
guidelines](http://docs.docker.com/engine/userguide/labels-custom-metadata/).
By default `dli` will check the file called `Dockerfile` in the present
working directory. You can pass a path via the `--dockerfile` option.

```bash
$ dli lint
========> Check all labels have namespaces
   [WARN] Label 'vendor' should use a namespace based on reverse DNS notation
========> Check labels don't use reserved namespaces
========> Check labels only use valid characters
========> Check labels start and end with alpanumeric characters
========> Check labels for double dots and dashes
```

`dli lint` will return a non-zero exit code if it finds any errors. This
should make it useful for integrating into pipelines.

## Validator

The validator validates the labels against a provided [JSON
Schema](http://json-schema.org/). The idea being you can use a custom
schema for your organisation or, eventually, community provided schemas.

```bash
dli validate
========> Check labels based on schema in 'schema.json'
```

You can see a working example in the [example](example) directory. This
includes a sample schema and Dockerfile. You can see sample output from
an invalid Dockerfile below, in this case missing a required parameter.

```bash
$ dli validate
========> Check labels based on schema in 'schema.json'
  [ERROR] u'com.example.is-beta' is a required property

Failed validating u'required' in schema:
    {u'properties': {u'com.example.is-beta': {u'type': u'string'},
                     u'com.example.release-date': {u'type': u'string'},
                     u'com.example.version': {u'description':
u'Version',
                                              u'minimum': 0,
                                              u'type': u'integer'}},
     u'required': [u'com.example.is-beta', u'com.example.version'],
     u'title': u'Dockerfile schema',
     u'type': u'object'}

On instance:
    {u'com.example.release-date': u'2015-02-12',
     u'com.example.version': 1,
     u'vendor': u'ACME Incorporated'}
```


## Installation

For the moment you can install from this repository using `pip`.

```bash
git clone git@github.com:garethr/docker-label-inspector.git
cd docker-label-inspector
pip install .
```
