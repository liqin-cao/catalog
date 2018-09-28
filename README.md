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
* libapache2-mod-wsgi
* postgresql
* postgresql-contrib

## Configuration Summary

### Getting Started With Amazon Lightsail
#### Step 1 Start a new Ubuntu Linux server instance on [Amazon Lightsail](https://lightsail.aws.amazon.com)
* Create an AWS account with **12 Months of Free Tier Access**.
* Create an Amazon Lightsail instance using **OS Only** and **Ubuntu 16.04 LTS** instance image.
* Choose the lowest instance plan which should be free for the first month.
* Give the instance a hostname.
* Once the instance is up and running, the public IP address of the instance is displayed along with its name.

#### Step 2 SSH into the Ubuntu Linux server
* On the Lightsail **Connect** tab, verify SSH connection to the server via the **Connect using SSH** button.
* On the Lightsail **Connect** tab, follow the instructions to log into the server using SSH client [MobaXterm](https://mobaxterm.mobatek.net/) with user `ubuntu` and the default account private key.


### Secure The Server
#### Step 3 Update all currently installed packages
* From Ubuntu Linux server command prompt, run the following `apt-get` commands:

      $ sudo apt-get update
      $ sudo apt-get upgrade

#### Step 4 Change the SSH port from 22 to 2200
* Change SSH Port from **22** to **2200** in `/etc/ssh/sshd_config` file:
      
      $ sudo vi /etc/ssh/sshd_config
      
* Restart the SSH service:

      $ sudo service ssh restart 
      
* Finally, back on the Amazon Lightsail **Networking** tab, add **Custom|TCP|2200** to the **Firewall** section.

#### Step 5  Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
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
#### Step 6 Create a new user account named grader
* Create a **grader** user with any password (this feature will be replaced with key-based SSH authentication):

      $ sudo adduser grader

#### Step 7 Give grader the permission to sudo command
* Create a sudo access file `/etc/sudoers.d/grader` for **grader**:

      $ sudo vi /etc/sudoers.d/grader
   
      # User rules for grader
      grader ALL=(ALL) NOPASSWD:ALL

#### Step 8 Create an SSH key pair for grader using the ssh-keygen tool
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
#### Step 9 Configure the local timezone to UTC
* Log into the Ubuntu Linux server using [MobaXterm](https://mobaxterm.mobatek.net/) SSH session as **grader**.
* Check local timezone is set to UTC:

      $ sudo dpkg-reconfigure tzdata
      Current default time zone: 'Etc/UTC'
      Local time is now:      Mon Sep 24 16:58:05 UTC 2018.
      Universal Time is now:  Mon Sep 24 16:58:05 UTC 2018.

#### Step 10 Install and configure Apache to serve a Python mod_wsgi application
* Install **apache2** Apache HTTP Server:

      $ sudo apt-get install apache2
      
* Install **libapache2-mod-wsgi** to provide a WSGI compliant interface for hosting Python based web applications under Apache:
      
      $ sudo apt-get install libapache2-mod-wsgi

#### Step 11 Install and configure PostgreSQL
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

      $ sudo su postgres
      $ createuser catalog 
      $ createdb catalog
      $ psql
      postgres=# alter user catalog with encrypted password 'catalog';
      postgres=# grant all privileges on database catalog to catalog;

* Verify `catalog` database user is successfully created:

      postgres=# \du
      
  | Role name |                         Attributes                         | Member of
  | ----------|------------------------------------------------------------| -----------
  | catalog   |                                                            | {}
  | postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

* Verify `catalog` database is successfully created:

      postgres=# \l
  |     Name   |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges    |
  | -----------|----------|----------|-------------|-------------|----------------------- |
  | catalog    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/postgres         + |
  |            |          |          |             |             | postgres=CTc/postgres+ |
  |            |          |          |             |             | catalog=CTc/postgres   |
  | postgres   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |                        |

    
#### Step 12 Install git

### Deploy The Item Catalog Project
#### Step 13 Clone and setup the Item Catalog application from the Github repository
#### Step 14 Make Item Catalog application accessible from a browser 

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
* [How To Disable Remote Logon For Root On Ubuntu 16.04 LTS Servers](https://websiteforstudents.com/how-to-disable-remote-logon-for-root-on-ubuntu-16-04-lts-servers/)
* [How To Secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
