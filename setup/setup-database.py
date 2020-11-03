#!/usr/bin/env python3
import mysql.connector
from tqdm import tqdm

DEBUG = True
DB_NAME = "automationdb"
cnx = mysql.connector.connect(host='127.0.0.1', user='root',)
cursor = cnx.cursor(dictionary=True)
try:
    cursor.execute(f"DROP DATABASE {DB_NAME};")
    if DEBUG:
        print(f"Successfully dropped database {DB_NAME}.")
except mysql.connector.Error as err:
    pass
try:
    cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8';")
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)
if DEBUG:
    print(f"Successfully created database {DB_NAME}.")
cursor.close()
cnx.close()
cnx = mysql.connector.connect(host='127.0.0.1', database=DB_NAME, user='root', )
cnx.autocommit = True
cursor = cnx.cursor(dictionary=True)

with open("create-db-structure.sql") as fp:
    sql_query = fp.read()
length = len(sql_query.split(";\n"))
print(f"Applying {length} structure queries to database.")
pbar = tqdm(total=length, leave=False)
try:
    for result in cnx.cmd_query_iter(sql_query):
        pbar.update(1)
except mysql.connector.Error as err:
    pbar.close()
    print(f"Failed creating database structure: {err}")
    exit(1)
pbar.close()
if DEBUG:
    print(f"Successfully created database structure.")

with open("create-db-data.sql") as fp:
    sql_query = fp.read()
length = len(sql_query.split(";\n"))
print(f"Applying {length} data insert queries to database.")
pbar = tqdm(total=length, leave=False)
try:
    for result in cnx.cmd_query_iter(sql_query):
        pbar.update(1)
except mysql.connector.Error as err:
    pbar.close()
    print(f"Failed creating database data: {err}")
    exit(1)
pbar.close()
if DEBUG:
    print(f"Successfully created database data.")

cursor.close()
cnx.close()
print("Finished creating database.")
exit()
