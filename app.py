from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database connection
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'

# Creating the model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    director = db.Column(db.String(40))
    genre = db.Column(db.String(40))

    def __repr__(self):
        return f'Title: {self.title}, year: {self.year} and genre: {self.genre}'


# Adding the routes to the templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies/')
def show_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@app.route('/add-movie/', methods=['POST', 'GET'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        genre = request.form['genre']

        new_movie = Movie(title=title, year=year, director=director, genre=genre)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('show_movies'))
        except:
            return 'There was a message adding this movie'

    else:
        return render_template('add-movie.html')