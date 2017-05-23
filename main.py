from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import itertools
from werkzeug import secure_filename
import os
import json
import glob
from collections import OrderedDict



app = Flask(__name__)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['json'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



# returns the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("database/" + "movies.db")
    movies = list(itertools.chain.from_iterable
                  (conn.execute("SELECT Image from Movies where Mood = 'nocontent'")))
    names = list(itertools.chain.from_iterable
                 (conn.execute("SELECT Name from Movies where Mood = 'nocontent'")))
    if request.method == 'POST':
        slider1 = request.form['range1']
        slider2 = request.form['range2']
        slider3 = request.form['range3']
        slider4 = request.form['range4']
        print(slider1, slider2, slider3, slider4)
        # calm
        if int(slider1) > 1:
            print("calm")
            movies = list(itertools.chain.from_iterable
                               (conn.execute("SELECT Image from Movies where Mood = 'calm'")))
            names = list(itertools.chain.from_iterable
                               (conn.execute("SELECT Name from Movies where Mood = 'calm'")))
            print(movies)
            print(names)
            return render_template('index.html', movies=movies, names=names)
        # agitated
        if int(slider1) < 1:
            print("agitated")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'agitated'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'agitated'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # sad
        if int(slider2) > 1:
            print("sad")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'sad'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'sad'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # happy
        if int(slider2) < 1:
            print("happy")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'happy'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'happy'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # wideawake
        if int(slider3) > 1:
            print("wideawake")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'wideawake'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'wideawake'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # tired
        if int(slider3) < 1:
            print("tired")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'tired'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'tired'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # fearless
        if int(slider4) > 1:
            print("fearless")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'fearless'")))
            names = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Name from Movies where Mood = 'fearless'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
        # scared
        if int(slider4) < 1:
            print("scared")
            movies = list(itertools.chain.from_iterable
                          (conn.execute("SELECT Image from Movies where Mood = 'scared'")))
            names = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Name from Movies where Mood = 'scared'")))
            print(movies)
            return render_template('index.html', movies=movies, names=names)
    return render_template('index.html', movies=movies, names=names)


# returns the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    files = glob.glob('uploads/*')
    for f in files:
        os.remove(f)
    if request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            print(filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open("uploads/" + filename, 'r') as f:
                d = json.load(f, object_pairs_hook=OrderedDict)
                movienames = []
                for row in d:
                    l = []
                    for value in row.values():
                        l.append(value)
                    movienames.append(l)
                print(movienames)
                for movie in movienames:
                    conn = sqlite3.connect("database/" + "movies.db")
                    conn.execute("INSERT INTO Movies VALUES (?,?,?,?)", movie)
                    conn.commit()
                    print("inserted")
            # Redirect the user to the home page
            return redirect(url_for('index'))
    return render_template('upload.html')


# runs the FlaskApp
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
# [END app]
