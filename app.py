from flask import Flask, render_template,  send_from_directory, flash, redirect, url_for, session, logging, request
from make_tree import make_tree # For file trees in a tuple
from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import configparser
import pseudo_diceware
from make_glob_list import make_glob # for listing out files in a folder to pass to WT Forms. REQUIRES PYTHON3
import re
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


@app.route('/')
def index():
    return render_template('home.html')

## Don't currently need an about page.
# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/music')
def music():
    # Route for the music page
    music_list = make_tree("./media")
    return render_template('music.html', tree = music_list)

@app.route('/media/<string:path>')
def media_send(path):
    return send_from_directory('media', path)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1,max=50)])
	email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50), validators.Email(message='Please enter a valid email.')])
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

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        # Get user by Username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                #if  correct password
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else :
                #if password incorrect
                app.logger.info('Valid username. Invalid Password.')
                error = 'Invalid Login'
                return render_template('login.html', error=error)

        else : #username not found
            app.logger.info('No User')
            error = 'Username not found'
            return render_template('login.html', error=error)
        cur.close()
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Produce a dict of previously generated passwords to display in each web page
def retrieve_generated_passwords(n_passwords):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM generated_passwords order by date_created DESC LIMIT %s ;", [n_passwords])
    results = cur.fetchall()
    cur.close()
    return(results)

# Produce list of books to pass to WTFORMS as LIST of value/label TUPLES
# To use the regex capture groups I needed, I had to use re.search instead of re.sub.
def wtform_tuple_creator(func):
    def func_wrapper(folder_path,filetype):
        list_of_paths=func(folder_path,filetype)
        list_of_path_tuples = []
        for file_path in list_of_paths:
            filename = re.search('[^\/]*\.'+filetype,file_path).group(0)
            list_of_path_tuples.append((
            file_path,
            filename
            ))
        return(list_of_path_tuples)
    return(func_wrapper)

#No syntactic sugar with the fancy @ symbols and whatnot
make_glob_list_to_wtforms_tuple = wtform_tuple_creator(make_glob)

# diceware page
class diceware_form(Form):
    book = SelectField('Book', choices = make_glob_list_to_wtforms_tuple('./wordlists','txt')) # where choices is a list of value/label pairs
    n_words = IntegerField('Number of Words',[validators.DataRequired(), validators.NumberRange(min=1, max=20, message='Please enter an integer between 1 and 20.')], default=7)

@app.route('/diceware', methods=['GET', 'POST'])
def diceware():
    form = diceware_form(request.form)
    # if submitting a request to the diceware form
    if request.method == 'POST' and form.validate():
        # Do stuff if post request is made
        book_path = form.book.data
        n_words = form.n_words.data
        diceware_passphrase = " ".join(pseudo_diceware.main(book_path, n_words))
        flash(diceware_passphrase, 'success')

        client_ip = request.environ['REMOTE_ADDR']
        user_agent = request.user_agent.string
        book_used = form.book.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        cur.execute("INSERT INTO generated_passwords(ip_address, browser_info, generated_password, book) VALUES(%s,%s,%s,%s)",(client_ip, user_agent, diceware_passphrase, book_used))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

    ####
    #### Retrieve previously generated passwrods to tabulate on the page.
    ####
    dict_of_passphrase_tuples = retrieve_generated_passwords(100)
    #app.logger.info(dict_of_passphrase_tuples)
    return render_template('diceware.html', form=form, dict_of_tuples=dict_of_passphrase_tuples)

@app.route('/password_list')
def password_list():
    ####
    #### Retrieve previously generated passwrods to tabulate on the page.
    ####
    dict_of_passphrase_tuples = retrieve_generated_passwords(100)
    app.logger.info(dict_of_passphrase_tuples)
    return render_template('password_list.html', dict_of_tuples=dict_of_passphrase_tuples)
# Initialization at runtime from command line
if __name__ == '__main__':

	app.secret_key=imported_config['DEFAULT']['session_secretkey']
	app.run(debug=True)
