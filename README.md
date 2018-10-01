# Amazon Lightsail Configuration For Hosting Catalog Flask Application With PostgreSQL Database

Take a baseline installation of a AWS Lightsail Linux server and prepare it to host an existing web application via:
* securing the server from a number of attack vectors,
* installing and configuring a PostgreSQL database server, and 
* deploying the existing Catalog Flask applications onto it.

## Amazon Lightsail Server Info
* Public IP Address: 34.205.85.252
* SSH Port: 2200
* Web Application URL: http://34.205.85.252.xip.io/

## Software Summary
* apache2
* bleach
* Flask
* git
* httplib2
* libapache2-mod-wsgi
* oauth2client
* pip
* postgresql
* postgresql-contrib
* python-dev
* python 2.7.12
* python-sqlalchemy
* python-psycopg2
* requests
* sqlalchemy
* virtualenv

## Configuration Summary

### Getting Started With Amazon Lightsail
#### Step 1 - Start a new Ubuntu Linux server instance on [Amazon Lightsail](https://lightsail.aws.amazon.com)
* Create an AWS account with **12 Months of Free Tier Access**.
* Create an Amazon Lightsail instance using **OS Only** and **Ubuntu 16.04 LTS** instance image.
* Choose the lowest instance plan which should be free for the first month.
* Give the instance a hostname.
* Once the instance is up and running, the public IP address of the instance is displayed along with its name.

