import sqlite3


db_conn = sqlite3.connect('smartfactory.db')
db_cursor = db_conn.cursor()
db_cursor.execute("create table if not exists sf (subject text, content_time REAL)")
db_cursor.execute("INSERT INTO sf VALUES (?, ?)", ('stop', 123))
db_conn.commit()




db_cursor.execute('select * from sf')
for row in db_cursor:
    print(row)
    
db_conn.close()