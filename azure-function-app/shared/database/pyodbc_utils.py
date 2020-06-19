import pyodbc
from .database_credentials import DatabaseCredentials

class PyodbcUtils :
    """ Static class with helper function to ease setting up a connection to the database. 
    """

    @staticmethod
    def create_connection(creds: DatabaseCredentials) -> (pyodbc.Connection, pyodbc.Cursor) :
        connection_string = 'DRIVER={SQL Server};' + f"SERVER={creds.server},1433'"
        
        conn = pyodbc.connect(connection_string, database = creds.database, \
            user = creds.username, password = creds.password)

        cursor = conn.cursor()

        return conn, cursor

    @staticmethod
    def row_to_dict(fields: list, values : tuple) -> dict :
        return dict(zip(fields, values))

