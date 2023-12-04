#!/usr/bin/python3

import sqlite3
import read_cursor as rc

datab = 'wirepas_mesh_network.db'
conn = sqlite3.connect(datab)
print ("\nOpened database '" + datab + "' successfully");

do=True
while do:
   table = input("\n(type 'exit' for leaving the prompt) \n enter the name of the table: ")  

   if table == "exit":
      print("bye :)")
      do=False
   else:
      try: 
         cursor = conn.execute("SELECT * from "+table)
         rc.print_cursor(cursor, table)

      except:
         print("Table '" + table + "' does not exist or had a problem with imported modules.")


   

conn.close()