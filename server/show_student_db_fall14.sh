#!/bin/bash
#


DB="CS535.db"
TBL="CS535_student_table"


echo "SELECT * FROM $TBL ;" | sqlite3 $DB

