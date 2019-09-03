#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging
import time
import re
from datetime import datetime
from epics import PV

import config
import globus_lib
import log_lib



__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'


global_PVs = {}


def init_general_PVs(global_PVs):

    global_PVs['ExperimentYearMonth'] = PV('2bmS1:ExpInfo:ExperimentYearMonth')
    global_PVs['UserEmail'] = PV('2bmS1:ExpInfo:UserEmail')
    global_PVs['UserLastName'] = PV('2bmS1:ExpInfo:UserLastName')


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

    # year_month = args.year_month
    # pi_last_name = args.pi_last_name
    # pi_email = args.pi_email
    init_general_PVs(global_PVs)
    year_month = global_PVs['ExperimentYearMonth'].get()
    pi_last_name = global_PVs['UserLastName'].get()
    pi_email = global_PVs['UserEmail'].get()
    
    args.year_month = "".join([chr(c) for c in year_month]).rstrip('\x00')
    args.pi_last_name = "".join([chr(c) for c in pi_last_name]).rstrip('\x00')
    args.pi_email = "".join([chr(c) for c in pi_email]).rstrip('\x00')

    # message = args.globus_message
    # with open (args.globus_message_file, "r") as myfile:
    #     args.globus_message=myfile.read()
    # print(args.globus_message)  

    log_lib.info('Creating user directories on server %s:%s' % (args.globus_server_uuid, args.globus_server_top_dir))


    log_lib.info('************ %s' % args.year_month)

    globus_lib.create_dir(args.year_month, args, ac, tc)

    new_dir = args.year_month + '/' + args.pi_last_name
    globus_lib.create_dir(new_dir, args, ac, tc)


    new_dir = args.year_month + '/' + args.pi_last_name
    log_lib.info('Sharing %s%s with %s' % (args.globus_server_top_dir, new_dir, args.pi_email))
    globus_lib.share_dir(new_dir, args, ac, tc)


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
        # load args from default (config.py) if not changed
        config.log_values(args)
        args._func(args)
        # undate globus.config file
        sections = config.GLOBUS_PARAMS
        config.write(args.config, args=args, sections=sections)
    except RuntimeError as e:
        log_lib.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

