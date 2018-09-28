# Vegan Shopping List

This application allows registered users to add, edit and delete vegan items within a variety of vegan alternative categories.

The application can be access via http://localhost:8000 with the following pages:
* Home Page: /
    * Displays all current vegan alternative categories
    * Displays the latest added vegan items
    * Logged in users can add a new vegan item from this page
* Category Page: /catalog/<category_name>/items
    * Displays all the vegan items available for the selected category
    * Logged in users can add a new vegan item to the category from this page
* Category Item Page: /catalog/<category_name>/<item_title>
    * Dsiplays specific information of the selected vegan item
    * Logged in users can edit/delete the vegan items that they've added
* Edit Category Item Page: /catalog/<item_title>/edit
    * Logged in users can edit their own vegan items
* Delete Category Item page: /catalog/<item>/delete
    * Logged in users can delete their own vegan items
* JSON endpoint: /catalog.json
    * Retrieves all the vegan items grouped by category

This application is written in [Python](https://www.python.org/) using [Flask](http://flask.pocoo.org/) web framework, a third-party [OAuth 2.0](https://oauth.net/2/) authentication & authorization service (like Google Accounts and Facebook Accounts), and [SQLAlchemy](http://www.sqlalchemy.org/) SQL toolkit to manage the following database tables:

Table **user**

Column    | Type         | Modifiers                      
--------- |------------- |----------------------------
id        | Integer      | primary_key=True
name      | Sring(32)    | nullable=False, index=True
email     | Sring(250)   | nullable=False
picture   | Sring(250)   |

Table **category**

Column | Type      | Modifiers
------ |---------- |------------------------
id     | Integer   | primary_key=True
name   | Sring(80) | nullable=False, index=True

Table **item**

Column        |  Type       | Modifiers
------------- |------------ |----------------------------------
id            | Integer     | primary_key=True
created_date  | DateTime    | default=datetime.datetime.utcnow
title         | String(80)  | nullable=False
description   | String(250) | nullable=False
cat_id        | Integer     | ForeignKey('category.id')
user_id       | Integer     | ForeignKey('user.id')

## Getting Started

These instructions will get you a copy of the application up and running.

### Git

If you don't already have Git installed, [download Git from git-scm.com.](http://git-scm.com/downloads) Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash).  
(On Mac or Linux systems you can use the regular terminal program.)

### VirtualBox

VirtualBox is the software that actually runs the VM. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Downloads)  Install the *platform package* for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads) Install the version for your operating system.

### Prerequisites

* [Python 2.7.12](https://docs.python.org/2/) - the application programming language
* [Werkzeug 0.8.3](http://werkzeug.pocoo.org/) - the Python WSGI utility library (pip install werkzeug==0.8.3)
* [Flask 0.9](http://flask.pocoo.org/) - the microframework for Python based on Werkzeug, Jinja 2 (pip install flask==0.9)
* [SQLAlchemy 1.2.11](http://www.sqlalchemy.org) - Python SQL toolkit and Object Relational Mapper
* [oauth2client](https://github.com/google/oauth2client) - client library for accessing resources protected by OAuth 2.0
* [vagrantfile...](https://github.com/liqin-cao/vegan_shopping_list/blob/master/vagrantfile) - VM configurations

## Fetch the Source Code and VM Configuration

**Windows:** Use the Git Bash program (installed with Git) to get a Unix-style terminal.  
**Other systems:** Use your favorite terminal program.

From the terminal, run:

    git clone https://github.com/liqinca0/vegan_shopping_list.git

This will give you a directory named **vegan_shopping_list** complete with the source code for the application and a **vagrantfile** for installing all of the necessary tools. 

## Run the virtual machine!

Using the terminal, change directory to vegan_shopping_list (**cd /vegan_shopping_list**), then type **vagrant up** to launch your virtual machine:

    > cd /vegan_shopping_list
    > vagrant up

## Running the Vegan Shopping List App
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.

Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  Change to the /vegan_shopping_list directory by typing **cd /vegan_shopping_list**. This will take you to the shared folder between your virtual machine and host machine. Change to the /catalog directory by typing **cd /catalog**. This will take you to the application folder.

    > vagrant ssh
    > cd /vegan_shopping_list
    > cd /catalog
    
Type **ls** to ensure that you are inside the directory that contains application.py, db_models.py, db_initdata.py, oauth_utils.py, fb_client_secrets.json, google_client_secrets.json and two directories named 'templates' and 'static'.

    > ls
    > python db_models.py
    > python db_initdata.py
    > python application.py
    
1. **python db_models.py** - initializes the database
2. **python db_initdata.py** - populates the database with vegan alternative categories and some vegan items
3. **python application.py** - runs the Flask web server
4. In your browser visit **http://localhost:8000** to view the vegan shopping list app.

You should be able to view vegan alternative categories and items. After logging in with Google or Facebook account, you should be able to add, edit, and delete your own vegan items.

## Known Issues

* Facebook login is not suppored on Firefox Version 62.0. Using the sample code from [Facebook Login for the Web with the JavaScript SDK](https://developers.facebook.com/docs/facebook-login/web), the same behavior is observed.

## Release Notes

* Facebook login is not available on Firefox 62.0; only Google login is suppored on Firefox 62.0.
* For thread safe access to the database, the scoped_session() is used so that a single global variable can be used to safely represent transactional database sessions with sets of objects, localized to a single request thread.  See [Contextual/Thread-local Sessions](http://docs.sqlalchemy.org/en/latest/orm/contextual.html) for more detail.
* Modal login dialog is implemented with [Bootstrap Modal Plugin](https://www.w3schools.com/bootstrap/bootstrap_modal.asp).
* [Requiring HTTPS for Facebook Login](https://developers.facebook.com/blog/post/2018/06/08/enforce-https-facebook-login/) will be enforced by October 6, 2018.  The application can still run with HTTP on “localhost” addresses, but only while the app is still in development mode.

## Tested With

* Windows 10 Enterprise
* ubuntu-16.04
* Google Chrome Version 68.0.3440.106
* Microsoft Edge Version 25.10586.672.0
* Firefox Version 62.0

## Contributing

N/A

## Versioning

N/A

## Authors

* Liqin Cao

## License

This project is licensed under the LC License.

## Acknowledgments

* Udacity Full Stack Web Developer Nanodegree
* [W3School](https://www.w3schools.com/) for icons and css styling tips
* [www.webkinzinsider.com](http://www.webkinzinsider.com/w/images/5/52/Chicken_Sad.png) for the error page image
* [SNAPPA](https://snappa.com/) to create the app banner image
* [United Poultry Concerns](http://upc-online.org/) for the banner background image
* [Flask Snippets](http://flask.pocoo.org/snippets/3/) for CSRF protection of CRUD operations