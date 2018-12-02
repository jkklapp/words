# Word counter

Forked from (https://github.com/gableh/flask-docker-boilerplate)


## Setup

To build the images type `docker-compose build`
To run locally the containers `docker-compose up` and navigate to `localhost`

## Architecture

There are 6 containers:

ngingx - The webserver running Nginx
app - The applications
db - The database is using Mongo. This stores words.
worker - Processes url asynchrously (Celery)
monitor - Checks async tasks (Celery)
redis - Used by celery to store tasks' metadata
