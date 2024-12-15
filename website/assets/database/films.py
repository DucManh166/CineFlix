from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
# As of now this relies on internal categories API while interacting with externals 
# as this is the appropriate solution
app = Flask(__name__)
load_dotenv()
tmdb_api_key = os.environ.get("TMDB_API_KEY")
tmdb_base_url = "https://api.themoviedb.org/3"
tmdb_blueprint = Blueprint('movies', __name__, url_prefix='/api')
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000"]}})

@tmdb_blueprint.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "Query parameter missing"}), 400
    response = make_tmdb_request(f"/search/movie?api_key={tmdb_api_key}&query={query}")
    if 'results' in response:
        # Process each movie in the results list
        results = [process_movie_image(movie) for movie in response['results']]
        return jsonify(results)
    else:
        return jsonify({'error': 'Results not found in response'}), 500

@tmdb_blueprint.route("/movie/<movie_id>")
def get_movie(movie_id):
    return make_tmdb_request(f"/movie/{movie_id}?api_key={tmdb_api_key}&append_to_response=videos,credits")

@tmdb_blueprint.route("/popular")
def get_popular():
    response = make_tmdb_request(f"/movie/popular?api_key={tmdb_api_key}")
    if 'results' in response:
        # Process each movie in the results list
        results = [process_movie_image(movie) for movie in response['results']]
        return jsonify(results)
    else:
        return jsonify({'error': 'Results not found in response'}), 500
    
@tmdb_blueprint.route("/top_rated")
def get_top_rated():
   response = make_tmdb_request(f"/movie/top_rated?api_key={tmdb_api_key}")
   if 'results' in response:
    # Process each movie in the results list
       results = [process_movie_image(movie) for movie in response['results']]
       return jsonify(results)
   else:
       return jsonify({'error': 'Results not found in response'}), 500

@tmdb_blueprint.route("/upcoming")
def get_upcoming():
    response = make_tmdb_request(f"/movie/upcoming?api_key={tmdb_api_key}")
    if 'results' in response:
        # Process each movie in the results list
        results = [process_movie_image(movie) for movie in response['results']]
        return jsonify(results)
    else:
        return jsonify({'error': 'Results not found in response'}), 500

def make_tmdb_request(path):
  url = f"{tmdb_base_url}{path}"
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if 'results' in data:
      for movie in data['results']:
        # Remove unnecessary field since not required
        movie.pop('backdrop_path', None)  
        movie.pop('original_title', None)  
        movie.pop('original_language', None)  
        movie.pop('video', None)  
        movie.pop('vote_average', None)  
        movie.pop('vote_count', None)  
        movie.pop('adult', None)  
    return data
  except requests.exceptions.RequestException as e:
    return jsonify({"error": str(e)}), 500
  except Exception as e:
    return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def get_full_poster_path(poster_path):
    if poster_path is None:
       return ""
    base_url = "https://image.tmdb.org/t/p/"
    image_size = "w500"  # Hardcoded for preview purpose, intended for modify 
    # image size on API
    full_url = base_url + image_size + poster_path
    return full_url

def process_movie_image(movie):
    movie["poster_path"] = get_full_poster_path(movie.get("poster_path"))
    return movie

app.register_blueprint(tmdb_blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5010)