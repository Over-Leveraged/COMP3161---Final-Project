import mysql.connector
from app import app


## CHANGE THIS TO YOUR USERNAME AND PASSWORD

def databaseConnection():
    try:
        conn = mysql.connector.connectmydb = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="course_system"
)
        print("Database connection successful")
        return conn
    except mysql.connector.Error as error:
        print("Error connecting to database: {}".format(error))

