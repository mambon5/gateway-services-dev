#!/usr/bin/python3

import sqlite3

datab = 'wirepas_mesh_network.db'
table = input("enter the name of the table to delete: ")
confirm = input("ATTENTION: YOU ARE GOING TO DELETE THE TABLE '" + table + "' FROM THE DATABASE: '" +
datab + "' FOREVER! Are you sure you want to proceed? y/n :" )


conn = sqlite3.connect(datab)
print ("Opened database '" + datab + "' successfully");

if confirm == "y":
    conn.execute('''DROP TABLE '''+table)
    print ("Table " + table + " deleted amb èxit ");
else:
    print("No table deleted, you can return home safe.")

conn.close()