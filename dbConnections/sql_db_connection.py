import pyodbc

server = "ONLYNIGHT\SQLEXPRESS"
database = "OnlyNight"

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER=' + server + ';\
                      DATABASE=' + database + ';\
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()
