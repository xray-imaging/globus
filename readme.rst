======
GLOBUS
======


`globus <https://github.com/aps-7bm/globus/tree/voyager>`_ is a Python script that interfaced with the APS Data Management System.  It reads beamline PVs to set up a Data Management experiment, create directories on the data acquisition and analysis machines, manage users for the experiment, send e-mails to users with information on how to get their data from Voyager, and manage automated data transfer (termed DAQs) from the analysis machine to Voyager.
The notification email can be sent to all users listed in the beamline schedule by using the --schedule option.

year-month, pi_last_name and pi_email area automatically retrieved from the APS scheduling system for the current user (see `DTagging <https://github.com/xray-imaging/DTagging>`_ for more information on how to create and update epics process variables containing user and experiment information using the APS scheduling system).


Installation
------------

Install the following::

    $ git clone https://github.com/aps-7bm/globus.git
    $ cd globus 
    $ git checkout voyager
    $ python setup.py install


Configuration
-------------

- customize the email to the user by editing the `message <https://github.com/xray-imaging/globus/blob/master/message.txt>`_
- for automatic retrieval of user information from the APS scheduling system see `DMagic <https://github.com/aps-7bm/DMagic/tree/dm>`_. Alternatively you can set year-month, pi_last_name and pi_email as epics PV by configuring the epics section of the `config <https://github.com/xray-imaging/globus/blob/master/config.py>`_ file


Usage
-----

Once the DMagic medm screen is synchronized with the APS scheduling system and contains valid values like:

.. image:: medm_screen.png
  :width: 400
  :alt: medm screen

you can run globus as follows:

globus -h for help
        
    globus init
        Creates a globus.conf default file

    globus user_init 
        Reads the PV data, creates a DM experiment, and adds users from the proposal to the experiment 

    globus dirs
    globus email
        Using the current user information from the scheduling system:

        - create a directory named "year-month/pi_last_name" on the endpoint
        - share the directory with globus with the user
        - send a notification to the user with the URL to the shared folder and a user customizable `message <https://github.com/xray-imaging/globus/blob/master/globus/message.txt>`_

    globus dirs
        Using the current user information from the scheduling system:

        - create a directory named "year-month/pi_last_name" on the data collection computer
        - create a directory named "year-month/pi_last_name" on the data analysis computer

        data collection and data analysis machines need to be configured in the local section of the `config <https://github.com/xray-imaging/globus/blob/master/config.py>`_ file. The directory creation requires ssh access to the data collection and data analysis machines, if prefered not to use a password see `SSH login without password <http://www.linuxproblem.org/art_9.html>`_.
        
        
Examples
--------

::

    $ globus dirs
    $ globus email --schedule

Note: globus email will send the email notification with the globus share only to the PI as listed in the medm screen (using the PV value), with the additional --schedule option the notification is sent to all users listed in the proposal.
