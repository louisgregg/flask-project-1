#!/usr/bin/python
"""
Create tables for the flask project using the config file.
Use of mysqldb outlined here:
https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
Requirements for python-mysql connector outlined here:
https://stackoverflow.com/questions/25865270/how-to-install-python-mysqldb-module-using-pip
Requirements were already met for packages used to connect flask with mysql.
"""

import MySQLdb

import configparser
imported_config = configparser.ConfigParser()
imported_config.read(("flaskapp-config-1.ini"))


# Connect
db = MySQLdb.connect(host=imported_config['DEFAULT']['MYSQL_HOST'],
                     user=imported_config['DEFAULT']['MYSQL_USER'],
                     passwd=imported_config['DEFAULT']['MYSQL_PASSWORD'],
                     db=imported_config['DEFAULT']['MYSQL_DB'])

cursor = db.cursor()

sql_command="create table generated_passwords( id INT(11) auto_increment PRIMARY KEY, ip_address VARCHAR(40), browser_info VARCHAR(1000), generated_password VARCHAR(1000), date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, book VARCHAR(100));"
cursor.execute(sql_command)
db.commit()
sql_command="show fields from generated_passwords;"
cursor.execute(sql_command)

sql_command="create table users(id INT(11) auto_increment PRIMARY KEY, name VARCHAR(100),email varchar(100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
cursor.execute(sql_command)
db.commit()
sql_command="show fields from users;"
cursor.execute(sql_command)
# Close the connection
db.close()
