# Capstone2022

## Project Setup

1. This command is for creating the virtual env: python -m venv venv

2a. Activate the env:
for windows, type this command for activating the env : '\venv\Scripts\activate
for mac or linux, type this command to activate the env: source venv/bin/activate

2b. To add missing api key go to .env copy file and delete "copy" so you only see .env
    then put in the mailchimp api key inside the area where its missing. 

3. After activating install the all the packages with this command: pip install -r requirements.txt

4. Then use command to run application:  flask run

5. On front end make sure to install all packages using npm install

<!-- 
.env is a file I created that contains mailchimp Api Key.
~Venv file is the virtual environment file
~flaskenv is for Flaskenv for flask environment to set which file is the main app file. in this case it's app.py

flask_smorest is the package to create the api with flask,

this package provides api swagger doccumentation.

after running the application go to this url.

http://127.0.0.1:5000/docs
 --> 

