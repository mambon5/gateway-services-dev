#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE node_status
         (node_id TEXT      NOT NULL,
         time           TEXT     NOT NULL,
         status INT    NOT NULL,
         primary key (node_id, time));''')
print("Table created successfully")


cursor = conn.execute("SELECT node_id, time, status from node_status")
for row in cursor:
   print("node_id = ", row[0])
   print("time = ", row[1])
   print("status = ", row[2])
   

print("Operation done successfully")
conn.close()