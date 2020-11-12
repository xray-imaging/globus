import os
import pathlib
import smtplib

from email.message import EmailMessage

from globus import log
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

def send_email(msg, email_list):
    if not yes_or_no('   *** Yes or No'):                
        log.info(' ')
        log.warning('   *** Message not not sent')
        return False

    s = smtplib.SMTP('localhost')
    for em in email_list:
        if msg['To'] is None:
            msg['To'] = em
        else:
            msg.replace_header('To',em)
        log.info('   Sending informational message to {:s}'.format(em))
        s.send_message(msg)
    s.quit()

def yes_or_no(question):
    answer = str(input(question + " (Y/N): ")).lower().strip()
    while not(answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
        log.warning("Input yes or no")
        answer = str(input(question + "(Y/N): ")).lower().strip()
    if answer[0] == "y":
        return True
    else:
        return False
