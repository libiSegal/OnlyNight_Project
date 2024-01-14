import sql_db_connection as db

connection = db.db_connection


def insert_segment(segment_to_insert):
    """
    Check is the segment is not exists and if not insert the segment into the database
    :param segment_to_insert: the segment to insert
    :return:the new id of the segment
    """
    segments = select_column_by_table('SEGMENTS', 'segment')
    if segments is None or not check_if_data_exist(segments, segment_to_insert):
        return insert_segment_into_table(segment_to_insert)
    else:
        print('Segment already exists')
        return Exception('Segment already exists')


def select_column_by_table(table_name, columns):
    """
    Read a specified column from a given table and return it
    :param table_name: the table and to select
    :param columns:the columns to select
    :return:the rows of the column in the specified table
    """
    try:
        query = f'''SELECT {columns} FROM {table_name}'''
        result = db.read_from_db(connection, query)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return Exception(e)


def check_if_data_exist(table_data, value):
    """
    Check if the new value already exists in the sql table
    :param table_data: the table to check
    :param value: the value to check
    :return: True if the value is existing in the table
    """
    for column in table_data:
        if value == column[0]:
            return True
    return False


def insert_segment_into_table(segment_name):
    """
    Insert the segment into the sql table
    :param segment_name: the value to insert
    :return: the id of the new row
    """
    try:
        print('Inserting segment into the table')
        query = f'''INSERT INTO SEGMENTS(segment) VALUES ('{segment_name}')'''
        return db.execute_query(connection, query)
    except Exception as e:
        print(f'Error {e}')
        return Exception(e)


# this function is a temporary function!
def insert_data(table_name, segment_id, year, data):
    query = f'''INSERT INTO {table_name}(segment_id, number_year, ADR ) VALUES ('{segment_id}','{year}','{data}')'''
    db.execute_query(connection, query)
    print(f'Inserted')

# insert_data("SEPTEMBER", 4, 2023, 504)
# insert_segment('New York')
# select_column_by_table('SEPTEMBER', 'ADR')
