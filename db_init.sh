#!/bin/bash

rm -f app.db
rm -rf migrations
python3 run.py db init
python3 run.py db migrate
python3 run.py db upgrade
python3 run.py db_populate