#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully");


cursor = conn.execute("SELECT * from node_status")
print ("Data in table:\n");
for row in cursor:
   print("node_id = ", row[0])
   print("time = ", row[1])
   print("status = ", row[2])
   print("   ---    ")
   

print("Operation done successfully")
conn.close()