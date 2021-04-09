# install mysql
# pip install mysql-connector-python
from mysql.connector import errorcode
import mysql.connector


config = {
  'host': 'localhost',
  'database': 'wordfinder_corpora',
  'user': 'user',
  'password': 'project',
  'raise_on_warnings': True
}
try:
  cnx = mysql.connector.connect(**config)
  if cnx.is_connected():
    print('Connected to MySQL database')

  mycursor = cnx.cursor()
  #mycursor.execute('CREATE DATABASE wordfinder_corpora')
  mycursor.execute('SHOW DATABASES')

  for db in mycursor:
    print(db)


  #mycursor.execute('CREATE TABLE english (text VARCHAR(255))')
  #mycursor.execute('CREATE TABLE latin (text VARCHAR(255))')
  #mycursor.execute('CREATE TABLE french (text VARCHAR(255))')
  mycursor.execute('SHOW TABLES')
  for tb in mycursor:
    print(tb)


except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()



