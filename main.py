from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

# Dictionary to store movie data
movies_data = {}

def load_movies(filename):
    movies = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies.append(row['Title'])
            movies_data[row['Title'].lower()] = {
                'Rating': row['Rating'],
                'Genre': row['Genre'],
                'Release Year': row['Release Year']
            }
    return movies

movies = load_movies('movies.csv')

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/get_rating')
def get_rating():
    movie_name = request.args.get('movie_name', '').lower()
    movie_info = movies_data.get(movie_name)
    
    if movie_info:
        return jsonify({
            'title': movie_name.title(),
            'rating': movie_info['Rating'],
            'genre': movie_info['Genre'],
            'release_year': movie_info['Release Year']
        })
    else:
        # Get suggestions for similar movie titles
        suggestions = [title for title in movies if movie_name in title.lower()][:5]
        return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)