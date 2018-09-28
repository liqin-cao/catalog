# Amazon Lightsail Configuration For Hosting Catalog Flask Application With PostgreSQL Database

Take a baseline installation of a AWS Lightsail Linux server and prepare it to host an existing web application by
* securing the server from a number of attack vectors,
* installing and configuring a PostgreSQL database server, and 
* deploying the existing Catalog Flask applications onto it.

## Amazon Lightsail Server Info
* Public IP Address: 34.205.85.252
* SSH Port: 2200
* Web Application URL: http://34.205.85.252.xip.io/

## Software Summary

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
* On the Lightsail **Connect** tab, follow the instructions to log into the server using my own SSH client [MobaXterm](https://mobaxterm.mobatek.net/) with user **ubuntu** and the default account private key.


### Secure The Server
#### Step 3 Update all currently installed packages
  
    $ sudo apt-get update
    $ sudo apt-get upgrade

#### Step 4 Change the SSH port from 22 to 2200
* Change SSH Port from 22 to 2200 in `/etc/ssh/sshd_config` file:
      
      $ sudo vi /etc/ssh/sshd_config
      
* Restart the SSH service:

      $ sudo service ssh restart 
      
* Finally, on the Lightsail **Networking** tab, add Custom/TCP/2200 to the **Firewall** section.

#### Step 5  Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
* Check UFW status is inactive
      
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
    
    $ sudo adduser grader

#### Step 7 Give grader the permission to sudo command
* Create a sudo access file `/etc/sudoers.d/grader` for **grader**:

      $ sudo vi /etc/sudoers.d/grader
   
      # User rules for grader
      grader ALL=(ALL) NOPASSWD:ALL

#### Step 8 Create an SSH key pair for grader using the ssh-keygen tool
* From local machine, generate a SSH key pair for **grader**.  when prompted for file to save the key, enter `grader`.  This command generates two files: `grader` and `grader.pub`. Rename `grader` file to `grader.pem`.
 
      $ ssh-keygen
      $ mv grader grader.pem
 
* Back on Ubuntu Linux server, switch the user to **grader**:

      $ sudo su - grader
      
* Create a `.ssh` folder in `/home/grader` directory, set the folder owner to **grader** and grant read/write/execute privilege only to the owner:

      $ cd /home/grader
      $ mkdir .ssh
      $ chown grader:grader /home/grader/.ssh
      $ chmod 700 /home/grader/.ssh
      
* Create a `/home/grader/.ssh/authorized_keys` file, copy the content of `grader.pub` (generated public key) and grant read/write privilege only to the owner:

      $ vi /home/grader/.ssh/authorized_keys
      $ chmod 600 /home/grader/.ssh/authorized_keys

* Log into the server using [MobaXterm](https://mobaxterm.mobatek.net/) SSH session with user **grader** and `grader.pem` (generated private key).

To disable password login and remote login of the `root` user, follow the instructions from [How To Disable Remote Logon For Root On Ubuntu 16.04 LTS Servers](https://websiteforstudents.com/how-to-disable-remote-logon-for-root-on-ubuntu-16-04-lts-servers/):
* `sudo vi /etc/ssh/sshd_config` and set `PasswordAuthentication no`
* `sudo vi /etc/ssh/sshd_config` and change `PermitRootLogin prohibit-password` to `PermitRootLogin no`
* `sudo service ssh restart`

### Prepare To Deploy The Project
#### Step 9 Configure the local timezone to UTC
#### Step 10 Install and configure Apache to serve a Python mod_wsgi application
#### Step 11 Install and configure PostgreSQL
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
