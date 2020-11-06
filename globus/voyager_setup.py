import datetime

import dm
from globus import log
from globus import pv
from globus import directories
import dmagic

exp_api = dm.ExperimentDsApi()
bss_api = dm.BssApsDbApi()
user_api = dm.UserDsApi()
daq_api = dm.ExperimentDaqApi()
oee = dm.common.exceptions.objectAlreadyExists.ObjectAlreadyExists

__author__ = "Alan L Kastengren"
__copyright__ = "Copyright (c) 2020, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'


def make_proposal_username_list(args):
    '''Make a list of DM usernames for the current proposal.
    '''
    log.info('Making a list of DM system usernames from target proposal')
    year_month, pi_lastname, prop_number, prop_title = pv.update_experiment_info(args)
    target_prop = bss_api.getProposal(str(prop_number))
    users = target_prop['experimenters']
    log.info('   Adding the primary beamline contact')
    user_ids = {'d' + str(args.primary_beamline_contact_badge)}
    for u in users:
        log.info('   Adding user {0}, {1}, badge #{2}'.format(
                    u['lastName'], u['firstName'], u['badge']))
        user_ids.add('d' + str(u['badge']))
    return user_ids


def make_exp_username_list(args):
    '''Make a list of the usernames from the current DM experiment.
    '''
    log.info('Making a list of DM system usernames from current DM experiment')
    exp_name = directories.make_directory_name(args)
    try:
        exp_obj = exp_api.getExperimentByName(exp_name)
        return exp_obj['experimentUsernameList']
    except:
        log.error('No such experiment in the DM system: {:s}'.format(exp_name))
        log.error('   Have you run globus user_init yet?')
        return []


def make_user_email_list(username_list):
    '''Make a list of e-mail addresses for a list of DM usernames.
    Input
    list of DM usernames, each of which is in the form 'd12345'
    Returns:
    list of e-mail addresses.
    '''
    email_list = []
    for u in username_list:
        try:
            user_obj = user_api.getUserByUsername(u)
            email_list.append(user_obj['email'])
            log.info('   Added email {:s} for user {:s}'.format(email_list[-1], u))
        except:
            log.warning('   Problem loading email for user {:s}'.format(u))
    return email_list
        

def create_dm_experiment(args):
    '''Creates a new experiment on Voyager using Data Management.
    Uses the GUP title as the description.
    Name is in the form year-month-PILastName-GUP#
    Returns:
    Experiment object
    '''
    year_month, pi_lastname, prop_number, prop_title = pv.update_experiment_info(args)
    dir_name = directories.make_directory_name(args)
    log.info('See if there is already a DM experiment')
    try:
        old_exp = exp_api.getExperimentByName(dir_name)
        log.warning('   Experiment already exists')
        return old_exp 
    except:
        log.info('Creating new DM experiment: {0:s}/{1:s}'.format(year_month, dir_name))
    target_prop = bss_api.getProposal(str(prop_number))
    start_datetime = datetime.datetime.strptime(
                        target_prop['startTime'],
                        '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.datetime.strptime(
                        target_prop['endTime'],
                        '%Y-%m-%d %H:%M:%S')
    new_exp = exp_api.addExperiment(dir_name, typeName = args.experiment_type,
                        description = prop_title, rootPath = year_month,
                        startDate = start_datetime.strftime('%d-%b-%y'),
                        endDate = end_datetime.strftime('%d-%b-%y'))
    log.info('   Experiment successfully created!')
    return new_exp


def experiment_add_users(exp_obj, username_list):
    '''Add a list of users to a DM experiment
    '''
    existing_unames = exp_obj['experimentUsernameList']
    for uname in username_list:
        user_obj = user_api.getUserByUsername(uname)
        if uname in existing_unames:
            log.warning('   User {:s} is already a user for the experiment'.format(
                        make_pretty_user_name(user_obj)))
            continue
        user_api.addUserExperimentRole(uname, 'User', exp_obj['name'])
        log.info('   Added user {0:s} to the DM experiment'.format(
                    make_pretty_user_name(user_obj)))


