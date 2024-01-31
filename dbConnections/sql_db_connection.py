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


def exec_function(function_name, *args):
    val = args
    print(val)
    sql = f"SELECT * FROM {function_name}{args}"
    print(sql)
    data = cursor.execute(sql)
    return data


def exec_query(ids):
    string_ids = str(ids).replace("[", "").replace("]", "")
    sql = f"""SELECT 
              rooms.ID, rooms.Hotel_id, rooms.Price, rooms.Description, 
              rooms.Sys_code, rooms.Check_in, rooms.Check_out, rooms.Nights, 
              rooms.BToken, rooms.Limit_date,rooms.Remarks,
              metadata.Code, metadata.Description
              FROM rooms 
             JOIN metadata ON metadata.Room_ID = rooms.ID
             WHERE rooms.ID IN ({string_ids})"""
    data = cursor.execute(sql).fetchall()
    return data


def exec_select_hotel_data_query(ids):
    string_ids = str(ids).replace("[", "").replace("]", "")
    sql = f"""SELECT hotels.ID, hotels.Name, hotels.Code, hotels.Stars,
                addressesInfo.Address, addressesInfo.City, addressesInfo.Country,addressesInfo.Phone, addressesInfo.Fax,
                positions.Latitude, positions.Longitude, positions.Pip,
				images.Description, images.Img
                FROM hotels 
                JOIN addressesInfo ON addressesInfo.ID = Address_id 
                JOIN positions ON positions.ID = Position_id
				JOIN images ON images.Hotel_id = hotels.ID
                WHERE hotels.ID IN ({string_ids})"""
    data = cursor.execute(sql).fetchall()
    return data
