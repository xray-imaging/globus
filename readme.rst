======
GLOBUS
======

Tasks
-----
    - Authenticate with Globus
    - Create a folder on a Globus server
    - Share the Globus server folder with a user
    - Send to the user an email with the URL to the shared folder

Installation
------------

    - copy globus.py and globus_lib.py in your working directory

Configuration
-------------

    - see Step 1 at https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
      to register your app with Globus and get your project app_id

    - set your project app-id and personal-endpoint-uuid as default in the config.py file

Usage
-----
    
    globus.py -h for help
        
    globus.py init
        Creates a globus.conf default file

        globus.py show
            Show all endpoints shared and owned by the active globus credentials 

        globus.py mkdir
            Using the current user information from the scheduling system,
            - creates a directory named "year-month/pi_last_name" on the endpoint
            - share the directory with globus with the user
            - send a notification to the user with the directory globus link 

Example:
    globus.py mkdir
        2019-08-30 19:52:04,134   General 
        2019-08-30 19:52:04,134     config           globus.conf 
        2019-08-30 19:52:04,134     verbose          True 
        2019-08-30 19:52:04,247   Please go to this URL and login: https://auth.globus.org/v2/oauth2/
        Please enter the code you get after login here: 
        2019-08-30 19:52:18,754   Show all endpoints shared and owned by my globus user credentials 
        2019-08-30 19:52:18,755   *** Endpoints shared with me: 
        2019-08-30 19:52:19,406   *** *** [ad484910-0842-11e7-bb15-22000b9a448b] aps_32id 
        2019-08-30 19:52:19,407   *** *** [1d5c7410-72a8-11e5-ba4c-22000b92c6ec] petrel SEP DMagic 32-ID 
        2019-08-30 19:52:19,407   *** *** [e133a81a-6d04-11e5-ba46-22000b92c6ec] None 
        2019-08-30 19:52:19,407   *** *** [f9489388-dff8-11e5-978f-22000b9da45e] None 
        2019-08-30 19:52:19,408   *** Endpoints owned with me:: 
        2019-08-30 19:52:19,499   *** *** [979afa64-ffed-11e8-9345-0e3d676669f4] fast@merlot 
        2019-08-30 19:52:19,499   *** *** [9bb494f2-ec29-11e8-8cab-0a1d4c5c824a] sec2admin@akitaWin 
        2019-08-30 19:52:19,500   *** *** [576cdd42-ec22-11e8-8cab-0a1d4c5c824a] sec2admin@grayhound 
        2019-08-30 19:52:19,500   *** *** [f1f39c62-ec26-11e8-8cab-0a1d4c5c824a] tomo@handyn 
        2019-08-30 19:52:19,500   *** *** [da277910-c06f-11e8-8c25-0a1d4c5c824a] txmtwo 
        2019-08-30 19:52:19,501   *** *** [671a86f0-ec26-11e8-8cab-0a1d4c5c824a] user2bmb@lyra 
        2019-08-30 19:52:19,501   *** *** [372404f4-ec2f-11e8-8cab-0a1d4c5c824a] user2bmb@pg10ge 
        2019-08-30 19:52:19,502   Creating user directories on server e133a81a-6d04-11e5-ba46-22000b92c6ec://2-BM/ 
        2019-08-30 19:52:19,790   *** Path /2-BM/2022-01/ already exists 
        2019-08-30 19:52:20,054   *** Path /2-BM/2022-01/empty pi_last_name/ already exists 
        2019-08-30 19:52:20,055   Sharing /2-BM/2022-01/empty pi_last_name with test@anl.gov 
        2019-08-30 19:52:20,380   *** Path /2-BM/2022-01/empty pi_last_name/ has been shared with decarlo@anl.gov 
