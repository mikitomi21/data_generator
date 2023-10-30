import pyodbc
import os
database_connection_string = 'DRIVER={SQL Server Native Client 11.0};SERVER=EWIK;DATABASE=AKCJE_STRAZY_POZARNEJ;Trusted_Connection=yes;'
connection = pyodbc.connect(database_connection_string)
db_cursor = connection.cursor()

tables = ["Akcje",
          "Strazacy",
          "Kierowcy",
          "Remizy",
          "Zespoly",
          "Trasy",
          "Drogi",
          "Przynaleznosc_do_trasy",
          "Przynaleznosc_do_zespolu"]
os.chdir("bulks")
def CreateBulkInsertQuerry(tableName, filename):
    return f"""
    USE AKCJE_STRAZY_POZARNEJ;
    BULK INSERT dbo.{tableName} 
    FROM '{os. getcwd()}\\{filename}' 
    WITH (FIELDTERMINATOR='|');
    """

try:
    for table in tables:
        db_cursor.execute(CreateBulkInsertQuerry(table, table+".bulk"))
        connection.commit()
        print("BULK INSERT completed successfully.")
except Exception as e:
    print("Error during BULK INSERT:", e)
finally:
    connection.close()

exit()