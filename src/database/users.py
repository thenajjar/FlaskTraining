import psycopg2
from src.database.db_config import db_config


class users_db_class(object):
    """A postgres database class to create, store, and get data of users database
    """

    def __init__(self):
        # Create users table in the database if it doesn't exists
        try:
            self.create_table()
        except Exception:
            pass

    def create_table(self):
        """ create tables in the PostgreSQL database"""
        command = """ CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL
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
            cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception("Failed to create database")
        finally:
            if conn is not None:
                conn.close()

    def create_user(self, new_name, new_username, new_email, new_phone, new_password):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO users (name, username, email, password, phone)
                VALUES(%s, %s, %s, %s, %s)
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
                      new_password, new_phone)
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
            if conn is not None:
                conn.close()

        return user_id

    def get_user(self, user_id):
        """ insert a new vendor into the vendors table """
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
            # execute the INSERT statement
            cur.execute(sql, user_id)
            # get the generated id back
            value = cur.fetchone()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error_message:
            raise Exception("500", "SERVER_FAILURE",
                            "Failed to get user data from database.", error_message)
        finally:
            if conn is not None:
                conn.close()
        if value:
            return value
        else:
            raise Exception("404", "NOT_FOUND",
                            "User is not found.", "")

    def exists(self, key, value):
        """ insert a new vendor into the vendors table """
        sql = """SELECT 1 from users WHERE {} = %s;""".format(key)
        conn = None
        try:
            # read database configuration
            params = db_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
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
            if conn is not None:
                conn.close()


try:
    users_db = users_db_class()
except Exception as error:
    raise SystemExit(error)
