import mysql.connector.pooling

dbconfig = {
    "user": "root",
    "password": "12345678",
    "host": "localhost",

}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 20,
                                                      **dbconfig)
cnx1 = cnxpool.get_connection()
cnx2 = cnxpool.get_connection()
create_db_query = "SHOW DATABASES"
show_db_query = "SHOW DATABASES"
with cnx1.cursor() as cursor:
    cursor.execute(show_db_query)
    for db in cursor:
        print(db)