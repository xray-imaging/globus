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

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'

__all__ = ['create_clients',
           'create_dir',
           'share_globus_dir']


def make_username_list(args):
    '''Set up a DM experiment to store data on Voyager.
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


def make_user_email_list:
    pass


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
        log.warning('Experiment already exists')
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
    log.info('Adding users from the current proposal to the DM experiment.')
    for uname in username_list:
        try:
            user_api.addUserExperimentRole(uname, 'User', exp_obj['name'])
            log.info('   Added user {:s} to the DM experiment'.format(uname))
        except oee:
            log.warning('   User {:s} is already a user for the experiment'.format(uname))


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
    log.info('Add a DAQ to experiment {:s}'.format(exp_name))
    dm_dir_name = "@{0:s}:{1:s}".format(args.analysis,analysis_dir_name)
    daq_api.startDaq(exp_name, dm_dir_name)


def show_endpoints(args, ac, tc):

    log.info('Show all endpoints shared and owned by my globus user credentials')
    log.info("*** Endpoints shared with me:")
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        log.info("*** *** [{}] {}".format(ep["id"], ep["display_name"]))
    log.info("*** Endpoints owned by me:")
    for ep in tc.endpoint_search(filter_scope="my-endpoints"):
         log.info("*** *** [{}] {}".format(ep["id"], ep["display_name"]))


def create_clients(app_id):
  """
  Create authorize and transfer clients

  Parameters
  ----------
  app_id : App UUID 

  Returns
  -------
  ac : Authorize client
  tc : Transfer client
    
    """

  client = globus_sdk.NativeAppAuthClient(app_id)
  client.oauth2_start_flow(refresh_tokens=True)

  log.warning('Please go to this URL and login: {0}'.format(client.oauth2_get_authorize_url()))

  get_input = getattr(__builtins__, 'raw_input', input)
  auth_code = get_input('Please enter the code you get after login here: ').strip() # pythn 3
  # auth_code = raw_input('Please enter the code you get after login here: ').strip() # python 2.7
  
  token_response = client.oauth2_exchange_code_for_tokens(auth_code)

  # let's get stuff for the Globus Transfer service
  globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
  # the refresh token and access token, often abbr. as RT and AT
  transfer_rt = globus_transfer_data['refresh_token']
  transfer_at = globus_transfer_data['access_token']
  expires_at_s = globus_transfer_data['expires_at_seconds']

  # Now we've got the data we need, but what do we do?
  # That "GlobusAuthorizer" from before is about to come to the rescue
  authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)
  # and try using `tc` to make TransferClient calls. Everything should just
  # work -- for days and days, months and months, even years
  ac = globus_sdk.AuthClient(authorizer=authorizer)
  tc = globus_sdk.TransferClient(authorizer=authorizer)

  return ac, tc


def create_globus_dir(args,
                    ac,              # Authorize client  
                    tc):             # Transfer client

    date_dir_path = args.globus_server_top_dir + args.year_month + '/'
    pi_last_name_dir_path = args.globus_server_top_dir + args.year_month + '/' + args.pi_last_name + '/'

    try:
      response = tc.operation_mkdir(args.globus_server_uuid, path=date_dir_path)
      log.info('*** Created folder: %s' % date_dir_path)
    except:
      log.warning('*** Path %s already exists' % (date_dir_path))

    try:
      response = tc.operation_mkdir(args.globus_server_uuid, path=pi_last_name_dir_path)
      log.info('*** Created folder: %s' % pi_last_name_dir_path)
      return True
    except:
      log.warning('*** Path %s already exists' % (pi_last_name_dir_path))
      return False


def create_dir(directory,       # Subdirectory name under top to be created
               args,
               ac,              # Authorize client  
               tc):             # Transfer client

    new_dir_path = args.globus_server_top_dir + directory + '/'

    try:
      response = tc.operation_mkdir(args.globus_server_uuid, path=new_dir_path)
      log.info('*** Created folder: %s' % new_dir_path)
      return True
    except:
      log.warning('*** Path %s already exists' % new_dir_path)
      return False


def share_globus_dir(args,
              ac,             # Authorize client  
              tc):            # Transfer client

    # Query to Auth Client to verify if a globus user ID is associated to the user email address, if not one is generated
    response = ac.get("/v2/api/identities?usernames="+args.pi_email)

    # Get user id from user email
    r = ac.get_identities(usernames=args.pi_email)
    user_id = r['identities'][0]['id']
    # log.info(r, user_id)

    directory_full_path = args.globus_server_top_dir + args.year_month + '/' + args.pi_last_name + '/'
    # Set access control and notify user
    rule_data = {
      'DATA_TYPE': 'access',
      'principal_type': 'identity',
      'principal': user_id,
      'path': directory_full_path,
      'permissions': 'r',
      'notify_email': args.pi_email,
      'notify_message': args.globus_message
    }

    try: 
      response = tc.add_endpoint_acl_rule(args.globus_server_uuid, rule_data)
      log.info('*** Path %s has been shared with %s' % (directory_full_path, args.pi_email))
      return True
    except:
      log.warning('*** Path %s is already shared with %s' % (directory_full_path, args.pi_email))
      return False


