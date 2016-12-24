import mysql.connector
import sys

from log import log_main

log = log_main.Log(100, "log/database_log.txt")


class Database(object):
    """
    This class serves as a database template
    """

    __password = ""
    __username = ""
    __database = ""

    def __init__(self):

        self.set_password()

        try:

            self.cnx = mysql.connector.connect(user=self.__username, password=self.__password,
                                          host='127.0.0.1',
                                          database=self.__database)
        except Exception as e:

            log.err("Database","Error while starting database",e)

        log.inf("Database", "MySQL database started.")

    def set_password(self): # Copys password, username and database name from a file named info.
                           # The file should be created before using the class.

        try:

            text_file = open("/opt/sql/http_server_1", "r")

        except Exception as e:

            log.err("Database","Error while reading file 'info.txt' ",e)

        self.__password = text_file.readline().rstrip('\n')
        self.__username = text_file.readline().rstrip('\n')
        self.__database = text_file.readline().rstrip('\n')

    def check_connection(self): # Check if connection is down, reconnects if true.

        if(not self.cnx.is_connected()):
            self.cnx.reconnect()

    def handle_close(evt): # Termination clean up

        evt.cnx.disconnect()
        evt.cnx.shutdown()
        log.inf("Database", "Database terminated.")
        sys.exit(0)

    def insert_file(self,file_name, file_path, file_type):

        self.check_connection()

        data = list()

        try:

            data = (str(file_name), str(file_path), str(file_type))

        except Exception as e:
            log.bug("Database","Unable to convert values",e)
            raise Exception('Input proper values.')

        cursor = self.cnx.cursor()

        try:

            cursor.execute('INSERT INTO files(file_name, file_path, file_type) VALUE(%s,%s,%s)', data)

            self.cnx.commit()

        except Exception as e:
            log.bug("Database","Error while inserting >" + str(data) + "< into database",e)
            raise Exception('Unable to save to database.')

        cursor.execute("SELECT LAST_INSERT_ID()")
        return_id = cursor.fetchone()[0]

        data = []

        return return_id


    def fetch_files(self):

        self.check_connection()

        cursor = self.cnx.cursor()

        try:

            cursor.execute("SELECT id, date, file_name, file_path, file_type FROM files")

        except Exception as e:

            log.err("Database","Error while fetching from database",e)

        return_list = list()

        for (id, date, file_name, file_path, file_type) in cursor:

            return_dict = dict()

            return_dict["id"] = id
            return_dict["date"] = date
            return_dict["file_name"] = file_name
            return_dict["file_path"] = file_path
            return_dict["file_type"] = file_type

            return_list.append(return_dict)

        return return_list


    def remove_file(self,id):

        self.check_connection()

        data = []

        try:

            data.append(int(id))

        except Exception as e:
            log.bug("Database", "Unable to convert values", e)
            raise Exception('Input proper values.')

        cursor = self.cnx.cursor()

        try:
            cursor.execute("DELETE FROM files WHERE id = %s", data)
            self.cnx.commit()

        except Exception as e:
            log.err("Database", "Error while deleting data from database", e)

        return cursor.rowcount >= 1

    def insert_note(self, message):

        self.check_connection()

        data = list()

        try:

            data = (str(message),)

        except Exception as e:
            log.bug("Database", "Unable to convert values", e)
            raise Exception('Input proper values.')

        cursor = self.cnx.cursor()

        try:

            cursor.execute('INSERT INTO notes(message) VALUE(%s)', data)

            self.cnx.commit()

        except Exception as e:
            log.bug("Database", "Error while inserting >" + str(data) + "< into database", e)
            raise Exception('Unable to save to database.')

        cursor.execute("SELECT LAST_INSERT_ID()")
        return_id = cursor.fetchone()[0]

        data = []

        return return_id

    def fetch_notes(self):

        self.check_connection()

        cursor = self.cnx.cursor()

        try:

            cursor.execute("SELECT id, date, message FROM notes")

        except Exception as e:

            log.err("Database", "Error while fetching from database", e)

        return_list = list()

        for (id, date, message) in cursor:
            return_dict = dict()

            return_dict["id"] = id
            return_dict["date"] = date
            return_dict["message"] = message

            return_list.append(return_dict)

        return return_list

    def remove_note(self, id):

        self.check_connection()

        data = []

        try:

            data.append(int(id))

        except Exception as e:
            log.bug("Database", "Unable to convert values", e)
            raise Exception('Input proper values.')

        cursor = self.cnx.cursor()

        try:
            cursor.execute("DELETE FROM notes WHERE id = %s", data)
            self.cnx.commit()

        except Exception as e:
            log.err("Database", "Error while deleting data from database", e)

        return cursor.rowcount >= 1