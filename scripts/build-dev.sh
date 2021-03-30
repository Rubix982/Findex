#!/bin/sh

make remove
sudo docker-compose -f docker-compose.dev.yaml up --build