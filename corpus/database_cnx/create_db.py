# install mysql
# pip install mysql-connector-python
import mysql.connector as mariadb
import mariadb
import sys

mariadb_cnx = mariadb.connect(user='zguo4@hopper.slu.edu', password='SJk+6L4K3fKX', database='psd_project', host='db1.mcs.slu.edu', port=3306)

mycursor = mariadb_cnx.cursor(dictionary=True)




