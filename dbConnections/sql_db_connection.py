import pyodbc

server = "ONLYNIGHT\SQLEXPRESS"
database = "OnlyNight"

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER=' + server + ';\
                      DATABASE=' + database + ';\
                      Trusted_Connection=yes;')

cursor = conn.cursor()


def exec_stored_procedures(name, values):
    """
    Executes stored procedure in sql server
    :param name: the name of the procedure to be executing
    :param values: the values to be stored in the procedure
    :return: the result of the procedure
    """
    sql = f"EXEC {name} {values}"
    sql = sql.replace("(", "")
    sql = sql.replace(")", "")
    row_id = cursor.execute(sql).fetchall()
    if isinstance(row_id, list) and len(row_id) > 0:
        row_id = row_id
    conn.commit()
    return row_id


def exec_views(name):
    """
    Executes view in sql server
    :param name: the name of the view
    :return:the result of the view
    """
    sql = f"SELECT * FROM {name}"
    data = cursor.execute(sql)
    return data


def exec_query_select_room_prices_by_ids(ids):
    """
    Execute a SQL query to select room price data based on a list of IDs.
    This function builds and executes a SQL query to retrieve specific hotel data based on the provided list of IDs
    :param ids: A list of hotel IDs to select data for
    :return: The data retrieved from the database based on the specified IDs
    """
    string_ids = str(ids).replace("[", "").replace("]", "")
    sql = f"SELECT ID, Price, Check_in FROM rooms WHERE ID IN ({string_ids})"
    return cursor.execute(sql).fetchall()


def exec_query_select_rooms(ids):
    """
    Execute a SQL query to select room data based on a list of IDs.
    This function builds and executes a SQL query to retrieve specific hotel data based on the provided list of IDs
    :param ids: A list of hotel IDs to select data for
    :return:  The data retrieved from the database based on the specified IDs
    """
    string_ids = str(ids).replace("[", "").replace("]", "")
    sql = f"""SELECT 
              rooms.ID, rooms.Hotel_id, rooms.Price, rooms.Description, 
              rooms.Sys_code, rooms.Check_in, rooms.Check_out, rooms.Nights, 
              rooms.BToken, rooms.Limit_date,rooms.Remarks,
              metadata.Code, metadata.Description
              FROM rooms 
             LEFT JOIN metadata ON metadata.Room_ID = rooms.ID
             WHERE rooms.ID IN ({string_ids})"""
    data = cursor.execute(sql).fetchall()

    if data:
        return data
    return []


def exec_query_select_hotel_data(ids):
    """
    Execute a SQL query to select hotel data based on a list of IDs.
    This function builds and executes a SQL query to retrieve specific hotel data based on the provided list of IDs.
    :param ids: A list of hotel IDs to select data for
    :return: The data retrieved from the database based on the specified IDs
    """
    if isinstance(ids, int):
        ids = [ids]
    if isinstance(ids, list):
        if len(ids) > 0:
            string_ids = str(ids).replace("[", "").replace("]", "")
            sql = f"""SELECT hotels.ID, hotels.Name, hotels.Code, hotels.Stars,
                        addressesInfo.Address, addressesInfo.City, addressesInfo.Country,addressesInfo.Phone, addressesInfo.Fax,
                        positions.Latitude, positions.Longitude, positions.Pip,
                        images.Description, images.Img
                        FROM hotels 
                        LEFT JOIN addressesInfo ON addressesInfo.ID = Address_id 
                        LEFT JOIN positions ON positions.ID = Position_id
                        LEFT JOIN images ON images.Hotel_id = hotels.ID
                        WHERE hotels.ID IN ( {string_ids} )"""

            data = cursor.execute(sql).fetchall()

            if data:
                return data

    return []
