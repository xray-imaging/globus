import log_lib
import globus_sdk

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2019, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'

__all__ = ['create_clients',
           'create_dir',
           'share_dir']

def show_endpoints(params):
    # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
    # to create your project app_id
    # app_id = "8235a963-59a6-4354-9724-d330025b199d"
    app_id = params.app_id

    ac, tc = create_clients(app_id)

    log_lib.info("Endpoints shared with me:")
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        # Logger("log").info("[{}] {}".format(ep["id"], ep["display_name"]))
        # LOG.info("[{}] {}".format(ep["id"], ep["display_name"]))
        # # LOG.info(ep["id"], ep["display_name"])
        # LOG.info(ep["id"] + ep["display_name"])
        log_lib.info("[{}] {}".format(ep["id"], ep["display_name"]))
    log_lib.info("My Endpoints:")
    for ep in tc.endpoint_search(filter_scope="my-endpoints"):
        # Logger("log").info("[{}] {}".format(ep["id"], ep["display_name"]))
        log_lib.info("[{}] {}".format(ep["id"], ep["display_name"]))


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

  log_lib.warning('Please go to this URL and login: {0}'.format(client.oauth2_get_authorize_url()))

  get_input = getattr(__builtins__, 'raw_input', input)
  # auth_code = get_input('Please enter the code you get after login here: ').strip() # pythn 3
  auth_code = raw_input('Please enter the code you get after login here: ').strip() # python 2.7
  
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

def create_dir(new_share,     # Subdirectory name under top to be created and shared with user
               endpoint_id,   # Endpoint id on which to create shared folder
               endpoint_top,  # Endpoint top directory
               ac,            # Authorize client  
               tc):           # Transfer client

    # Create directory to be shared
    share_path = endpoint_top + new_share + '/'
    tc.operation_mkdir(endpoint_id, path=share_path)
    return share_path

def share_dir(share_path,     # Endpoint path to shared folder
              email,          # User email address for notification
              endpoint_id,    # Endpoint id on which to create shared folder
              ac,             # Authorize client  
              tc):            # Transfer client

    # Generate user id from user email
    r = ac.get_identities(usernames=email)
    user_id = r['identities'][0]['id']
    # log_lib.info(r, user_id)

    # Set access control and notify user
    rule_data = {
      'DATA_TYPE': 'access',
      'principal_type': 'identity',
      'principal': user_id,
      'path': share_path,
      'permissions': 'r',
      'notify_email': email,
      'notify_message': 
          'The data that you requested from RDP is available.'
    }
    tc.add_endpoint_acl_rule(endpoint_id, rule_data)

