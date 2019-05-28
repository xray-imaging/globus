#!/Users/decarlo/conda/anaconda3/bin/python
import os
import sys
import argparse
import logging
import time
import re

import globus_lib
import config


__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'

LOG = logging.getLogger('globus')

def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def show(args):
    LOG.info('Show all endpoints owned and shared by your globus user credentials')
    globus_lib.show_endpoints(args)


def mkdir(args):
    # from xfluo import mkdiro
    # mkdiro.tomo(args)
    return 0

def space_holder():
    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id
    app_id = "8235a963-59a6-4354-9724-d330025b199d"

    ac, tc = globus_lib.create_clients(app_id)

    print("Endpoints shared with me:")
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        print("[{}] {}".format(ep["id"], ep["display_name"]))

    # print output for the endpoint shared with me:
    # [ad484910-0842-11e7-bb15-22000b9a448b] aps_32id
    # [26a93324-0847-11e7-bb15-22000b9a448b] nersc_aps_32id
    # [e133a81a-6d04-11e5-ba46-22000b92c6ec] petrel tomography

    # picked petrel
    globus_server_id = u'e133a81a-6d04-11e5-ba46-22000b92c6ec'

    shared_path = globus_lib.create_dir('2020-12', globus_server_id, '/2-BM/', ac, tc)
    globus_lib.share_dir(shared_path, 'decarlof@gmail.com', globus_server_id, ac, tc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])
    show_params = config.GLOBUS_PARAMS

    cmd_parsers = [
        ('init',        init,           (),                             "Create configuration file"),
        ('show',        show,           show_params,                    "Show endpointS"),
    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    LOG.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    LOG.addHandler(stream_handler)
    if args.log:
        file_handler = logging.FileHandler(args.log)
        file_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s: %(message)s'))
        LOG.addHandler(file_handler)

    try:
        config.log_values(args)
        args._func(args)
    except RuntimeError as e:
        LOG.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

