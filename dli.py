#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import re
import json

import jsonschema
import click
from singleton.singleton import Singleton
from dockerfile_parse import DockerfileParser
from colorama import init, Fore, Style


@Singleton
class Logger(object):
    """Simple Singleton logger with pretty output"""
    def __init__(self):
        init()
        self.has_failures = False

    def warn(self, str):
        print(Fore.YELLOW + '   [WARN] ' + str + Style.RESET_ALL)

    def info(self, str):
        print('========> ' + str)

    def success(self, str):
        print(Fore.GREEN + '[SUCCESS] ' + str + Style.RESET_ALL)

    def error(self, str):
        print(Fore.RED + '  [ERROR] ' + str + Style.RESET_ALL)
        self.has_failures = True


class DockerfileNotFoundError(Exception):
    pass

class SchemaNotFoundError(Exception):
    pass


class DockerfileLabelParser(object):
    """Base class for parsing Dockerfile"""
    def __init__(self, path):
        self.logger = Logger.instance()
        if os.path.exists(path):
            parser = DockerfileParser(path=path)
            self.labels = parser.labels
        else:
            self.logger.error("Can't open Dockerfile at '%s'" % path)
            raise DockerfileNotFoundError

class DockerfileLabelLint(DockerfileLabelParser):
    """Class with methods for checking Docker official LABEL rules"""
    def namespaced_labels(self):
        self.logger.info('Check all labels have namespaces')
        for key in self.labels.keys():
            if key.count('.') < 2:
                self.logger.warn("Label '%s' should use a namespace based on reverse DNS notation" % key)

    def reserved_namespaces(self):
        self.logger.info("Check labels don't use reserved namespaces")
        for key in self.labels.keys():
            for reservation in ['com.docker', 'io.docker', 'org.dockerproject']:
                if key.startswith(reservation):
                    self.logger.error("Label '%s' is reserved for internal use" % reservation)

    def valid_characters(self):
        self.logger.info('Check labels only use valid characters')
        for key in self.labels.keys():
            match = re.match('^[a-z0-9-.]+$', key)
            if not match:
                self.logger.error("Label '%s' must consist of lower-cased alphanumeric characters, dots and dashes" % key)

    def valid_start_and_end_characters(self):
        self.logger.info('Check labels start and end with alpanumeric characters')
        for key in self.labels.keys():
            start = re.match('[a-z0-9]', key[0])
            end = re.match('[a-z0-9]', key[-1])
            if not start or not end:
                self.logger.error("Label '%s' must start and end with lower-cased alphanumeric characters" % key)

    def consecutive_dividers(self):
        self.logger.info('Check labels for double dots and dashes')
        for key in self.labels.keys():
            if (key.find('..') > -1) or (key.find('--') > -1):
                self.logger.error("Label '%s' must not contain consecutive dots or dashes" % key)


class DockerfileLabelSchema(DockerfileLabelParser):
    """Class for validating Docker LABELS against a JSON schema"""
    def validate(self, schema):
        self.logger.info("Check labels based on schema in '%s'" % schema)
        if os.path.exists(schema):
            data = {}
            for key in self.labels:
                if self.labels[key].isdigit():
                    data[key] = int(self.labels[key])
                else:
                    data[key] = self.labels[key]

            with open(schema) as schema_file:
                schema_data = json.load(schema_file)
            try:
                jsonschema.validate(data, schema_data)
            except jsonschema.ValidationError as e:
                self.logger.error(str(e))
            except jsonschema.SchemaError as e:
                self.logger.error(str(e))
        else:
            self.logger.error("Schema file '%s' not found" % schema)
            raise SchemaNotFoundError


@click.group()
def cli():
    """Utilities for ensuring LABELS in Dockerfiles are well maintained"""
    pass

@click.command()
@click.option('--dockerfile', default='Dockerfile', help='Path to the Dockerfile')
def lint(dockerfile):
    """Check for common issues with Dockerfile LABELS"""
    try:
        linter = DockerfileLabelLint(path=dockerfile)

        # All (third-party) tools should prefix their keys with the
        # reverse DNS notation of a domain controlled by the author.
        # For example, com.example.some-label.
        linter.namespaced_labels()

        # The com.docker.*, io.docker.* and org.dockerproject.* namespaces
        # are reserved for Docker’s internal use.
        linter.reserved_namespaces()

        # Keys should only consist of lower-cased alphanumeric characters,
        # dots and dashes (for example, [a-z0-9-.]).
        linter.valid_characters()

        # Keys should start and end with an alpha numeric character.
        linter.valid_start_and_end_characters()

        # Keys may not contain consecutive dots or dashes.
        linter.consecutive_dividers()

        logger = Logger.instance()
        if logger.has_failures:
            sys.exit(2)

    except DockerfileNotFoundError:
        sys.exit(3)


@click.command()
@click.option('--dockerfile', default='Dockerfile', help='Path to the Dockerfile')
@click.option('--schema', default='schema.json', help='Path to the JSON schema')
def validate(dockerfile, schema):
    """Validate Dockerfile LABELS based on a JSON schema"""
    try:
        validator = DockerfileLabelSchema(path=dockerfile)
        validator.validate(schema=schema)
        logger = Logger.instance()
        if logger.has_failures:
            sys.exit(2)
    except (SchemaNotFoundError, DockerfileNotFoundError):
        sys.exit(3)


cli.add_command(lint)
cli.add_command(validate)
