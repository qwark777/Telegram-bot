
import mysql.connector.pooling

config = {
    "user": "root",
    "password": "12345678",
    "host": "localhost",
    "database": "msutndr"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=20,
)

connection = connection_pool.get_connection()
cursor = connection.cursor()
cursor.execute("SELECT * FROM mytable")
results = cursor.fetchall()