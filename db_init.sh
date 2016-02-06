#!/bin/bash

rm -f app.db
rm -rf migrations
python run.py db init
python run.py db migrate
python run.py db upgrade

