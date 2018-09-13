from flask import Flask,render_template
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)

@app.route('/')
def hello_world():
    conn = sqlite3.connect(os.path.join(BASE_DIR,'movie_site.db'))
    cursor = conn.cursor()
    sql = 'select id,title,cover,director from movie'
    rows = cursor.execute(sql)
    movies = []
    for row in rows:
        # (id,title,cover,director)
        movie = {}
        movie['id'] = row[0]
        movie['title'] = row[1]
        movie['cover'] = row[2]
        movie['director'] = row[3]
        movies.append(movie)
    return render_template('index.html',movies=movies)

@app.route("/detail/")
def detail():
    pass

if __name__ == '__main__':
    app.run()
