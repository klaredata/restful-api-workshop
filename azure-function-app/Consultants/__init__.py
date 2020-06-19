import logging
import pyodbc
import json
import azure.functions as func

from __app__.shared.database.database_credentials import DatabaseCredentials                   # pylint: disable=import-error
from __app__.shared.database.database_credentials_reader import DatabaseCredentialsReader      # pylint: disable=import-error
from __app__.shared.database.pyodbc_utils import PyodbcUtils                                   # pylint: disable=import-error

def main(req: func.HttpRequest) -> func.HttpResponse:    
    
    #logging.info(str(req.method))
    #logging.info(str(req.headers))
    #logging.info("Body: '" + str(req.get_body().decode('UTF-8')) + "'")
    #logging.info(str(req.get_json()))
    #logging.info(str(req.route_params))
    
    # Read credentials to connect to the database. 
    # When developing locally, use the JSON file.
    # When running on Functions, use the environment variables. 
    reader = DatabaseCredentialsReader()
    creds = reader.discover_credentials('db_credentials.json')

    conn, cursor = PyodbcUtils.create_connection(creds)
    cursor.execute("SELECT * FROM Consultants")

    if req.method == "GET":
        # Check that body is empty. 
        if not is_body_empty(req) : 
            return func.HttpResponse(status_code=400, body="Bad request: body should be empty.", )

        list_results = []
        for row in cursor.fetchall():
            list_results.append(PyodbcUtils.row_to_dict(('ConsultantId', 'FirstName', 'LastName', 'Email', 'Catchphrase', 'JobTitle'), row))
        
        json_string = json.dumps(list_results)    

        return func.HttpResponse(mimetype="application/json", body=json_string)
        
    elif req.method == "POST":
        try : 
            json_object = req.get_json()
        except : 
            return func.HttpResponse(status_code=400, body="Bad request: cannot parse JSON.")

        type_list = ( ("ConsultantId", int), ("FirstName", str), ("LastName", str), \
            ("Email", str), ("Catchphrase", str), ("JobTitle", str) )

        prep_sql_statement = "INSERT INTO Consultants VALUES (?, ?, ?, ?, ?, ?)"
        rows = PyodbcUtils.convert_object_to_rows(json_object, type_list)

        try : 
            cursor.executemany(prep_sql_statement, rows)
            return func.HttpResponse(status_code=200)
        except Exception: 
            conn.rollback()

        return func.HttpResponse(status_code=400, body="Bad request: could not fulfill database operation.")

    elif req.method == "PUT":
        return func.HttpResponse("bla")

        # Goed: return 200 plus resultaat van de operatie. 
        # Fout: 400. 


    elif req.method == "DELETE":
        return func.HttpResponse("bla")

        # Goed: return 200, geen resultaat. 
        # Fout: 400. 


    else : 
        return func.HttpResponse(status_code=400, body="Bad request: illegal HTTP method.")

def is_body_empty (req: func.HttpRequest) -> bool : 
    return req.get_body().decode('UTF-8').strip() == ""