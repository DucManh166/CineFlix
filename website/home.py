from flask import Blueprint, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()
path = Blueprint('home', __name__)
API_IP = os.getenv("API_IP")
CATEGORIES_PORT = os.getenv("CATEGORIES_PORT")
FILM_PORT = os.getenv("FILM_PORT")

@path.route('/')
def render():
    categories = handle_categories_response("api/categories")
    
    return render_template("index.html", 
                           categories=categories.json()['categories'])

def handle_categories_response(path):
    url = f"http://{API_IP}:{CATEGORIES_PORT}/{path}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        response = []  # Handle errors, provide empty list if API fails
        # As of now all unhandled exception is considered undefined behavior

    return response

# Deprecated
def handle_film_response(path):
    url = f"http://{API_IP}:{FILM_PORT}/{path}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        response = []  # Handle errors, provide empty list if API fails
        # As of now all unhandled exception is considered undefined behavior

    return response
