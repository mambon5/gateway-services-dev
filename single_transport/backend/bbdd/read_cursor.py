def print_cursor(cursor, table_name):
    try:
        column_names = list(map(lambda x: x[0], cursor.description))

        rows_read=0
        print ("\nData in table " + table_name + ": ")
        print("+---------------------+")
        for row in cursor:
            row_text = ""
            for col in range(len(column_names)):
                row_text = row_text + " | " + column_names[col] +" = "+ str(row[col] )
            print(row_text + " |")
            
            print("+---------------------+")
            rows_read=rows_read+1

        
        print("\nReading finished. {} entries read succesfully.".format(rows_read))
    except:
        print("cursor not well set")