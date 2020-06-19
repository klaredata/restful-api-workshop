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
        conn.autocommit = True

        cursor = conn.cursor()
        cursor.fast_executemany = True

        return conn, cursor

    @staticmethod
    def row_to_dict(fields: list, values : tuple) -> dict :
        return dict(zip(fields, values))

    @staticmethod
    def convert_object_to_rows(json_object, type_list) -> list :
        if type(json_object) == dict : 
            return [ PyodbcUtils.convert_object_to_single_row(json_object, type_list) ]
        elif type(json_object) == list : 
            return [ PyodbcUtils.convert_object_to_single_row(x, type_list) for x in json_object ]
        
        raise Exception("Cannot convert object to SQL rows.")

    @staticmethod
    def convert_object_to_single_row(json_dict: dict, type_list) -> list :
        if type(json_dict) != dict : 
            raise Exception("Cennot convert object to SQL row: it is not a dict.")
        
        l = []

        for (field, field_type) in type_list : 
            if field not in json_dict : 
                raise Exception(f"Cannot convert object to SQL row: cannot find field {field}")
            if type(json_dict[field]) != field_type : 
                raise Exception(f"Cannot convert object to SQL row: field {field} is not of the appropriate type.")
            l.append(json_dict[field])
        
        return l