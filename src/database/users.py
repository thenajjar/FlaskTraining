import psycopg2
from src.database.db_config import db_config


class users_db_class:
    """A postgres database class to create, store, and get data of users table in database.
    """

    def __init__(self):
        # Create users table in the database if it doesn't exists
        try:
            self.create_table()
        except Exception:
            pass

    def create_table(self):
        """Create a postgres database table.

        Raises:
            Exception: if it fails to create the database table in postgres
        """
        # The sql command to be executed
        sql = """ CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
            )
            """
        conn = None
        try:
            # read the connection parameters
            params = db_config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            cur.execute(sql)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception("Failed to create database")
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()

    def create_user(self, new_name, new_username, new_email, new_phone, new_password, role):
        """Create new user row in the users table of postgres database.

        Args:
            new_name (str): the first and last name of the user
            new_username (str): the unique username of the user
            new_email (str): unique email to the user
            new_phone (str): user phone number
            new_password (str): user password

        Raises:
            Exception: if it fails to create new user.

        Returns:
            user_id (int): the id of the user in the database table
        """
        # sql comman to execute to create new user
        sql = """INSERT INTO users (name, username, email, password, phone, role)
                VALUES(%s, %s, %s, %s, %s, %s)
                RETURNING user_id;"""
        conn = None
        user_id = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            values = (new_name, new_username, new_email,
                      new_password, new_phone, role)
            cur.execute(sql, values)
            # get the generated id back
            user_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Database failed to create new user.", error_message)
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()

        return user_id

    def get_user(self, user_id):
        """Takes the user_id and returns a josn of the user details

        Args:
            user_id (int): the user_id in the database

        Raises:
            Exception: If the user doesn't exists or if it fails to connect to the database

        Returns:
            tuple: (user_id, name, username, email, password, phone, role)
        """
        # SQL command to fetch the user details by their id
        sql = """SELECT * from users WHERE user_id = {};""".format(
            int(user_id))
        conn = None
        value = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the SELECT SQL statement
            cur.execute(sql, user_id)
            # get a tuple with all the user details
            value = cur.fetchone()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Failed to get user data from database.", error_message)
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()
        if value:
            return value
        else:
            raise Exception("404", "NOT_FOUND",
                            "User is not found.", "")

    def exists(self, key, value):
        """Takes a column key and value and checks if value exists 
        in the column in the users table in the postgres database

        Args:
            key (string): column name in the users table
            value (any): value to check if it exists

        Raises:
            Exception: if it failed to connect to database

        Returns:
            True (boolen): if the user exists
        """
        # SQL command to find the value in a key in the users table
        sql = """SELECT 1 from users WHERE {} = %s;""".format(key)
        conn = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the SELECT statement
            cur.execute(sql, (value,))
            # get the generated id back
            result = cur.fetchall()
            # close communication with the database
            cur.close()
            if result:
                return True
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Server failed to connect to database.", error_message)
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()
    
    
    def get_id(self, key, value):
        """Takes a column key and value and checks if value exists 
        in the column in the users table in the postgres database

        Args:
            key (string): column name in the users table
            value (any): value to check if it exists

        Raises:
            Exception: if it failed to connect to database

        Returns:
            True (boolen): if the user exists
        """
        # SQL command to find the value in a key in the users table
        sql = """SELECT * from users WHERE {} = %s;""".format(key)
        conn = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the SELECT statement
            cur.execute(sql, (value,))
            # get the generated id back
            result = cur.fetchall()[0][0]
            # close communication with the database
            cur.close()
            if result:
                return result
            else:
                raise Exception("404", "NOT_FOUND",
                            str(key) + " Not found.", error_message)
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Server failed to connect to database.", error_message)
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()
    
    def get_role(self, key, value):
        """Takes a column key and value and checks if value exists 
        in the column in the users table in the postgres database

        Args:
            key (string): column name in the users table
            value (any): value to check if it exists

        Raises:
            Exception: if it failed to connect to database

        Returns:
            True (boolen): if the user exists
        """
        # SQL command to find the value in a key in the users table
        sql = """SELECT * from users WHERE {} = %s;""".format(key)
        conn = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the SELECT statement
            cur.execute(sql, (value,))
            # get the generated id back
            result = cur.fetchall()[0][-1]
            # close communication with the database
            cur.close()
            if result:
                return result
            else:
                raise Exception("404", "NOT_FOUND",
                            str(key) + " Not found.", error_message)
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Server failed to connect to database.", error_message)
        finally:
            # close communication if it's still open due to an error
            if conn is not None:
                conn.close()

# try to make a connection to the users table
try:
    users_db = users_db_class()
except Exception as error:
    raise SystemExit(error)
