import os
import sys
import pathlib
import argparse
import configparser
import numpy as np
from collections import OrderedDict
from globus import log

CONFIG_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'globus.conf')
TOKEN_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'token.npy')
CREDENTIALS_FILE_NAME = os.path.join(str(pathlib.Path.home()), '.scheduling_credentials')

SECTIONS = OrderedDict()

SECTIONS['general'] = {
    'config': {
        'default': CONFIG_FILE_NAME,
        'type': str,
        'help': "File name of configuration",
        'metavar': 'FILE'},
    'globus-token-file': {
        'default': TOKEN_FILE_NAME,
        'type': str,
        'help': "File name containing the globus access token",
        'metavar': 'FILE'},
    'verbose': {
        'default': True,
        'help': 'Verbose output',
        'action': 'store_true'}}

SECTIONS['scheduling'] = {
    'beamline' : {
        'default' : '7-BM-A,B',
        'type': str,
        'help': "beam line name as define in the APS scheduling system"},
    'set': {     
        'type': float,
        'default': 0,
        'help': "Number of +/- number days for the current date. Used for setting user info for past/future user groups"},
    'url':{
        'default': 'https://beam-api-dev.aps.anl.gov',
        'type': str,
        'help': "URL address of the scheduling system REST API' "},
    'credentials': {
        'default': CREDENTIALS_FILE_NAME,
        'type': str,
        'help': "File name containing the restAPI service credetinals in the format of user|pwd",
        'metavar': 'FILE'},    
    }

# SECTIONS['experiment'] = {
#     'year-month': {
#         'default': '2020-12',
#         'type': str,
#         'help': "Experiment year and month",
#         'metavar': 'FILE'},
#     'pi-last-name': {
#         'default': 'decarlo',
#         'type': str,
#         'help': "Experiment PI last name",
#         'metavar': 'FILE'},
#     'pi-email': {
#         'default': 'decarlof@gmail.com',
#         'type': str,
#         'help': "Experiment PI email",
#         'metavar': 'FILE'}}

SECTIONS['globus'] = {
    'experiment-type': {
        'type': str,
        'default': '7BM',
        'help': 'Experiment type in the DM system'},
    'primary-beamline-contact-badge': {
        'type': int,
        'default': 56788,
        'help': 'Badge name of primary beamline contact.  Added to all DM experiments'},
    'primary-beamline-contact-email': {
        'default': 'akastengren@anl.gov',
        'type': str,
        'help': "Beamline scientist email",
        'metavar': 'FILE'},
    'secondary-beamline-contact-badge': {
        'type': int,
        'default': 56788,
        'help': 'Badge name of primary beamline contact.  Added to all DM experiments'},
    'secondary-beamline-contact-email': {
        'default': 'akastengren@anl.gov',
        'type': str,
        'help': "Beamline scientist email",
        'metavar': 'FILE'},
    'globus-message-file': {
        'default': 'message-7bm.txt',
        'type': str,
        'help': "File name of the notification e-mail message to user",
        'metavar': 'FILE'},
    'edit-user-badge': {
        'default': 0,
        'type': int,
        'help': 'Badge number of the last user manually added to the experiment'},
    'globus-server-name': {
        'type': str,
        'default': 'voyager',
        'help': "Globus server name. Supported severs are: voyager or petrel"},
    # 'globus-server-uuid': {
    #     'default': 'e133a81a-6d04-11e5-ba46-22000b92c6ec',
    #     'type': str,
    #     'help': 'Globus UUID of the endpoint for formation of a direct email link, Options are e133a81a-6d04-11e5-ba46-22000b92c6ec for petrel and 9c9cb97e-de86-11e6-9d15-22000a1e3b52 for voyager'},
    # 'globus-app-uuid': {
    #     'default': 'a9badd00-39c3-4473-b180-8bccc113ba1d', # for usr32idc/petrel
    #     'type': str,
    #     'help': "Globus app UUID, to create one see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client",
    #     'metavar': 'PATH'},
    # 'globus-server-top-dir': {
    #     'default': '/gdata/dm/7BM',
    #     'type': str,
    #     'help': 'Path from data storage root to the beamline top directory. Options are /gdata/dm/7BM or /gdata/dm/2BM'},
    } 

SECTIONS['local'] = {
    'analysis': {
        'type': str,
        'default': 'mach',
        'help': "Computer running the data analysis"},
    'analysis-user-name': {
        'type': str,
        'default': '7bmb',
        'help': "User name to access the data analysis computer"},
    'analysis-top-dir': {
        'type': str,
        'default': '/local/data/',
        'help': "raw data top directory"},
    'detector': {
        'type': str,
        'default': 'prandtl',
        'help': "Computer controlling the detector where the raw data are stored"},
    'detector-user-name': {
        'type': str,
        'default': '7bmb',
        'help': "User name to access the computer controlling the detector"},
    'detector-top-dir': {
        'type': str,
        'default': '/local/data/',
        'help': "raw data top directory"},
    }


SECTIONS['epics'] = {
    'ioc-prefix' : {
        'default' : '7bmb1:',
        'type': str,
        'help': "IOC prefix for PVs"},
    'tomoscan-prefix' : {
        'default' : 'TomoScan:',
        'type': str,
        'help': "scan prefix for PVs"},
    'experiment-year-month': {
        'default': 'ExperimentYearMonth', 
       'type': str,
        'help': "EPICS process variable containing the experiment year and month",
        'metavar': 'PATH'},
    'user-email': {
        'default': 'UserEmail', 
        'type': str,
        'help': "EPICS process variable containing the user email address",
        'metavar': 'PATH'},
    'user-last-name': {
        'default': 'UserLastName', 
        'type': str,
        'help': "EPICS process variable containing the user last name",
        'metavar': 'PATH'},
    'proposal-number': {
        'default': 'ProposalNumber',
        'type': str,
        'help': 'EPICS PV containing the proposal number',
        'metavar': 'PATH'},
    'proposal-title': {
        'default': 'ProposalTitle',
        'type': str,
        'help': 'EPICS PV containing the proposal title',
        'metavar': 'PATH'},
    }

SECTIONS['email'] = {
    'schedule': {
        'default': False,
        'help': 'Set to True to send and email to all users listed in the current proposal',
        'action': 'store_true'}}

GLOBUS_PARAMS = ('globus', 'scheduling', 'local', 'epics')

NICE_NAMES = ('General', 'Scheduling', 'Globus', 'Local', 'Epics', 'e-mail')

def get_config_name():
    """Get the command line --config option."""
    name = CONFIG_FILE_NAME
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


def config_to_list(config_name=CONFIG_FILE_NAME):
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

            if value != '' and value != 'None':
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
    log.info('Writing initial config file')
    log.info(config_file)
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

            prefix = '# ' if value == '' else ''

            if name != 'config':
                config.set(section, prefix + name, str(value))
    with open(config_file, 'w') as f:
        config.write(f)


def show_config(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    log.warning('Globus status start')
    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k.replace('_', '-') in SECTIONS[section]))
        if entries:
            for entry in entries:
                value = args[entry] if args[entry] != None else "-"
                log.info("  {:<16} {}".format(entry, value))

    log.warning('Globus status end')
