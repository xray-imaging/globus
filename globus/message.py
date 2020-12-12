import os
import pathlib
import smtplib

from email.message import EmailMessage
from dmagic import scheduling

from globus import log
from globus import dm
from globus import globus

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
                line = 'Data link: {:s}'.format(dm.make_data_link(args))
            mess_file2.write(line)

    with open(globus_message_file, 'r') as mess_file3:        
        msg = EmailMessage()
        msg.set_content(mess_file3.read())
    msg['From'] = args.primary_beamline_contact_email
    msg['Subject'] = 'Important information on APS experiment'

    return msg

def send_email(args):

    log.info("email will contain %s download data link", args.globus_server_name)
    log.info("send email to users?")
    if not yes_or_no('   *** Yes or No'):                
        log.info(' ')
        log.warning('   *** Message not not sent')
        return False

    if (args.globus_server_name == 'voyager'):
        s = smtplib.SMTP('localhost')
        for em in args.email_list:
            if args.msg['To'] is None:
                args.msg['To'] = em
            else:
                args.msg.replace_header('To',em)
            log.info('   Sending informational message to {:s}'.format(em))
            s.send_message(args.msg)
        s.quit()
    elif (args.globus_server_name == 'petrel'):
        # # see https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
        # # to create your project app_id. Once is set put it in globus.config app-id field
        ac, tc = globus.create_clients(args)
        log.info('Creating user directories on server %s:%s' % (args.globus_server_uuid, args.globus_server_top_dir))
        # try to create the directories to share on the globus server in case after the globus dm_init the pi last name was manually changed
        globus.create_globus_dir(args, ac, tc)

        new_dir = args.year_month + '/' + args.pi_last_name

        users = scheduling.get_current_users(args)
        emails = scheduling.get_current_emails(users, exclude_pi=False)
        emails.append(args.primary_beamline_contact_email)
        emails.append(args.secondary_beamline_contact_email)
        for email in emails:
            args.pi_email = email
            log.warning('Sharing %s%s with %s' % (args.globus_server_top_dir, new_dir, args.pi_email))
            globus.share_globus_dir(args, ac, tc)
    else:
        log.error("%s is not a supported globus server" % args.globus_server_name)

def yes_or_no(question):
    answer = str(input(question + " (Y/N): ")).lower().strip()
    while not(answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
        log.warning("Input yes or no")
        answer = str(input(question + "(Y/N): ")).lower().strip()
    if answer[0] == "y":
        return True
    else:
        return False
