class DatabaseCredentials :

    def __init__(self, server, database, username, password) :
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def __repr__(self) :
        return f"{self.server};{self.database};{self.username};********"