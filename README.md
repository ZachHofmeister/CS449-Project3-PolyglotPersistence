# Project 3 - Polyglot Persistence and Service Discovery

**Team members**: Zach Hofmeister, Ryan Patrick 

## Description

Description

## Starting the services

First, generate the databases by running the **regenUsers.sh** and **regenPosts.sh** scripts inside the **/databases** directory.

Next, ensure that the config for haproxy includes the configuration settings found in **example-haproxy.cgf**, and restart haproxy like this:
> sudo systemctl restart haproxy

Finally, start the services using foreman like this:
> foreman start --formation users=1,posts=3

You should be able to navigate to localhost:5000/haproxy?stats to see the services if everything is done correctly.

## Users Service REST API Documentation



## Posts Service REST API Documentation



## Shortcomings

