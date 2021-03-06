#!/bin/bash

output=kitty_names.$(git rev-parse --short HEAD).sqlite

if [ -f "$output" ] ; then
  echo "output database exists ($output), not clobbering, exiting"
  exit 1
fi

# initialize database

sqlite3 "$output" < init.sql

# organisciak names

wget https://github.com/organisciak/names/raw/master/data/us-names-by-gender.csv -O /tmp/us-names-by-gender.csv 2>/dev/null

./organisciak/names_by_gender_to_sql.py /tmp/us-names-by-gender.csv | sqlite3 "$output"


# contributed names

./contributed_names/csv_to_sql.py contributed_names/Blatt_1-Tabelle_1.csv | sqlite3 "$output"
./contributed_names/csv_to_sql.py contributed_names/formularantworten_rewrite.csv | sqlite3 "$output"
