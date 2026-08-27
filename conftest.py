import mysql.connector
import config




def get_test_db_connection():
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database="pos_test_db"  # Use a separate test database
    )
    return connection