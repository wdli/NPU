#!/bin/bash
#


DB="CS535.db"
TBL="CS535_FALL14"


echo "SELECT * FROM $TBL ;" | sqlite3 $DB

