import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def connect_to_database():
    host = config['Telegram']['host_db']
    user = config['Telegram']['user_db']
    password = config['Telegram']['password_db']
    database = config['Telegram']['db_name']

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn
