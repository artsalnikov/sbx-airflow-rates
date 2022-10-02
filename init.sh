#!/bin/bash

echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose build
docker-compose up
