from epics import PV


def init_general_PVs(args):

    global_PVs = {}

    global_PVs['ExperimentYearMonth'] = PV(args.experiment_year_month)
    global_PVs['UserEmail'] = PV(args.user_email)
    global_PVs['UserLastName'] = PV(args.user_last_name)

    return global_PVs

def update_experiment_info(args):

    global_PVs = init_general_PVs(args)
    year_month = global_PVs['ExperimentYearMonth'].get()
    pi_last_name = global_PVs['UserLastName'].get()
    pi_email = global_PVs['UserEmail'].get()
    
    # convert list of chars into string and remove NULL termination
    year_month_str = "".join([chr(c) for c in year_month]).rstrip('\x00')
    pi_last_name_str = "".join([chr(c) for c in pi_last_name]).rstrip('\x00')
    pi_email_str = "".join([chr(c) for c in pi_email]).rstrip('\x00')

    return year_month_str, pi_last_name_str, pi_email_str


