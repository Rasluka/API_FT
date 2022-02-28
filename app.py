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


# Route and function to the Index page
@app.route('/')
def index():
    return render_template('index.html')

# Showing the list of movies
@app.route('/movies/')
def show_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

# Adding movies
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

# Delete route and function
@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = Movie.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('show_movies'))
    except:
        return 'We could not delete the movie!'

# Update route and function
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update_movie(id):
    movie_to_update = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie_to_update.title = request.form['title']
        movie_to_update.year = request.form['year']
        movie_to_update.director = request.form['director']
        movie_to_update.genre = request.form['genre']

        try:
            db.session.commit()
            return redirect(url_for('show_movies'))
        except:
            return 'We could not uptate the movie!'
    else:
        return render_template('update-movie.html', movie=movie_to_update)