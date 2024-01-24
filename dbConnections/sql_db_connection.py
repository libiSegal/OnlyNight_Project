import pyodbc

server = "ONLYNIGHT\SQLEXPRESS"
database = "OnlyNight"

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER=' + server + ';\
                      DATABASE=' + database + ';\
                      Trusted_Connection=yes;')

cursor = conn.cursor()


def exec_stored_procedure(name, values):
    """
    Executes stored procedure in sql server
    :param name: the name of the procedure to be executing
    :param values: the values to be stored in the procedure
    :return: the result of the procedure
    """
    sql = f"EXEC {name} {values}"
    sql = sql.replace("(", "")
    sql = sql.replace(")", "")
    print(sql)
    row_id = cursor.execute(sql).fetchall()[0]
    conn.commit()
    return row_id


def exec_view(name):
    """
    Executes view in sql server
    :param name: the name of the view
    :return:the result of the view
    """
    sql = f"SELECT * FROM {name}"
    data = cursor.execute(sql)
    return data


