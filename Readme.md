# Project usage guide
*before following the guide, please make sure you have python3 installed.




####virtual enviroment setup
some project dependencies are required in order to run the code, it is easiest to set everything up using the python venv package.
if you are familiar with python and wish to set up the dependencies some other way, please skip this part.

Open a terminal and install venv by typing: `apt-get install python3-venv`

Go to the project's main directory and create a virtual env by typing: `python3 -m venv env`

Activate the virtual env by running: `source env/bin/activate`

Install the project's dependencies by typying: `pip3 install -r requirements.txt`

You are now ready to run the code.

*when done working, deactivate the virtual env by simply typing `deactivate`

#### run the code.
Open a browser and enter the coderz website on https://multi.gocoderz.com, after logging in, go to UnityTest -> Games -> Demo Game. once loading is finished, the second icon from the right on the top left panel is a screen with wifi signal, click on it and copy the authentication token.

at the python project, on either index.py or one of the scripts in the examples folder, replace the default token with the one you copied
, and then run the code. you will now see the robot following your commands on the coderz website.