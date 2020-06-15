#there's a long winded explanation to how to install psycopg2
import psycopg2

#we have a database named example, so let's just connect to it!
#I actually haven't made one called example, so i just did createdb example
connection = psycopg2.connect('dbname=example')

#To queue up work in our database, we need to interact w/a cursor
cursor = connection.cursor()

#delete the table if it already exists
cursor.execute('DROP TABLE IF EXISTS table2;')

#triple quote lets me have a multi line command weow
#'cursor' executes the following line in the database
cursor.execute('''
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    )
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))
#Remember the transaction stuff - the above executes are both part of the transaction
#We then need to 'commit' it to send the work in

data = {
    'id': 2,
    'completed': False
}

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

cursor.execute(SQL, data)

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (3, True))



#basic SQL command to fetch
 
cursor.execute('SELECT * from table2;')

#fetch all the data
result = cursor.fetchall()
print(result)
result2 = cursor.fetchone()
print(result2)
#nothing gets printed from result2, as all the data has already been fetched

connection.commit()

#remember to close the connection after starting them (for both connection and cursor)
connection.close()
cursor.close()

#To run this script, do python3 -/directory/demo.py
#After you run the demo.py, you go into terminal and go into the database
#i.e. psql example