import psycopg2
from src.database.db_config import db_config


def create_table():
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
        raise Exception(error)
    finally:
        if conn is not None:
            conn.close()


def create_user(new_name, new_username, new_email, new_phone, new_password):
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
        values = (new_name, new_username, new_email, new_password, new_phone)
        cur.execute(sql, values)
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise Exception(error)
    finally:
        if conn is not None:
            conn.close()

    return user_id


def get_user(user_id):
    """ insert a new vendor into the vendors table """
    sql = """SELECT * from users WHERE user_id = {};""".format(int(user_id))
    conn = None
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
        if value:
            return value
        else:
            error_message = "User is not found"
            raise Exception(error_message)
    except (Exception, psycopg2.DatabaseError) as error_message:
        raise Exception(error_message)
    finally:
        if conn is not None:
            conn.close()


def db_value_exists(key, value):
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
        raise Exception(error_message)
    finally:
        if conn is not None:
            conn.close()
