import mysql.connector
from mysql.connector import pooling, cursor

# Создание пула соединений
connection_pool = pooling.MySQLConnectionPool(
    pool_name="dating_bot_pool",
    pool_size=5,  # Устанавливаем количество соединений в пуле
    host='localhost',
    database='my_database',
    user='my_user',
    password='my_password'
)


def execute_query(query, params=None):
    connection = connection_pool.get_connection()
    cursor_ = connection.cursor()

    try:
        cursor_.execute(query, params)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Пример использования
query = "SELECT * FROM users WHERE age > %s"
params = (18,)
results = execute_query(query, params)

for row in results:
    print(row)
