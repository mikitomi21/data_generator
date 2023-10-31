import pyodbc

database_connection_string = 'DRIVER={SQL Server Native Client 11.0};SERVER=L340;DATABASE=AKCJE_STRAZY_POZARNEJ;Trusted_Connection=yes;'
connection = pyodbc.connect(database_connection_string)
db_cursor = connection.cursor()

dropQueries = ["exec sp_MSforeachtable \"declare @name nvarchar(max); set @name = parsename('?', 1); exec sp_MSdropconstraints @name\"",
               "exec sp_MSforeachtable \"drop table ?\""]

with open("akcje_strazy_pozarnej.sql", 'r') as file:
    createQueries = file.read().split(';')

try:
    for query in dropQueries:
        db_cursor.execute(query)
        connection.commit()

    print("Database tables cleared.")

    for query in createQueries:
        if query.strip(): 
            db_cursor.execute(query)
            connection.commit()
    print("Database recreated.")

except Exception as e:
    print("Error: ", e)
finally:
    connection.close()