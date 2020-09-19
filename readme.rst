======
GLOBUS
======


`globus <https://github.com/xray-imaging/globus>`_ is a python script that automatically creates a directory on a globus server as "year-month/pi_last_name" (or any other preset path) and sends a customizable notification email to the "pi_email" that includes the URL to the shared folder.
The notification email can be sent to all users listed in the beamline schedule by using the --schedule option.

year-month, pi_last_name and pi_email are read from the EPIC PVs defined in the 'epics' section of the `globus config file <https://github.com/xray-imaging/globus/blob/master/globus/config.py>`_. By default these PVs are served by `TomoScan <https://tomoscan.readthedocs.io/en/latest/tomoScanApp.html#user-information>`_  and can be automatically updated for the current user using `dmagic tag <https://dmagic.readthedocs.io/en/latest/source/usage.html>`_.


Tasks
-----
- Authenticate with Globus
- Create a folder on a Globus server
- Share the Globus server folder with a user
- Send to the user an email with the URL to the shared folder
- Using the --schedule options share and email is sent to all users listed in current beamline schedule

Installation
------------

Install the following::

    $ pip install globus-sdk 
    $ pip install paramiko
    $ git clone https://github.com/xray-imaging/globus.git
    $ cd globus 
    $ python setup.py install


Configuration
-------------

- see step 1 in the `Globus tutorial <https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client>`_ to register your app with Globus and get your project app_id
- set your project app-id and personal-endpoint-uuid as default in the `config.py <https://github.com/xray-imaging/globus/blob/master/config.py>`_ file
- customize the email to the user by editing the `message <https://github.com/xray-imaging/globus/blob/master/message.txt>`_
- for automatic retrieval of user information from the APS scheduling system see `dmagic tag <https://dmagic.readthedocs.io/en/latest/source/usage.html>`_. Alternatively you can set year-month, pi_last_name and pi_email as epics PV by configuring the epics section of the `config <https://github.com/xray-imaging/globus/blob/master/config.py>`_ file


Usage
-----

Once the `DTagging <https://github.com/xray-imaging/DTagging>`_ medm screen is synchronized with the APS scheduling system and contains valid values like:

.. image:: medm_screen.png
  :width: 400
  :alt: medm screen

you can run `globus <https://github.com/xray-imaging/globus>`_  as follows:

globus -h for help
        
    globus init
        Creates a globus.conf default file

    globus show
        Show all endpoints shared and owned by the active globus credentials 

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
