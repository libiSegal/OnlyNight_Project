import pyodbc

server = "ONLYNIGHT\SQLEXPRESS"
database = "OnlyNight"
username = ""
password = ""
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER=' + server + ';\
                      DATABASE=' + database + ';\
                      UID=' + username + ';\
                      PWD=' + password + ';\
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()
