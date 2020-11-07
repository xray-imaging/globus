from epics import PV
from globus import log
import numpy as np


def init_general_PVs(args):

    global_PVs = {}
    prefix = args.pv_prefix
    scan_prefix = args.scan_prefix
    global_PVs['ExperimentYearMonth'] = PV(prefix + scan_prefix + args.experiment_year_month)
    global_PVs['UserEmail'] = PV(prefix + scan_prefix + args.user_email)
    global_PVs['UserLastName'] = PV(prefix + scan_prefix + args.user_last_name)
    global_PVs['GUP#'] = PV(prefix + scan_prefix + args.GUP_number)
    global_PVs['ProposalTitle'] = PV(prefix + scan_prefix + args.GUP_desc)

    return global_PVs

def update_experiment_info(args):
    '''Retrieve the information for the current experiment from the beamline PVs.
    Returns:
    Year and month of the current experiment as a string in the format %Y-%m
    Last name of the PI as a string
    Proposal number as a string
    '''
    global_PVs = init_general_PVs(args)

    year_month = global_PVs['ExperimentYearMonth'].get(as_string=True)
    pi_last_name = global_PVs['UserLastName'].get(as_string=True)
    pi_email = global_PVs['UserEmail'].get(as_string=True)
    gup_number = global_PVs['GUP#'].get(as_string=True)   
    gup_title = global_PVs['ProposalTitle'].get(as_string=True)

    return year_month, pi_last_name, gup_number, gup_title
 