#### Step 2. SSH into the Ubuntu Linux server
* On the Lightsail **Connect** tab, verify SSH connection to the server via the **Connect using SSH** button.
* On the Lightsail **Connect** tab, follow the instructions to log into the server using SSH client [MobaXterm](https://mobaxterm.mobatek.net/) with user `ubuntu` and the default account private key.


### Secure The Server
#### Step 3 - Update all currently installed packages
* From Ubuntu Linux server command prompt, run the following `apt-get` commands:

      $ sudo apt-get update
      $ sudo apt-get upgrade

#### Step 4 - Change the SSH port from 22 to 2200
* Change SSH Port from **22** to **2200** in `/etc/ssh/sshd_config` file:
      
      $ sudo vi /etc/ssh/sshd_config
      
* Restart the SSH service:

      $ sudo service ssh restart 
      
* Finally, back on the Amazon Lightsail **Networking** tab, add **Custom|TCP|2200** to the **Firewall** section.

#### Step 5 - Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
* Check UFW status is inactive:
      
      $ sudo ufw status
      
* Block all incoming and allow all outgoing connections:

      $ sudo ufw default deny incoming
      $ sudo ufw default allow outgoing
 
* Allow SSH port 2200, HTTP port 80 and NTP port 123:

      $ sudo ufw allow 2200/tcp
      $ sudo ufw allow www
      $ sudo ufw allow ntp
      
* Show ports added:

      $ sudo ufw show added
      
* Enable UFW and verify status is active:

      $ sudo ufw enable
      $ sudo ufw status


### Give grader Access
#### Step 6 - Create a new user account named grader
* Create a **grader** user with any password (this feature will be replaced with key-based SSH authentication):

      $ sudo adduser grader

#### Step 7 - Give grader the permission to sudo command
* Create a sudo access file `/etc/sudoers.d/grader` for **grader**:

      $ sudo vi /etc/sudoers.d/grader
      
      # User rules for grader
      grader ALL=(ALL) NOPASSWD:ALL

#### Step 8 - Create an SSH key pair for grader using the ssh-keygen tool
* From local machine, generate a SSH key pair for **grader**.  When prompted for file to save the key pair, enter `grader`.  This command generates two files: `grader` and `grader.pub`. Rename `grader` file to `grader.pem`.
 
      $ ssh-keygen
      $ mv grader grader.pem
 
* Back on the Ubuntu Linux server, switch the user to **grader**:

      $ sudo su - grader
      
* Create a `.ssh` folder in `/home/grader` directory, set the folder owner to **grader** and grant read/write/execute privilege only to the owner:

      $ cd /home/grader
      $ mkdir .ssh
      $ chown grader:grader /home/grader/.ssh
      $ chmod 700 /home/grader/.ssh
      
* Create a `/home/grader/.ssh/authorized_keys` file, copy the content of `grader.pub` (generated public key) and grant read/write privilege only to the owner:

      $ vi /home/grader/.ssh/authorized_keys
      $ chmod 600 /home/grader/.ssh/authorized_keys

* Log into the Ubuntu Linux server using [MobaXterm](https://mobaxterm.mobatek.net/) SSH session with user **grader** and `grader.pem` (generated private key).

Follow the instructions from [How To Disable Remote Logon For Root On Ubuntu 16.04 LTS Servers](https://websiteforstudents.com/how-to-disable-remote-logon-for-root-on-ubuntu-16-04-lts-servers/) to disable password login and remote login of the `root` user, :
* `sudo vi /etc/ssh/sshd_config` and set `PasswordAuthentication no`
* `sudo vi /etc/ssh/sshd_config` and change `PermitRootLogin prohibit-password` to `PermitRootLogin no`
* Restart SSH service with `sudo service ssh restart`


### Prepare To Deploy The Project
#### Step 9 - Configure the local timezone to UTC
* Log into the Ubuntu Linux server using [MobaXterm](https://mobaxterm.mobatek.net/) SSH session as **grader**.
* Check local timezone is set to UTC:

      $ sudo dpkg-reconfigure tzdata
      
      Current default time zone: 'Etc/UTC'
      Local time is now:      Mon Sep 24 16:58:05 UTC 2018.
      Universal Time is now:  Mon Sep 24 16:58:05 UTC 2018.

#### Step 10 - Install and configure Apache to serve a Python mod_wsgi application
* Install `apache2` Apache HTTP Server:

      $ sudo apt-get install apache2
      
* Install `libapache2-mod-wsgi` to provide a WSGI compliant interface for hosting Python based web applications under Apache:
      
      $ sudo apt-get install libapache2-mod-wsgi

#### Step 11 - Install and configure PostgreSQL
Follow the instructions from [How To Secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps) to install and secure PostgreSQL.

* Install PostgreSQL:

      $ sudo apt-get install postgresql postgresql-contrib
      
      Setting up postgresql-9.5 (9.5.14-0ubuntu0.16.04) ...
      Creating new cluster 9.5/main ...
            config /etc/postgresql/9.5/main
            data   /var/lib/postgresql/9.5/main
            locale en_US.UTF-8
            socket /var/run/postgresql
            port   5432

* Verify that no remote connections are allowed by looking in the host based authentication file:
      
      $ sudo vi /etc/postgresql/9.5/main/pg_hba.conf

      local   all             postgres                                peer
      local   all             all                                     peer
      host    all             all             127.0.0.1/32            md5
      host    all             all             ::1/128                 md5

* Create a new database user named `catalog` that has limited permissions to the `catalog` application database: 

      $ sudo su - postgres
      $ psql
      postgres=# create user catalog with password 'catalog';
      postgres=# create database catalog with owner catalog;
      postgres=# \c catalog
      catalog=# revoke all on schema public from public;
      catalog=# grant all on schema public to catalog;


* Verify `catalog` user is successfully created:

      postgres=# \du
      
  | Role name |                         Attributes                         | Member of
  | ----------|------------------------------------------------------------| -----------
  | catalog   |                                                            | {}
  | postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

* Verify `catalog` database is successfully created:

      postgres=# \l
  |     Name   |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges    |
  | -----------|----------|----------|-------------|-------------|----------------------- |
  | catalog    | catalog  | UTF8     | en_US.UTF-8 | en_US.UTF-8 |                        |
  | postgres   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |                        |

    
#### Step 12 - Install git
* Install `git` to clone the Item Catalog application from Github repository:

      $ sudo apt-get install git


### Deploy The Item Catalog Project
#### Step 13 - Clone and setup the Item Catalog application from the Github repository
* Clone Item Catalog application from the Github repository and place it `/var/www` folder:

      $ cd /var/www
      $ sudo git clone https://github.com/liqin-cao/catalog.git
      
Follow the instructions from [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps) to setup a simple Flask application for testing.

* Install and enable `mod_wsgi`:

      $ sudo apt-get install libapache2-mod-wsgi python-dev
      $ sudo a2enmod wsgi

* Create a simple test Flask application in `/var/www/catalog/catalog/__init__.py`:

      $ cd /var/www/catalog/catalog
      $ sudo vi __init__.py
      
            from flask import Flask
            app = Flask(__name__)
            @app.route("/")
            def hello():
                return "Hello Udacity!"
            if __name__ == "__main__":
                app.run()

* Install `pip` and `virtualenv`:

      $ sudo apt-get install python-pip
      $ sudo pip install --upgrade pip
      $ sudo pip install virtualenv

* Setup a virtual environment to keep the application and its dependencies isolated from the main system:

      $ cd /var/www/catalog/catalog
      $ sudo virtualenv venv
      
      New python executable in /var/www/catalog/catalog/venv/bin/python
      Installing setuptools, pip, wheel...done.
      
      $ source /var/www/catalog/catalog/venv/bin/activate

* Install `Flask` and test the installation by running the simple test Flask application:

      $ sudo pip install Flask
      
      Successfully installed Flask-1.0.2 Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 click-7.0 itsdangerous-0.24
      
      $ sudo python __init__.py

* Create an Apache Virtual Hosts configuration file in `/etc/apache2/sites-available` folder:

      $ sudo vi /etc/apache2/sites-available/catalog.conf
      
            <VirtualHost *:80>
                  ServerName 34.205.85.252
                  ServerAdmin liqincao@gmail.com
                  WSGIScriptAlias / /var/www/catalog/catalog.wsgi
                  <Directory /var/www/catalog/catalog/>
                        Order allow,deny
                        Allow from all
                  </Directory>
                  Alias /static /var/www/catalog/catalog/static
                  <Directory /var/www/catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                  </Directory>
                  ErrorLog ${APACHE_LOG_DIR}/error.log
                  LogLevel warn
                  CustomLog ${APACHE_LOG_DIR}/access.log combined
            </VirtualHost>

* Enable the `catalog` site:

      $ sudo a2ensite catalog
      
* Create the `catalog.wsgi` file to server the Flask application:

      $ sudo vi /var/www/catalog/catalog.wsgi
            #!/usr/bin/python

            import sys
            import logging

            logging.basicConfig(stream=sys.stderr)
            sys.path.insert(0,"/var/www/catalog/")

            from catalog import app as application
            application.secret_key = 'In My Secret Life'

* Restart Apache service:

      $ sudo service apache2 restart

* Verify that the simple test Flask application is accessible from the browser URL `http://34.205.85.252.xip.io/`.

#### Step 14 - Make Item Catalog application accessible from a browser
* Install modules needed by the Item Catalog application:

      $ source /var/www/catalog/catalog/venv/bin/activate
      $ sudo apt-get -qqy install python-sqlalchemy
      $ sudo apt-get -qqy install python-psycopg2
      $ sudo pip install sqlalchemy
      $ sudo pip install oauth2client
      $ sudo pip install requests
      $ sudo pip install httplib2
      $ sudo pip install bleach
      
* Update sqlalchemy to connect to PostgreSQL database in `db_models.py`, `db_initdata.py` and `application.py`:

      engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

* Create database tables and populate the tables with initial data:

      $ sudo python db_models.py
      $ sudo python db_initdata.py
      
* Rename `application.py` to `__init__.py` and restart Apache service `sudo service apache2 restart`.

* Verify that the Item Catalog application is accessible from the browser URL `http://34.205.85.252.xip.io/`.

#### Step 15 - Setup OAuth support and secure .git repository
* Update [Google OAuth credentials](https://console.developers.google.com) (`Authorized JavaScript origins` and `Authorized JavaScript origins`) to use the DNS name provided by [xip.io](http://xip.io/) service: `http://34.205.85.252.xip.io/`.

* Download the updated Google client secrets JSON file.

* Follow instructions from [Hide Git Repos on Public Sites](https://davidegan.me/hide-git-repos-on-public-sites/) to ensure that `http://34.205.85.252.xip.io/.git/config` is not publicly accessible via a browser!

      $ sudo vi /etc/apache2/conf-enabled/security.conf
      
      <DirectoryMatch "/\.git">
          Require all denied
      </DirectoryMatch>

* Restart Apache service `sudo service apache2 restart`.

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
* [MobaXterm](https://mobaxterm.mobatek.net/) for connecting to the Linux server
* [xip.io](http://xip.io/) for providing a DNS name that refers to the Ubuntu Linux server IP address
* [How To Disable Remote Logon For Root On Ubuntu 16.04 LTS Servers](https://websiteforstudents.com/how-to-disable-remote-logon-for-root-on-ubuntu-16-04-lts-servers/)
* [How To Secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
* [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
* [How To Hide Git Repos on Public Sites](https://davidegan.me/hide-git-repos-on-public-sites/)
