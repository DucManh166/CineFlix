import os
import pickle
import pandas as pd
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Initialize Flask app and blueprint
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000"]}})
movie_recommender_blueprint = Blueprint('movie_recommender', __name__, url_prefix='/api/movie')

DATA_DIR = "Files"

def get_filepath(filename):
    return os.path.join(app.root_path, DATA_DIR, filename)

class MovieRecommender:
    def __init__(self):
        self.datafile_map = {
            'movies': 'movies_dict.pkl',
            'movies2': 'movies2_dict.pkl',
            'new_df': 'new_df_dict.pkl'
        }
        self.similarity_file_map = {
            'tags': 'similarity_tags.pkl',
            'genres': 'similarity_genres.pkl',
            'keywords': 'similarity_keywords.pkl',
            'cast': 'similarity_tcast.pkl',
            'production_companies': 'similarity_tprduction_comp.pkl'
        }
        self.load_data()
        self.executor = ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_THREADS")))

    def load_data(self):
        self.dataframes = {}
        for df_name, file_name in self.datafile_map.items():
            file_path = get_filepath(file_name)
            try:
                with open(file_path, 'rb') as f:
                    self.dataframes[df_name] = pd.DataFrame.from_dict(pickle.load(f))
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file {file_path} not found. Preprocessing required.")
            except Exception as e:  #Catch other potential errors during loading
                raise Exception(f"Error loading {file_path}: {e}")

        self.similarity_matrices = {}
        for col_name, file_name in self.similarity_file_map.items():
            file_path = get_filepath(file_name)
            try:
                with open(file_path, 'rb') as f:
                    self.similarity_matrices[col_name] = pickle.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Similarity matrix file {file_path} not found. Recalculate needed.")
            except Exception as e:
                raise Exception(f"Error loading {file_path}: {e}")
    
    def recommend_movies(self, movie_title, similarity_type):
        with app.app_context():
            try:
                similarity_matrix = self.similarity_matrices[similarity_type]
                movie_index = self.dataframes['new_df'][self.dataframes['new_df']['title']  == movie_title].index[0]
                similarities = list(enumerate(similarity_matrix[movie_index]))
                similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
                similarities = similarities[1:21] # Top 20 recommendations

                movie_titles = [self.dataframes['new_df'].iloc[i[0]]['title'] for i in similarities]

                futures = [self.executor.submit(self.fetch_movie_details, title) for title in movie_titles]
                recommendations = [future.result() for future in futures]

                return jsonify(recommendations)
            except IndexError:
                return jsonify({"error": "Movie not found"}), 404
            except KeyError as e:
                return jsonify({"error": f"Invalid similarity type: {e}"}), 400
            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


    def fetch_movie_details(self, movie_title):
        with app.app_context():
            try:
                movies_df = self.dataframes['movies']
                movies2_df = self.dataframes['movies2']
                movie_data = movies_df[movies_df['title'] == movie_title].iloc[0]
                movie2_data = movies2_df[movies2_df['title'] == movie_title].iloc[0]
                details = {
                    "title": movie_data['title'],
                    "overview": movie2_data['overview'],
                    "release_date": movie2_data['release_date'],
                    "genres": movie_data['genres'],
                    "poster_path": self.fetch_poster(movie2_data['movie_id'])
                }
                return details
            except IndexError:
                return jsonify({"error": "Movie not found"}), 404
            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


    def fetch_poster(self, movie_id):
        try:
            response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}")
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            poster_path = data.get('poster_path')
            return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        except requests.exceptions.RequestException as e:
            return "" # Log it please

    def get_movie_list(self):
        """Returns a list of available movie titles."""
        with app.app_context():
            try:
                movies = self.dataframes['movies']
                movie_titles = movies['title'].tolist()
                return jsonify(movie_titles)
            except Exception as e:
                return jsonify({"error": f"Error retrieving movie list: {e}"}), 500

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown()

recommender = MovieRecommender()

# API routes
@movie_recommender_blueprint.route('/recommend/<movie_title>/<similarity_type>')
def recommend(movie_title, similarity_type):
    return recommender.recommend_movies(movie_title, similarity_type)

@movie_recommender_blueprint.route('/details/<movie_title>')
def details(movie_title):
    return recommender.fetch_movie_details(movie_title)

@movie_recommender_blueprint.route('/list') 
def movie_list():
    return recommender.get_movie_list()

# Register the blueprint
app.register_blueprint(movie_recommender_blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5010)

    