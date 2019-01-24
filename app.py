from flask import Flask, render_template,  send_from_directory, flash, redirect, url_for, session, logging, request
from make_tree import make_tree
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import configparser

# Import variables from the config file.
imported_config = configparser.ConfigParser()
imported_config.read(("flaskapp-config-1.ini"))


app =Flask(__name__)

# MySQL config imported from the config file values.
app.config['MYSQL_HOST'] = imported_config['DEFAULT']['MYSQL_HOST']
app.config['MYSQL_USER'] = imported_config['DEFAULT']['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = imported_config['DEFAULT']['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = imported_config['DEFAULT']['MYSQL_DB']
#Default class returned is a tuple. This project uses dict instead.
app.config['MYSQL_CURSORCLASS'] = imported_config['DEFAULT']['MYSQL_CURSORCLASS']

#Initialize MYSQL
mysql=MySQL(app)

# Route for the music page
music_list = make_tree("./media")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/music')
def music():
    return render_template('music.html', tree = music_list)

@app.route('/media/<string:path>')
def media_send(path):
    return send_from_directory('media', path)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1,max=50)])
	email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
	username= StringField('Username', [validators.DataRequired(), validators.Length(min=4,max=25)])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match.')])
	confirm = PasswordField('Comfirm Password',[validators.DataRequired()])

@app.route('/register', methods=['GET', 'POST'] )
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		# Do stuff if post request is made
		name=form.name.data
		email=form.email.data
		username=form.username.data
		"""
		THe password variable being filled below is in fact the concatination of a salt generated once and the hash of this salt with the password supplied by the user. This hash string is pushed to the MySQL DB.
		I changed this to sha256_crypt.hash from sha256_crypt.encrypt as it was deprecated.
		"""
		password=sha256_crypt.hash(str(form.password.data))

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('You are now registered and can log in', 'success')

		return redirect(url_for('login'))
	return render_template('register.html', form=form)

if __name__ == '__main__':
    
	app.secret_key=imported_config['DEFAULT']['session_secretkey']
	app.run(debug=True)
