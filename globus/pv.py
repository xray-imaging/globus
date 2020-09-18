from epics import PV


def init_general_PVs(args):

    global_PVs = {}

    global_PVs['ExperimentYearMonth'] = PV(args.experiment_year_month)
    global_PVs['UserEmail'] = PV(args.user_email)
    global_PVs['UserLastName'] = PV(args.user_last_name)

    return global_PVs

def update_experiment_info(args):

    global_PVs = init_general_PVs(args)
    year_month = global_PVs['ExperimentYearMonth'].get(as_string=True)
    pi_last_name = global_PVs['UserLastName'].get(as_string=True)
    pi_email = global_PVs['UserEmail'].get(as_string=True)
    
    return year_month, pi_last_name, pi_email


