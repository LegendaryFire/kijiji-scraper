import sqlite3


class Database:
    def __init__(self, filename="default.db"):
        self.__connection = sqlite3.connect(filename)
        self.__cursor = self.__connection.cursor()
        try:
            self.__cursor.execute("SELECT * FROM listing_data")
        except sqlite3.OperationalError:
            self.__init_database()

    def add_listing(self):
        pass

    def __init_database(self):
        """
        Initialize a new SQLite database. Creates the necessary tables for this application.
        :return: Returns none.
        """
        self.__cursor.execute("CREATE TABLE listing_data ("
                              "id INTEGER NOT NULL PRIMARY KEY,"
                              "title TEXT NOT NULL,"
                              "description TEXT NOT NULL,"
                              "price INTEGER NOT NULL"
                              ")")
        self.__cursor.close()
        pass
