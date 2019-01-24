import configparser
config = configparser.ConfigParser()
config.read(("flaskapp-config-1.ini"))

print(config['DEFAULT']['MYSQL_HOST'])
print(config['DEFAULT']['MYSQL_USER'])
print(config['DEFAULT']['MYSQL_PASSWORD'])
print(config['DEFAULT']['MYSQL_DB'])
print(config['DEFAULT']['MYSQL_CURSORCLASS'])
print(config['DEFAULT']['session_secretkey'])
