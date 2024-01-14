import mysql.connector
from mysql.connector import Error

sql_db = mysql.connector.connect()

cursor = sql_db

HOST = "sql11.freesqldatabase.com"
USERNAME = "sql11675161"
PASSWORD = "efyMfDZ1Xw"
DATABASE = "sql11675161"


def connect_to_db(host_name, user_name, password, database_name):
    """
      Connect to sql server database
      :param host_name: the host name of the sql server
      :param user_name:username of sql server
      :param password: the password on sql server
      :param database_name:the database name
      :return: the connection to the sql server
      """
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=password,
            database=database_name
        )
        print("MySQL Connection established")
    except Error as err:
        print(f"Error: {err}")
        return err

    return connection


def execute_query(connection, query):
    """
       This function execute queries in the sql db
       :param connection: the connection to the db
       :param query: the query to execute
       :return:the new id
       """
    connection_cursor = connection.cursor(buffered=True)
    try:
        connection_cursor.execute(query)
        connection.commit()
        new_id = connection_cursor.lastrowid
        print("execute the query")
        return new_id
    except Error as err:
        print(f"Error: {err}")
        return err

    finally:
        connection_cursor.close()
        connection.close()


def read_from_db(connection, query):
    """
        This function run read functions on sql
        :param connection: the connection to sql
        :param query:the query to run
        :return: the result of the query
        """
    connection_cursor = connection.cursor(buffered=True)
    try:
        connection_cursor.execute(query)
        result = connection_cursor.fetchall()
        print('Read the query')
        return result
    except Error as err:
        print(f"Error: {err}")
        return err

    finally:
        connection_cursor.close()
        connection.close()


# export the connection outside
db_connection = connect_to_db(HOST, USERNAME, PASSWORD, DATABASE)
