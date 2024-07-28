# DevGrid - Python Developer Challange

Python Flask web application with Mongo database to collect and store data from OpenWeather API.

## Table of contents

* [Requirements](#requirements)
    * [Manual Installation](#manual-installation)
    * [Docker and docker-compose](#docker-and-docker-compose)
    * [Flask and uWSGI](#flask-and-uwsgi)
    * [aiohttp](#aiohttp)
    * [MongoDB and pymongo](#mongodb-and-pymongo)
    * [python-dotenv](#python-dotenv)
    * [Faker](#faker)
* [Run the application](#run-the-application)
    * [Manual startup and restart](#manual-startup-and-restart)
    * [Docker installation](#docker-installation)
    * [Environment variables configuration](#environment-variables-configuration)
* [Test the application](#test-the-application)
    * [Scripts](#scripts)
        * [Unit tests and integration tests](#unit-tests-and-integration-tests)
        * [End-to-end tests](#end-to-end-tests)
        * [Testing everything](#testing-everything)
    * [Manually test](#manually-test)
        * [Collect endpoint (POST)](#collect-endpoint-post)
        * [Progress endpoint (GET)](#progress-endpoint-get)

## Requirements

### Manual Installation

[Installing and setting up the web application with Docker](#docker-installation) will automatically install the Python requirements, but if it is needed to make it by hand, its possible by using virtualenv, pyenv or any other similar Python virtual environment management tools, using only Pip for the installation.

```bash
cd devgrid-challenge/ # Enter the repository root
virtualenv venv # Create local virtualenv
source venv/bin/activate # Acitvate virtualenv
pip install -r reqs.txt # Install the Python requirements
```

### Docker and docker-compose

For the service to run on independent virtualized containers, [Docker CLI](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) are requires to run the application.

### Flask and uWSGI

Flask was chosen because I am more familiar with it and also it is a really fast and simple web framework, or microframework. Since Flask itself doesn't offer a production environment to run its apps, uWSGI was chosen as a web server interface to run it in a production environment, also due to Flask docs recommendation and because of uWSGI configurations.

### aiohttp

This library was chosen to handle asynchronous requests to collect data from Open Weather API.

### MongoDB and pymongo

MongoDB (7.0.12 or newer) was chosen because the data to be stored from Open Weather API will be purposefully redundant, so no need to use a relational SQL database, and because of MongoDB speed for finding data. PyMongo was chosen to be the library to connect and use MongoDB tools due to its similarities to the original Mongo Shell.

### python-dotenv

To manage project environment variables, python-dotenv allows us to create a simple `.env` file side-by-side with Python's `os.getenv` function, allowing us to use sensitive and/or mutable information inside of the code, like API keys, server ports, database location and more.

### Faker

Faker is one of the most famous libraries to create random data like names, emails, numbers and dates, enabling us to use it for testing different user entries and possibilities.

## Run the application

### Manual startup and restart

[Installing and setting up the web application with Docker](#docker-installation) will automatically run the uWSGI-Flask application, but if it is needed to do it by hand, its possible by running the following commands:

```bash
cd devgrid-challenge/ # Enter the repository root
chmod +x start.sh # Transform start.sh into an executable file
./start.sh # Start or Restart the application
```

For the `./start.sh` command to work, it is needed to configure `.env` environment variables, but in this repository, the `.env` is already filled up and tracked by Git -- in a normal and common project with sensible information of a real company, `.env` should never be tracked by Git. Checkout the environment variables section.

To run on development, you can just run:

```bash
source venv/bin/activate # Activate virtualenv
python3 index.py # Start application
```

### Docker installation

With the files `Dockerfile` and `docker-compose.yaml` in the repository root folder, it is possible to set up both Python Flask application and MongoDB Server by running the following command:

```bash
docker compose up
```

### Environment variables configuration

Environment variables can be configured both on `.env` and on `docker-compose.yaml`. Nothing needs to be changed for the application to run, based on the given files. But if it is needed to change the OpenWeather API Key or MongoDB connection info, change on `.env`.

## Test the application

There are two ways of running tests for this application, one of them is through running script and the other is manually testing.

You can run tests both on your machine or on the virtualized container. To run inside the container, when it is running, run the following command to be able to do the testing commands shown below:

```bash
docker exec -it <container_id> bash
```

### Scripts

#### Unit tests and integration tests

It is possible to run unit and integration tests by entering the already configured virtual environment and running the following command:

```bash
python3 -m unittest tests.unit_int.all
```

#### End-to-end tests

The same way as above, it is possible to run end-to-end tests by running the following command:

```bash
python3 -m unittest tests.e2e.all
```

Please, note that end-to-end tests may take a long time.

#### Testing everything

It is possible to combine all tests (unit, integration and end-to-end) by running the following command:

```bash
python3 -m unittest tests.all
```

Please, note that since end-to-end tests compose all of these tests, this command execution may take a long time.

### Manually test

By using any HTTP request testing tool, such as browsers, Postman, Curl or VSCode "REST Client" extension, it is possible to manually test the two endpoints of this Flask application by using the following configurations for each endpoint.

#### Collect endpoint (POST)

```
@baseUrl = http://localhost
@port = 8080

POST {{baseUrl}}:{{port}}/collect/2000
Content-Type: application/json

{}
```

With empty request body.

#### Progress endpoint (GET)

```
@baseUrl = http://localhost
@port = 8080

GET {{baseUrl}}:{{port}}/progress/1000
Content-Type: application/json

###
```

Obviously, updating `baseUrl` and `port` by depending on your local environment configuration.