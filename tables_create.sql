use flaskdb1;
create table users(id INT(11) auto_increment PRIMARY KEY, name VARCHAR(100),email varchar(100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
create table generated_passwords(
  id INT(11) auto_increment PRIMARY KEY,
  ip_address VARCHAR(40),
  browser_info VARCHAR(100),
  generated_password VARCHAR(1000),
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
