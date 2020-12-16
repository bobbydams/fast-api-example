# FastAPI Example API

This FastAPI example implements basic principles of Domain Driven Design and
allows for various backend adapters to be used to persist data.

# Prerequisites

This application recommends using:

- [Python v3.8](https://www.python.org/downloads/release/python-380/)
- [Poetry](https://pypi.org/project/poetry/)

# Installation

To install this project in a development environment, run the following command.

```
poetry install
poetry shell
```

If Poetry is not available, install using the `requirements.txt` included in this project.

```
pip install -r requirements.txt
```

# Running Application

To run the application in a development environment, run the following command.

```
uvicorn apps.api.app:app --reload
```

In addition, a Docker compose file is available to run the application in a Docker container.
This command requires the [Docker engine](https://docs.docker.com/get-docker/) as well as
[Docker Compose](https://docs.docker.com/compose/install/) to be installed on the
host machine. Note: The demo application mentioned below will not be served via Docker.

```
docker-compose up --build
```

Then navigate to http://localhost:8000

# Authentication

To authenticate with application, use username `test` and password `test` by
posting them to the following URL:

http://localhost:8000/login

```
{
  "username": "test",
  "password": "test"
}
```

In the response will be an `access_token` and `refresh_token`. The access token
should be included in the `Authorization` header as a bearer token.

# Demo Application

A demo application can be accessed with the following URL. This application will
demonstrate the use of the get and add methods on the book resource.

http://localhost:8000/demo/books

# API Documentation

When serving the development server, go to http://localhost:8000/apidocs to
view OpenAPI documentation. This will include documentation about each endpoint
and examples.

# Postman Collection

This project also includes a [Postman](https://www.postman.com/downloads/) collection
for testing individual endpoints available with this API project.

Import the file `Fast API Example.postman_collection.json` into your Postman application.

# Testing

To run tests, run the following command.

```
pytest
```

To view pytest coverage statistics:

```
pytest --cov=apps/api
```
