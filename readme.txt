Tasks:

        - Authenticate with Globus
        - Create a folder on a Globus server
        - Share the Globus server folder with a user
        - Send to the user an email with a link to the shared folder and experiment information

Installation:

        - copy globus.py and globus_lib.py in your working directory

Configuration:

        - see Step 1 at https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
          to register your app with Globus and get your project app_id

        - set your project app-id and personal-endpoint-uuid as default in the config.py file

Usage:
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