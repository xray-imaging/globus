======
GLOBUS
======


`globus <https://github.com/decarlof/globus>`_ is a python script that automatically creates a directory on a globus server as "year-month/pi_last_name" (or any other preset path) and sends a customizable notification email to "pi_email" that includes the URL to the shared folder.

year-month, pi_last_name and pi_email area automatically retrieved from the APS scheduling system for the current user (see `DTagging <https://github.com/decarlof/DTagging>`_ for more information).


Tasks
-----
- Authenticate with Globus
- Create a folder on a Globus server
- Share the Globus server folder with a user
- Send to the user an email with the URL to the shared folder

Installation
------------

- copy the content of `globus <https://github.com/decarlof/globus>`_ in your working directory

Configuration
-------------

- see Step 1 in the `Globus tutorial <https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client>`_ to register your app with Globus and get your project app_id
- set your project app-id and personal-endpoint-uuid as default in the config.py file
- customize the email to the user by editing the `message <https://github.com/decarlof/globus/blob/master/message.txt>`_ 
- for automatic retrieve of user information see `DTagging <https://github.com/decarlof/DTagging>`_  alternatively you can set year-month, pi_last_name and pi_email as epics PV and configure `init_general_PVs <https://github.com/decarlof/globus/blob/master/globus.py>`_


Usage
-----

Once the `DTagging <https://github.com/decarlof/DTagging>`_ medm screen is synchronized with the APS scheduling system and contains valid values like:

.. image:: medm_screen.png
  :width: 400
  :alt: medm screen

you can run `globus <https://github.com/decarlof/globus>`_  as follows:

globus.py -h for help
        
    globus.py init
        Creates a globus.conf default file

    globus.py show
        Show all endpoints shared and owned by the active globus credentials 

    globus.py email
        Using the current user information from the scheduling system:

        - create a directory named "year-month/pi_last_name" on the endpoint
        - share the directory with globus with the user
        - send a notification to the user with the URL to the shared folder and a user customizable `message <https://github.com/decarlof/globus/blob/master/message.txt>`_

