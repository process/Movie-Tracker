#!/bin/sh

rm -f database.db
sqlite3 database.db < db.schema
