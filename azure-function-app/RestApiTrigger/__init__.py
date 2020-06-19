import logging
import pyodbc
import json
import azure.functions as func

from __app__.shared.database.database_credentials import DatabaseCredentials                   # pylint: disable=import-error
from __app__.shared.database.database_credentials_reader import DatabaseCredentialsReader      # pylint: disable=import-error
from __app__.shared.database.pyodbc_utils import PyodbcUtils                                   # pylint: disable=import-error

def main(req: func.HttpRequest) -> func.HttpResponse:    
    
    logging.info(str(req.method))
    logging.info(str(req.headers))
    logging.info(str(req.get_body()))
    logging.info(str(req.get_json()))
    logging.info(str(req.route_params))
    
    # Read credentials to connect to the database. 
    # When developing locally, use the JSON file.
    # When running on Functions, use the environment variables. 
    reader = DatabaseCredentialsReader()
    creds = reader.discover_credentials('db_credentials.json')

    conn, cursor = PyodbcUtils.create_connection(creds)
    cursor.execute("SELECT * FROM Consultants")

    if req.method == "GET":

        # There shoudld be no ConsultantId identifier. 


        list_results = []
        for row in cursor.fetchall():
            list_results.append(PyodbcUtils.row_to_dict(('ConsultantId', 'FirstName', 'LastName', 'Email', 'Catchphrase', 'JobTitle'), row))
        
        jsonString = json.dumps(list_results)    

        response = func.HttpResponse(mimetype="application/json", body=jsonString)
        return response
    else :
    #if req.method == "POST":
        return func.HttpResponse("bla")
