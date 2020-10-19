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
    year_month = global_PVs['ExperimentYearMonth'].get()
    pi_last_name = global_PVs['UserLastName'].get()
    pi_email = global_PVs['UserEmail'].get()
    GUP_number = global_PVs['GUP#'].get()   
    GUP_title = global_PVs['ProposalTitle'].get()

    # convert list of chars into string and remove NULL termination
    year_month_str = string_from_pv_output(year_month)
    pi_last_name_str = string_from_pv_output(pi_last_name)
    pi_email_str = string_from_pv_output(pi_email)
    gup_number_str = string_from_pv_output(GUP_number)
    gup_title_str = string_from_pv_output(GUP_title)

    return year_month_str, pi_last_name_str, gup_number_str, gup_title_str


def string_from_pv_output(pv_output_in):
    '''Converts pv_output_in to string if necessary.
    '''
    if type(pv_output_in) == str:
        return pv_output_in
    elif type(pv_output_in) == np.ndarray:
        return "".join([chr(c) for c in pv_output_in]).rstrip('\x00')
 
