import logging
import pyodbc
import os
import azure.functions as func

from __app__.shared.database.database_credentials import DatabaseCredentials
from __app__.shared.database.database_credentials_reader import DatabaseCredentialsReader

def main(req: func.HttpRequest) -> func.HttpResponse:    
    logging.info(str(req.headers))
    logging.info(str(req.get_body()))
    logging.info(str(req.get_json()))

    reader = DatabaseCredentialsReader()

    logging.info(str(os.listdir()))

    os.environ['server'] = 'aaa'
    os.environ['database'] = 'bbb'
    os.environ['username'] = 'ccc'
    os.environ['password'] = 'aaddda'

    creds = reader.discover_credentials('db_credentials.json')

    return func.HttpResponse(str(creds))
