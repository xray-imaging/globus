Tasks:

        - Authenticate with Globus
        - Create a folder on a Globus server
        - Share the Globus server folder with a user
        - Send to the user an email with a link to the shared folder

Installation:

        - copy globus.py and globus_lib.py in your working directory

Configuration:

        - see Step 1 at https://globus-sdk-python.readthedocs.io/en/stable/tutorial/#step-1-get-a-client
          to register your app with Globus and get your project app_id

        - set your project app_id in globus.py

Usage:
        globus.py -h for help
        
        - running globus.py the first time provides the list of Globus servers shared with your Globus account. 
          Select one Globus server among the one available by assigning its UUID to the globus_server_id variable.
