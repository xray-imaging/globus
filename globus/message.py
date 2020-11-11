import os
import pathlib
from email.message import EmailMessage
from globus import voyager_setup

def message_file_name(args):
    return os.path.join(pathlib.Path(__file__).parent, args.globus_message_file)

def message(args):
    #Add in the actual data link to the message
    globus_message_file = message_file_name(args)
    with open(globus_message_file, 'r') as mess_file:
        temp_mess_file = mess_file.readlines()
    with open(globus_message_file, 'w') as mess_file2:
        for line in temp_mess_file:
            if line.startswith('Data link:'):
                line = 'Data link: {:s}'.format(voyager_setup.make_data_link(args))
            mess_file2.write(line)

    with open(globus_message_file, 'r') as mess_file3:        
        msg = EmailMessage()
        msg.set_content(mess_file3.read())
    msg['From'] = args.primary_beamline_contact_email
    msg['Subject'] = 'Important information on APS experiment'

    return msg