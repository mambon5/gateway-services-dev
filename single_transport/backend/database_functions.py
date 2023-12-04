"""
Set of functions that control the interaction from main script to the database.
We have the following functionalities implemented:

1. Modify database values
2. Read database values
"""
# global variables:

# path to gateway database:
# DB_PATH = "/home/roma/smartec/gateway-services/single_transport/backend/bbdd/"
DB_PATH = "bbdd/"
#name of database:
DB_NAME = "wirepas_mesh_network.db"

datab = DB_PATH + DB_NAME

#table names:
TABLE_SUCCESS = "successful_requests"
TABLE_FAILS = "failed_requests"
TABLE_REQUESTS_SENT = "requests_sent"
TABLE_RECEIVED_RESPONSES = "responses_received"



# functions:

def sql_set_values(values, column_names):
    """
    Creates part of the SQL SET statement. In particular, it creates the part of the query
    where each value is matched to its variable like so:

    - variable = value

    :param values: List of values to be sent in the SQL statement
    :type values: list
    :param column_names: List of database variables or column names to be updated
    :type column_names: list

    :return:
        **text** (*string*) -- the part of the SQL statement that does the variable assignation to the values
    """
    text = ""
    first = True
    for val in range(len(values)):

        value = ""
        if first:
            first = False
        else :
            text = text + ", " 
        
        # checking if value is a string, and acting accordingly
        is_a_string = isinstance(values[val], str)
        if is_a_string:
            value = "'" + values[val] + "'"
        else:
            value = str(values[val])
            
        # write the SET part of the query:
        text = text +  column_names[val] + " = " + value
    return text

def get_row_string(row, column_names):
    """
    Displays a row of the database. 

    :param row: a row of values from the database
    :type row: list
    :param column_names: List of database variables or column names that have values in the row
    :type column_names: list

    :return:
        **row_text** (*string*) -- 1 line of text containing the row values and its variable names
    """

    row_text = ""
    for col in range(len(column_names)):
        row_text = row_text + " | " + column_names[col] +" = "+ str(row[col] )
    return row_text

def print_rows(cursor, table_name):
    """
    Prints all rows in a specific table. 

    :param cursor: I don't know what is this parameter tbh
    :type cursor: list?
    :param table_name: Name of the SQL table to print
    :type table_name: string

    :return:
        None
    """
    table = table_name
    column_names = list(map(lambda x: x[0], cursor.description))

    rows_read=0
    print ("\nData in table " + table + ": ")
    print("+---------------------+")
    for row in cursor:
        row_text = get_row_string(row, column_names)
        print(row_text + " |")        
        print("+---------------------+")
        rows_read=rows_read+1

