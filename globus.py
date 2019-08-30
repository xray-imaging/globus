#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id. Once is set put it in globus.config app-id field
    app_id = args.app_id
    ac, tc = globus_lib.create_clients(app_id)
    globus_lib.show_endpoints(args, ac, tc)


def mkdir(args):

    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id. Once is set put it in globus.config app-id field
    app_id = args.app_id
    ac, tc = globus_lib.create_clients(app_id)
    globus_lib.show_endpoints(args, ac, tc)

    server_id = args.globus_server_uuid
    server_top_dir = args.globus_server_top_dir
    message = args.globus_message

    year_month = args.year_month
    pi_last_name = args.pi_last_name
    pi_email = args.pi_email

    log_lib.info('On server %s top directory %s' % (args.globus_server_uuid, args.globus_server_top_dir))
    new_dir_path = globus_lib.create_dir(year_month, server_id, server_top_dir, ac, tc)
    # if new_dir_path is not None:
    #     log_lib.info('*** Created folder: %s' % new_dir_path)
    new_dir_path = globus_lib.create_dir(pi_last_name, server_id, server_top_dir + year_month + '/', ac, tc)
    # if new_dir_path is not None:
    #     log_lib.info('*** Created folder: %s' % new_dir_path)

    # ret = globus_lib.share_dir(new_dir_path, pi_email, server_id, message, ac, tc)
    # if ret is not None:
    #     log_lib.info('*** Sent email to %s' % pi_email)


def main():
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
        args._func(args)
    except RuntimeError as e:
        log_lib.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

