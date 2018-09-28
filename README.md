# AWS Lightsail Configuration For Hosting Catalog Flask Application With PostgreSQL Database

Take a baseline installation of a AWS Lightsail Linux server and prepare it to host an existing web application by
* securing the server from a number of attack vectors,
* installing and configuring a PostgreSQL database server, and 
* deploying the existing Catalog Flask applications onto it.

## Getting Started With Amazon Lightsail
### Step 1 Start a new Ubuntu Linux server instance on [Amazon Lightsail](https://lightsail.aws.amazon.com)
### Step 2 SSH into the Ubuntu Linux server


## Secure The Server
### Step 3 Update all currently installed packages
### Step 4 Change the SSH port from 22 to 2200
### Step 5  Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

## Give grader Access
### Step 6 Create a new user account named grader
### Step 7 Give grader the permission to sudo
### Step 8 Create an SSH key pair for grader using the ssh-keygen tool

## Prepare To Deploy The Project
### Step 9 Configure the local timezone to UTC
### Step 10 Install and configure Apache to serve a Python mod_wsgi application
### Step 11 Install and configure PostgreSQL
### Step 12 Install git

## Deploy The Item Catalog Project
### Step 13 Clone and setup the Item Catalog application from the Github repository
### Step 14 Make Item Catalog application accessible from a browser 

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
