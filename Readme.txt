# Top Ten Lists Application

# Section 0: Intro
This app will allow users to create lists on a website, and rank items on those
lists

# Section 1: Set up environment
1. Download virtualbox, and vagrant
2. Run vagrant init on the folder location where your finalProject.py, and folders
are located
3. In the terminal type vagrant up
4. type vagrant ssh to login to the virtual machine
5. run 'run.py'
6. install all the modules from the requirements.txt file

Section 2: Requirements
Flask==0.10.1
Flask-SQLAlchemy==2.1
Flask-WTF==0.12
GnuPGInterface==0.3.2
Jinja2==2.8
MarkupSafe==0.23
SQLAlchemy==1.0.11
WTForms==2.1
Werkzeug==0.11.3
apt-xapian-index==0.44
argparse==1.2.1
chardet==2.0.1
command-not-found==0.2.44
## FIXME: could not find svn URL in dependency_links for this package:
distribute==0.6.24dev-r0
httplib2==0.9.2
itsdangerous==0.24
language-selector==0.1
oauth2client==1.5.2
pyasn1==0.1.9
pyasn1-modules==0.0.8
python-apt==0.8.3ubuntu7
python-debian==0.1.21ubuntu1
requests==2.9.1
rsa==3.3
six==1.10.0
ufw==0.31.1-1
wsgiref==0.1.2

Section 3: Installation
App not on github yet
Install by unzipping the file in the location where you have your virtual machine

Section 4: Setup
To setup the database first run database_setup.py
There is no populating script yet, database will be empty at first.

Section 5: How to run
To run the app type python run.py

Section 6: Usage
1.  Open http://localhost:5000
2.  To use the app, first click Login, this will create a user for you
3.  Now click on your author name and you will go to you lists page
4.  Here you click create a list
5.  Input a name, description and a pic_url for your list
6.  Now you have created a list
7.  No click the list name, and click create new item
8.  Populate your list with items!
9.  Now anyone can go the page, click on your author name and see your lists. 


To run the application:

If you are using the database in the file:
Do this:
1. Run project.py. 
2. In your browser open the url localhost:5000
3. To create a Top Ten list first click "Login"
4. Start adding lists and items!

Section 7: json endpoint
1. You can query data from the app at
	sitename/owners/json
	sitename/lists/json
	sitename/items/json

	

