import mysql.connector.pooling

dbconfig = {
    "user": "root",
    "password": "12345678",
    "host": "localhost",

}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=20, **dbconfig)
cnx1 = connection_pool.get_connection()
cnx2 = connection_pool.get_connection()
create_db_query = "INSERT personal_information(id) VALUES (5);"
show_db_query = "USE msutndr"
s = "SELECT * FROM personal_information LIMIT 10"

with cnx1.cursor() as cursor:
    cursor.execute(show_db_query)
    insert_stmt = (
        "INSERT personal_information(id)"
        "VALUES (%s)"
    )
    data = (2,)
    cursor.execute(insert_stmt, data)
    cursor.execute(s)
    result_set = cursor.fetchall()
    # Do something with the result set
    print(*result_set)
    cnx1.commit()
