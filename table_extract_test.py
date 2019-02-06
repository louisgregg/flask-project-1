import MySQLdb

import configparser
imported_config = configparser.ConfigParser()
imported_config.read(("flaskapp-config-1.ini"))

# Connect
db = MySQLdb.connect(host=imported_config['DEFAULT']['MYSQL_HOST'],
                     user=imported_config['DEFAULT']['MYSQL_USER'],
                     passwd=imported_config['DEFAULT']['MYSQL_PASSWORD'],
                     db=imported_config['DEFAULT']['MYSQL_DB'])

# db = MySQLdb.connect(host=imported_config['DEFAULT']['MYSQL_HOST'],
#                      user=imported_config['DEFAULT']['MYSQL_USER'],
#                      passwd=imported_config['DEFAULT']['MYSQL_PASSWORD'],
#                      db=imported_config['DEFAULT']['MYSQL_DB'],
#                      cursorclass = imported_config['DEFAULT']['MYSQL_CURSORCLASS'])

# Produce a dict of previously generated passwords to display in each web page
def retrieve_generated_passwords(n_passwords):
    cur = db.cursor()
    cur.execute("SELECT * FROM generated_passwords LIMIT %s ;", [n_passwords])
    results = cur.fetchall()
    cur.close()
    return(results)

print(retrieve_generated_passwords(1))
