import pyodbc

server = "ONLYNIGHT\SQLEXPRESS"
database = "OnlyNight"

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER=' + server + ';\
                      DATABASE=' + database + ';\
                      Trusted_Connection=yes;')

cursor = conn.cursor()


def exec_stored_procedure(name, values):
    sql = f"EXEC {name} {values}"
    sql = sql.replace("(", "")
    sql = sql.replace(")", "")
    print(sql)
    row_id = cursor.execute(sql).fetchall()[0]
    conn.commit()
    return row_id





