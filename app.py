from flask import Flask, render_template,  send_from_directory
from make_tree import make_tree
app =Flask(__name__)

music_list = make_tree("./media")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/music')
def music():
    return render_template('music.html', tree = music_list)

@app.route('/media/<string:path>')
def media_send(path):
    return send_from_directory('media', path)

if __name__ == '__main__':
    app.run(debug=True)
