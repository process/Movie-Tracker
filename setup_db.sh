#!/bin/bash

if [ -f database.db ];
then
  echo "Database already exists. Please delete."
  exit 1
fi

sqlite3 database.db < db.schema