def start_dm_daq(args):
    '''Starts a DAQ process on the current experiment.
    '''
    exp_name = directories.make_directory_name(args)
    analysis_dir_name = directories.create_analysis_dir_name(args)
    log.info('Check that the directory exists on the analysis machine')
    dir_check = directories.check_remote_directory(args.analysis, analysis_dir_name) 
    if dir_check == 2:
        log.info('   Need to make the analysis machine directory')
        mkdir_response = directories.create_remote_directory(
                            args.analysis, analysis_dir_name)
        if mkdir_response:
            log.error('   Unknown response when creating analysis machine directory.  Exiting')
            return
    elif dir_check == 0:
        log.info('   Directory already exists')
    else:
        log.warning('   Unknown response when checking for analysis machine directory.  Exiting')
        return    
    dm_dir_name = "@{0:s}:{1:s}".format(args.analysis,analysis_dir_name)
    log.info('Check to make sure the appropriate DAQ is not already running.')
    current_daqs = daq_api.listDaqs()
    for d in current_daqs:
        if (d['experimentName'] == exp_name and d['status'] == 'running'
            and d['dataDirectory'] == dm_dir_name):
            log.warning('   DAQ is already running.  Returning.')
            return
    log.info('Add a DAQ to experiment {:s}'.format(exp_name))
    daq_obj = daq_api.startDaq(exp_name, dm_dir_name)


def stop_dm_daq(args):
    '''Stops the currently running DM DAQ. 
    '''
    exp_name = directories.make_directory_name(args)
    log.info('Stopping all DM DAQs for experiment {:s}'.format(exp_name))
    daqs = daq_api.listDaqs()
    removed_daq_counter = 0
    for d in daqs:
        if d['experimentName'] == exp_name and d['status'] == 'running':
            log.info('   Found running DAQ for this experiment.  Stopping now.')
            daq_api.stopDaq(d['experimentName'],d['dataDirectory'])
            removed_daq_counter += 1
    if removed_daq_counter == 0:
        log.info('   No active DAQs for this experiment were found')


def add_user(args):
    exp_name = directories.make_directory_name(args)
    try:
        exp_obj = exp_api.getExperimentByName(exp_name)
    except:
        log.error('   No appropriate experiment found.')
        return
    try:
        experiment_add_users(exp_obj, ['d{:d}'.format(args.edit_user_badge)])
    except:
        log.error('   Problem adding the user.  Check the badge number')
    

def remove_user(args):
    '''Remvoe a user from the DM experiment.
    '''
    exp_name = directories.make_directory_name(args)
    dm_username = 'd{:d}'.format(args.edit_user_badge)
    try:
        user_to_remove = user_api.getUserByUsername(dm_username)
    except:
        log.error('   Problem retrieving user information.  Check the badge number')
        return
    log.info('Removing user {0:s} from experiment {1:s}'.format(
                make_pretty_user_name(user_to_remove), exp_name))
    try:
        exp_obj = exp_api.getExperimentByName(exp_name)
    except:
        log.error('    No appropriate experiment found.')
        return
    try:
        user_api.deleteUserExperimentRole(dm_username, 'User', exp_name)
    except:
        log.error('   Problem removing the user.  Check the badge number')


def list_users(args):
    '''Lists the users on the current experiment in a nice format.
    '''
    log.info('Listing the users on the DM experiment')
    exp_name = directories.make_directory_name(args)
    try:
        exp_obj = exp_api.getExperimentByName(exp_name)
    except:
        log.error('   No appropriate experiment found.')
        return
    username_list = exp_obj['experimentUsernameList']
    if len(username_list) == 0:
        log.info('   No users for this experiment')
        return
    for uname in username_list:
        user_obj = user_api.getUserByUsername(uname)
        log.info('   User {0:s}, badge {1:s} is on the DM experiment'.format(
                    make_pretty_user_name(user_obj), user_obj['badge']))


def make_pretty_user_name(user_obj):
    '''Makes a printable name from the DM user object
    '''
    output_string = ''
    if 'firstName' in user_obj:
        output_string += user_obj['firstName'] + ' '
    if 'middleName' in user_obj:
        output_string += user_obj['middleName'] + ' '
    if 'lastName' in user_obj:
        output_string += user_obj['lastName']
    return output_string


def make_email_link(args):
    '''Makes the link to give to users so they can access their data directly.
    '''
    exp_name = directories.make_directory_name(args)
    target_exp = exp_api.getExperimentByName(exp_name)
    year_month, pi_lastname, prop_number, prop_title = pv.update_experiment_info(args)
    output_link = 'https://app.globus.org/file-manager?origin_id='
    output_link += args.globus_endpoint_id
    output_link += '&origin_path='
    target_dir = args.globus_beamline_root + '/' + year_month + '/' + exp_name + '/\n'
    output_link += target_dir.replace('/','%2F') 
    return output_link