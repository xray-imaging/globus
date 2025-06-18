======
GLOBUS
======


`globus <https://github.com/xray-imaging/globus>`_ is a Python script that interfaced with the APS Data Management System (e.g. Voyager) and a generic `Globus server <https://www.globus.org/>`_ (e.g. Petrel).  It reads beamline PVs to set up a Data Management experiment, create directories on the data acquisition and analysis machines, manage users for the experiment, send e-mails to users with information on how to get their data from Voyager or Petrel, and manage automated data transfer (termed DAQs) from the analysis machine to Voyager.
The notification email can be sent to all users listed in the beamline schedule by using the --schedule option.

year-month, pi_last_name and pi_email are read from the EPIC PVs defined in the 'epics' section of the `globus config file <https://github.com/xray-imaging/globus/blob/master/globus/config.py>`_. By default these PVs are served by `TomoScan <https://tomoscan.readthedocs.io/en/latest/tomoScanApp.html#user-information>`_  and can be automatically updated for the current user using `dmagic tag <https://dmagic.readthedocs.io/en/latest/source/usage.html>`_.


Dependencies
------------

`globus` dependencies are listed in the envs/requirements.txt file. 


Installation
------------

Install from `Anaconda <https://www.anaconda.com/distribution/>`_ python3.x, then install globus::

    $ git clone https://github.com/xray-imaging/globus.git
    $ cd globus
    $ pip install .


Environment configuration
-------------------------

There are also several environment variables that must be set for the DM API to work properly.  They can be found in the /home/dm_bm/etc/dm.conda.setup.sh script.  Copy everything in this script to your account's ~/.bashrc file.


Configuration
-------------

- customize the email to the user by editing the `message <https://github.com/xray-imaging/globus/blob/master/globus/message.txt>`_
- for automatic retrieval of user information from the APS scheduling system see `dmagic tag <https://dmagic.readthedocs.io/en/latest/source/usage.html>`_. 


Usage
-----

Once the DMagic medm screen is synchronized with the APS scheduling system and contains valid values like:

.. image:: medm_screen.png
  :width: 400
  :alt: medm screen

you can run globus as follows::

    $ source /home/dm_bm/etc/dm.setup.sh

then:

    globus -h for help
        
    globus set
        Creates a globus.conf default file

    globus init 
        Initialize data mamagement. 
        If using a DM server:
            Create an experiment in the DM system
            Add users to this experiment
        if using a Globus server: 
            Create or refresh a globus access token
            Create directory on the globus server 
    globus dirs
        Checks for directories on the analysis and detector computers and creates them, as needed

    globus email
        E-mails all users on an experiment with information on how to access their data

    globus start_daq
        Starts automated file upload from the analysis computer to a DM server
    
    globus stop_daq
        Stops automated file uploads for this experiment to a DM server

    globus add_user --edit-user-badge 123456
        Adds the user with the badge 123456 to a DM experiment

    globus list_users
        Lists the users (name and badge numbers) that are part of the DM experiment

    globus remove_user --edit-user-badge 123456
        Removes the user with badge 123456 from the DM experiment

        data collection and data analysis machines need to be configured in the local section of the `config <https://github.com/xray-imaging/globus/blob/master/globus/config.py>`_ file. The directory creation requires ssh access to the data collection and data analysis machines, if prefered not to use a password see `SSH login without password <http://www.linuxproblem.org/art_9.html>`_.
        
        
Typical Workflow
----------------

For DM server::

    $ globus init
    $ globus dirs
    $ globus list_users
    $ globus add_user --edit-user-badge 123456
    $ globus remove_user --edit-user-badge 987654 
    $ globus email 

For Globus server::

    $ globus init
    $ globus dirs
    $ globus email 
