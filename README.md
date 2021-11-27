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

Next, install the following packages with this command:
> sudo apt install haproxy ruby-foreman redis python3-hiredis awscli python3-boto3

Next, copy the configuration settings found in **example-haproxy.cgf** and paste them at the bottom of the config file for haproxy.
The config file will be located in the /etc/haproxy directory, and you must open it with root privilege to edit it. For example:
> sudo nano /etc/haproxy/haproxy.cfg

Next, restart haproxy like this:
> sudo systemctl restart haproxy

Next, configure AWS CLI like this:

> aws configure

> AWS Access Key ID [None]: fakeMyKeyId

> AWS Secret Access Key [None]: fakeSecretAccessKey

> Default region name [None]: us-west-2

> Default output format [None]: table

Next, generate the users and posts databases by running the **regenAll.sh** script inside the **/databases** directory.

To rengenerate the polls database, start dynamodb with the following command:

> java -Djava.library.path=./databases/dynamodb/DynamoDBLocal_lib -jar ./databases/dynamodb/DynamoDBLocal.jar -sharedDb

And while that is running, run the **regenPolls.py** script like this:

> python3 regenPolls.py

Finally, start the services using foreman like this:
> foreman start --formation users=1,posts=3,likes=1,polls=1,svcrg=1,dynamoDB=1

You should be able to navigate to localhost:5000/haproxy?stats to see the services if everything is done correctly.

## Shortcomings

We believe the project is fully functional, but we didn't finish the REST API documentation besides example comments on how to make each type of request above their functions in their respective python file.