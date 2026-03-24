import mysql.connector

__cnx = None

def get_sql_connection():
    global __cnx

    if __cnx is None:
        print("Opening MySQL connection...")
        __cnx = mysql.connector.connect(
            host="localhost",   # IMPORTANT
            user="root",
            password="root",    # change if needed
            database="grocery_store"
        )

    return __cnx