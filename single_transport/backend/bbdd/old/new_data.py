#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")

conn.execute("INSERT INTO node_status (node_id, time, status) \
      VALUES ('17727218', '15:27', 0)");
print ("New data added to table successfully")

conn.commit()
conn.close();
