#!/Users/decarlo/conda/anaconda3/bin/python
import os
import sys
import argparse
import logging
import time
import re
from datetime import datetime

import config
import globus_lib
import log_lib



__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'


def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def show(args):
    log_lib.info('Show all endpoints owned and shared by your globus user credentials')
    globus_lib.show_endpoints(args)


def mkdir(args):

    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id
    print(args.app_id)
    app_id = args.app_id
    server_id = args.globus_server_uuid
    server_top_dir = args.globus_server_top_dir
    message = args.globus_message

    year_month = args.year_month
    pi_last_name = args.pi_last_name
    pi_email = args.pi_email

    ac, tc = globus_lib.create_clients(app_id)

    log_lib.info("Endpoints shared with me:")
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        log_lib.info("[{}] {}".format(ep["id"], ep["display_name"]))

    log_lib.info('On server %s top directory %s' % (server_id, server_top_dir))
    shared_path = globus_lib.create_dir(year_month, server_id, server_top_dir, ac, tc)
    log_lib.info('Created folder: %s' % shared_path)
    shared_path = globus_lib.create_dir(pi_last_name, server_id, server_top_dir + year_month + '/', ac, tc)
    log_lib.info('Created folder: %s' % shared_path)
    globus_lib.share_dir(shared_path, pi_email, server_id, message, ac, tc)
    log_lib.info('Sent email to %s' % pi_email)

    return 0

def create(args):
    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id
    # app_id = "8235a963-59a6-4354-9724-d330025b199d"
    app_id = "a9badd00-39c3-4473-b180-8bccc113ba1d" # for usr32idc

    ac, tc = globus_lib.create_clients(app_id)


    log_lib.info("Endpoints shared with me:")
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        log_lib.info("[{}] {}".format(ep["id"], ep["display_name"]))

    # print output for the endpoint shared with me:
    # [ad484910-0842-11e7-bb15-22000b9a448b] aps_32id
    # [26a93324-0847-11e7-bb15-22000b9a448b] nersc_aps_32id
    # [e133a81a-6d04-11e5-ba46-22000b92c6ec] petrel tomography

    # picked petrel
    globus_server_id = u'e133a81a-6d04-11e5-ba46-22000b92c6ec'

    shared_path = globus_lib.create_dir('2020-12', globus_server_id, '/2-BM/', ac, tc)
    shared_path = globus_lib.create_dir('pi_last_name', globus_server_id, '/2-BM/2020-12/', ac, tc)
    globus_lib.share_dir(shared_path, 'decarlof@gmail.com', globus_server_id, ac, tc)


def main():
    # create logger
    # # python 3.5+ 
    # home = str(pathlib.Path.home())
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'

    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = logs_home + 'globus_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log_lib.setup_logger(lfname)


    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])
    show_params = config.GLOBUS_PARAMS
    mkdir_params = config.GLOBUS_PARAMS

    cmd_parsers = [
        ('init',        init,           (),                             "Create configuration file"),
        ('show',        show,           show_params,                    "Show endpoints"),
        ('mkdir',       mkdir,          mkdir_params,                   "Create folder on endpoint"),

    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)

    try:
        config.log_values(args)
        # log_lib.info(args)
        args._func(args)
    except RuntimeError as e:
        log_lib.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

