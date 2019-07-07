#!/home/f/fi/fin/public_html/flasky/venv_3/bin/python3

from flask import Flask, render_template,  send_from_directory, flash, redirect, url_for, session, logging, request
from flask_project_1.make_tree import make_tree # For file trees in a tuple
from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, IntegerField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import configparser
import flask_project_1.pseudo_diceware as p_d
from flask_project_1.make_glob_list import make_glob # for listing out files in a folder to pass to WT Forms. REQUIRES PYTHON3
import re

# Import variables from the config file.
imported_config = configparser.ConfigParser()
imported_config.read(("/home/f/fi/fin/public_html/flasky/flask_project_1/flaskapp-config-1.ini"))

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

#Initialize secret key for session
app.secret_key=imported_config['DEFAULT']['session_secretkey']

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/music')
def music():
    # Route for the music page
    music_list = make_tree("/home/f/fi/fin/public_html/flasky/flask_project_1/media")
    return render_template('music.html', tree = music_list)

@app.route("/media/<string:path>")
def media_send(path):
    return send_from_directory("media", path)

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
    book = SelectField('Book', choices = make_glob_list_to_wtforms_tuple('/home/f/fi/fin/public_html/flasky/flask_project_1//wordlists','txt')) # where choices is a list of value/label pairs
    n_words = IntegerField('Number of Words',[validators.DataRequired(), validators.NumberRange(min=1, max=20, message='Please enter an integer between 1 and 20.')], default=7)

@app.route('/diceware', methods=['GET', 'POST'])
def diceware():
    form = diceware_form(request.form)
    # if submitting a request to the diceware form
    if request.method == 'POST' and form.validate():
        # Do stuff if post request is made
        book_path = form.book.data
        n_words = form.n_words.data
        diceware_passphrase = " ".join(p_d.main(book_path, n_words))
        flash(diceware_passphrase, 'success')

        client_ip = request.environ['REMOTE_ADDR']
        user_agent = request.user_agent.string
        book_used = filename = re.search('[^\/]*\.'+'txt',form.book.data).group(0)
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO generated_passwords(ip_address, browser_info, generated_password, book) VALUES(%s,%s,%s,%s)",(client_ip, user_agent, diceware_passphrase, book_used))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

    #### Retrieve previously generated passwrods to tabulate on the page.
    dict_of_passphrase_tuples = retrieve_generated_passwords(100)
    return render_template('diceware.html', form=form, dict_of_tuples=dict_of_passphrase_tuples)

@app.route('/nlp')
def nlp():
    # Route for the music page
    image_list = make_tree("/home/f/fi/fin/public_html/flasky/flask_project_1/sentiment_images")
    return render_template('twint_nlp.html', tree = image_list)    

@app.route('/sentiment_images/<string:path>')
def sentiment_images_send(path):
    return send_from_directory("sentiment_images", path)

@app.route('/photos/<string:path>')
def photos_send(path):
    return send_from_directory("photos", path)    

@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/uploaded_files/<string:path>')
def key_send(path):
    return send_from_directory("uploaded_files", path)       

# Initialization at runtime from command line
if __name__ == '__main__':
    app.secret_key=imported_config['DEFAULT']['session_secretkey']
    app.run()
