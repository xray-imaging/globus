import argparse
import sys
import configparser
from collections import OrderedDict
import numpy as np
import log_lib


NAME = "globus.conf"
SECTIONS = OrderedDict()

SECTIONS['general'] = {
    'config': {
        'default': NAME,
        'type': str,
        'help': "File name of configuration",
        'metavar': 'FILE'},
    'verbose': {
        'default': True,
        'help': 'Verbose output',
        'action': 'store_true'}}

SECTIONS['experiment'] = {
    'year-month': {
        'default': '2020-12',
        'type': str,
        'help': "Experiment year and month",
        'metavar': 'FILE'},
    'pi-last-name': {
        'default': 'decarlo',
        'type': str,
        'help': "Experiment PI last name",
        'metavar': 'FILE'},
    'pi-email': {
        'default': 'decarlof@gmail.com',
        'type': str,
        'help': "Experiment PI email",
        'metavar': 'FILE'}}

SECTIONS['file-io'] = {
    'input-file-path': {
        'default': '.',
        'type': str,
        'help': "Name of the last file used",
        'metavar': 'PATH'},
    'input-path': {
        'default': '.',
        'type': str,
        'help': "Path of the last used directory",
        'metavar': 'PATH'},
    'output-file-path': {
        'default': '.',
        'type': str,
        'help': "Name of the last output file used",
        'metavar': 'PATH'},
    'output-path': {
        'default': '.',
        'type': str,
        'help': "Path of the last output used directory",
        'metavar': 'PATH'},

        }

SECTIONS['globus'] = {
    'app-id': {
        'default': 'a9badd00-39c3-4473-b180-8bccc113ba1d', # for usr32idc
        'type': str,
        'help': "App id UUID, to create one see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client",
        'metavar': 'PATH'},
    'personal-endpoint-name': {
        'type': str,
        'default': 'handyn',
        'help': "Personal endpoint name"},
    'personal-endpoint-uuid': {
        'type': str,
        'default': 'f1f39c62-ec26-11e8-8cab-0a1d4c5c824a',
        'help': "Personal endpoint UUID"},
    'personal-endpoint-top-dir': {
        'type': str,
        'default': '/local/data/',
        'help': "Personal endpoint top directory"},
    'globus-server-name': {
        'type': str,
        'default': 'petrel',
        'help': "Globus server name"},
    'globus-server-uuid': {
        'type': str,
        'default': 'e133a81a-6d04-11e5-ba46-22000b92c6ec', # petrel tomography
        'help': "Globus server UUID"},
    'globus-message': {
        'type': str,
        'default': 'Notification Message to user',
        'help': "Globus server UUID"},
    'globus-server-top-dir': {
        'type': str,
        'default': '/2-BM/',
        'help': "Globus server top directory"}}



GLOBUS_PARAMS = ('file-io', 'globus', 'experiment')

NICE_NAMES = ('General', 'Input')

def get_config_name():
    """Get the command line --config option."""
    name = NAME
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--config'):
            if arg == '--config':
                return sys.argv[i + 1]
            else:
                name = sys.argv[i].split('--config')[1]
                if name[0] == '=':
                    name = name[1:]
                return name

    return name


def parse_known_args(parser, subparser=False):
    """
    Parse arguments from file and then override by the ones specified on the
    command line. Use *parser* for parsing and is *subparser* is True take into
    account that there is a value on the command line specifying the subparser.
    """
    if len(sys.argv) > 1:
        subparser_value = [sys.argv[1]] if subparser else []
        config_values = config_to_list(config_name=get_config_name())
        values = subparser_value + config_values + sys.argv[1:]
        #print(subparser_value, config_values, values)
    else:
        values = ""

    return parser.parse_known_args(values)[0]


def config_to_list(config_name=NAME):
    """
    Read arguments from config file and convert them to a list of keys and
    values as sys.argv does when they are specified on the command line.
    *config_name* is the file name of the config file.
    """
    result = []
    config = configparser.ConfigParser()

    if not config.read([config_name]):
        return []

    for section in SECTIONS:
        for name, opts in ((n, o) for n, o in SECTIONS[section].items() if config.has_option(section, n)):
            value = config.get(section, name)

            if value is not '' and value != 'None':
                action = opts.get('action', None)

                if action == 'store_true' and value == 'True':
                    # Only the key is on the command line for this action
                    result.append('--{}'.format(name))

                if not action == 'store_true':
                    if opts.get('nargs', None) == '+':
                        result.append('--{}'.format(name))
                        result.extend((v.strip() for v in value.split(',')))
                    else:
                        result.append('--{}={}'.format(name, value))

    return result


class Params(object):
    def __init__(self, sections=()):
        self.sections = sections + ('general', )

    def add_parser_args(self, parser):
        for section in self.sections:
            for name in sorted(SECTIONS[section]):
                opts = SECTIONS[section][name]
                parser.add_argument('--{}'.format(name), **opts)

    def add_arguments(self, parser):
        self.add_parser_args(parser)
        return parser

    def get_defaults(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)

        return parser.parse_args('')


def write(config_file, args=None, sections=None):
    """
    Write *config_file* with values from *args* if they are specified,
    otherwise use the defaults. If *sections* are specified, write values from
    *args* only to those sections, use the defaults on the remaining ones.
    """
    config = configparser.ConfigParser()

    for section in SECTIONS:
        config.add_section(section)
        for name, opts in SECTIONS[section].items():
            if args and sections and section in sections and hasattr(args, name.replace('-', '_')):
                value = getattr(args, name.replace('-', '_'))
                if isinstance(value, list):
                    print(type(value), value)
                    value = ', '.join(value)
            else:
                value = opts['default'] if opts['default'] is not None else ''

            prefix = '# ' if value is '' else ''

            if name != 'config':
                config.set(section, prefix + name, str(value))
    with open(config_file, 'w') as f:
        config.write(f)


def log_values(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k in SECTIONS[section]))

        if entries:
            log_lib.info(name)

            for entry in entries:
                value = args[entry] if args[entry] is not None else "-"
                log_lib.info("  {:<16} {}".format(entry, value))
