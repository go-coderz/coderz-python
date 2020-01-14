# Usage

- Before following the guide, please make sure you have python3 installed.

### Virtual enviroment setup

Some project dependencies are required in order to run the code, it is easiest to set everything up using the python venv package.
If you are familiar with python and wish to set up the dependencies some other way, please skip this part.

Open a terminal and install venv by typing: `apt-get install python3-venv`

Go to the project's main directory and create a virtual env by typing: `python3 -m venv env`

Activate the virtual env by running: `source env/bin/activate`

Install the project's dependencies by typing: `pip3 install -r requirements.txt`

You are now ready to run the code.

\*when done working, deactivate the virtual env by simply typing `deactivate`

### Running the code

Go to https://multi.gocoderz.com, login and go to UnityTest -> Games -> Multi Game.
Once loading is finished, the second icon from the right on the top left panel is a screen with wifi signal, click on it and copy the authentication token.

run index.py at the python repository, paste the token when requested and choose the example code you wish to run. Go back to the CoderZ website and click on the "Play" icon (run simulation).
