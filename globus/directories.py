'''
Helper functions to check and create directories on remote machines.
    
'''
from pathlib import Path
import os
import subprocess
from paramiko import SSHClient

from globus import pv
from globus import log


def make_directory_name(args):
    '''Make a name based on year-month-piLastName-GUP#
    Return: str with the name
    '''
    year_month, pi_lastname, gup_number, gup_title = pv.update_experiment_info(args)
    return '{0:s}-{1:s}-{2:s}'.format(year_month, pi_lastname, gup_number)


def create_analysis_dir_name(args):
    exp_name = make_directory_name(args)
    year_month, pi_lastname, prop_number, prop_title = pv.update_experiment_info(args)
    analysis_path = Path(args.analysis_top_dir).joinpath(year_month,exp_name)
    log.info('Directory on analysis machine: {:s}'.format(str(analysis_path)))
    return str(analysis_path)


def create_detector_dir_name(args):
    exp_name = make_directory_name(args)
    year_month, pi_lastname, prop_number, prop_title = pv.update_experiment_info(args)
    detector_path = Path(args.detector_top_dir).joinpath(year_month,exp_name)
    log.info('Directory on analysis machine: {:s}'.format(str(detector_path)))
    return str(detector_path)


def check_remote_directory(remote_server, remote_dir):
    try:
        rcmd = 'ls ' + remote_dir
        # rcmd is the command used to check if the remote directory exists
        subprocess.check_call(['ssh', remote_server, rcmd], stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'))
        log.warning('      *** remote directory %s exists' % (remote_dir))
        return 0

    except subprocess.CalledProcessError as e: 
        # log.info('      *** return code = %d' % (e.returncode))
        log.warning('      *** remote directory %s does not exist' % (remote_dir))
        if e.returncode == 2:
            return e.returncode
        else:
            log.error('  *** Unknown error code returned: %d' % (e.returncode))
            return -1


def create_remote_directory(remote_server, remote_dir):
    '''Command to create directories on the remote machine.
    This will create all necessary parent directories.
    This was originally called with 'mkdir -p', but this will not
    set the created parent directories to the right permissions.
    '''
    cmd = 'mkdir -m 777 ' + remote_dir
    try:
        # log.info('      *** sending command %s' % (cmd))
        log.info('      *** creating remote directory %s' % (remote_dir))
        subprocess.check_call(['ssh', remote_server, cmd])
        log.info('      *** creating remote directory %s: Done!' % (remote_dir))
        return 0

    except subprocess.CalledProcessError as e:
        log.error('  *** Error while creating remote directory. Error code: %d' % (e.returncode))
        return -1


def mkdir(remote_server, remote_dir):
    '''Command to create directories on the remote machine.
    This will create all necessary parent directories.
    This was originally called with 'mkdir -p', but this will not
    set the created parent directories to the right permissions.
    '''
    log.info('Creating directory on server %s:%s' % (remote_server, remote_dir))
    path_parts = Path(remote_dir).parts
    parent_path = Path(path_parts[0])
    for p in path_parts[1:]:
        parent_path = parent_path.joinpath(p)
        ret = check_remote_directory(remote_server , str(parent_path))
        if ret == 2:
            iret = create_remote_directory(remote_server, str(parent_path))
