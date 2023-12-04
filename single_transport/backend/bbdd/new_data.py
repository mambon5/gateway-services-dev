#!/usr/bin/python3

import sqlite3

datab = 'test-time-series.db'

conn = sqlite3.connect(datab)
print ("Opened database successfully")


# conn.execute("INSERT INTO node_status (node_id, time, status) \
#       VALUES ('17727218', '15:27', 0)");

try: 
# check if table is there 
      conn.execute('''SELECT * FROM node_status
         LIMIT 1;''')
# if it succeeds, table exists

#now if table doesn't exist, create it:
except:
      conn.execute('''CREATE TABLE node_status
         (node_id TEXT      NOT NULL,
         time           TEXT     NOT NULL,
         node_counter INT NOT NULL,
         primary key (node_id, time));''')
      print("Table created successfully")

#write data to table
row=[('17127218', '15:17', -10)]
conn.executemany("INSERT INTO node_status (node_id, time, node_counter) \
      VALUES (?,?,?)",row);
print ("New data added to table successfully")

conn.commit()
conn.close();
