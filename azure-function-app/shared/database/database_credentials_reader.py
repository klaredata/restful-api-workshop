import logging
import json
import os
import os.path

from .database_credentials import DatabaseCredentials

class DatabaseCredentialsReader :
    """ Tool to discover the credentials of a database server from either
    a JSON file or the environment variables. 
    """

    def __init__(self):
        pass

    def discover_credentials(self, possible_file_location:str = None) -> DatabaseCredentials :
        """ Discovers the credentials of the SQL server to reach. 

        If possible_file_location is filled, the method will try extract the
        info from that JSON file. Otherwise, the environment variables will 
        be searched. 
        """
        
        credentials = None
        
        try : 
            if possible_file_location is not None : 
                credentials = self.__read_credentials_from_file(possible_file_location)
                if credentials is None :
                    logging.info(f"Credentials file not found at: {possible_file_location}. \
                        Fallback to finding the credentials in environment variables.")

            if credentials is None :
                credentials = self.__read_credentials_from_env_vars()        

            if credentials is None : 
                raise Exception("No database credentials found.") 
        except Exception as e :
            logging.error(str(e))
            raise

        return credentials

    def __read_credentials_from_file(self, possible_file_location) : 
        """ Read database credentials from JSON file. Returns None if this 
        task is unsuccessful. 
        """
        if not os.path.exists(possible_file_location) :
            return None
        
        # Read JSON file contents
        with open(possible_file_location, 'r') as possible_file:
            data = possible_file.read()
            
        # Parse to JSON object. 
        try : 
            obj = json.loads(data)
        except :
            return None

        if not self.__json_check_strings(obj, ['server', 'database', 'username', 'password']) :
            return None
        
        return DatabaseCredentials(obj['server'], obj['database'], obj['username'], obj['password'])

    def __json_check_strings(self, obj, key_list) -> bool :
        """ For each element in key_list, perform two checks: 
        - does that key exist in the dictionary? 
        - is the type of the value that is referred to, a string? 

        Returns True if all conditions are met. False otherwise. 
        """
        
        for key in key_list :
            if not key in obj or type(obj[key]) != str :
                return False

        return True

    def __read_credentials_from_env_vars(self): 
        """ Read database credentials from the environment variables. 
        Returns None if the credentials cannot be found. 
        """
        if not self.__env_vars_check_strings(['server', 'database', 'username', 'password']) :
            return None
        
        return DatabaseCredentials(os.environ['server'], os.environ['database'],\
            os.environ['username'], os.environ['password'])


    def __env_vars_check_strings(self, key_list) -> bool: 
        """ Returns True if all keys are present in the environment variables. 
        """
        for key in key_list : 
            if key not in os.environ : 
                return False
        return True
