# Project 3 - Polyglot Persistence and Service Discovery

**Team members**: Zach Hofmeister, Ryan Patrick 

## Description

Description

## Starting the services

First, create a new Python virtual environment like this:
> python3 -m venv env

Next, activate the virtual environment like this:
> source env/bin/activate

Next, install the required dependecies like this:
> pip install -r requirements.txt

Next, install haproxy like this:
> sudo apt install haproxy

Next, install foreman like this:
> sudo apt install ruby-foreman

Next, generate the databases by running the **regenUsers.sh** and **regenPosts.sh** scripts inside the **/databases** directory.

Next, copy the configuration settings found in **example-haproxy.cgf** and paste them at the bottom of the config file for haproxy.
The config file will be located in the /etc/haproxy directory, and you must open it with root privilege to edit it. For example:
> sudo nano /etc/haproxy/haproxy.cfg

Next, restart haproxy like this:
> sudo systemctl restart haproxy

Finally, start the services using foreman like this:
> foreman start --formation users=1,posts=3

You should be able to navigate to localhost:5000/haproxy?stats to see the services if everything is done correctly.

## Users Service REST API Documentation



## Posts Service REST API Documentation



## Shortcomings

