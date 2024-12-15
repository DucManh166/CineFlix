from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/Files/film_categories.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000"]}})

# Define the FilmCategory model
class FilmCategory(db.Model):
    api_id = db.Column(db.Integer, primary_key=True)  # Changed to api_id
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<FilmCategory {self.name}>'

# Create a blueprint for the categories API
categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

# Create the database table (only run once)
with app.app_context():
    db.create_all()


# API endpoints using the blueprint
@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = FilmCategory.query.all()
    output = [{'api_id': category.api_id, 'name': category.name} for category in categories] # Changed to api_id
    return jsonify({'categories': output})

@categories_bp.route('', methods=['POST'])
def add_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing "name" field in request body'}), 400

    try:
        new_category = FilmCategory(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category added', 'api_id': new_category.api_id}), 201 # Changed to api_id
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Category name "{data["name"]}" already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@categories_bp.route('/<int:api_id>', methods=['GET']) # Changed to api_id
def get_category(api_id): # Changed to api_id
    category = FilmCategory.query.get_or_404(api_id) # Changed to api_id
    return jsonify({'api_id': category.api_id, 'name': category.name}) # Changed to api_id


@categories_bp.route('/<int:api_id>', methods=['PUT']) # Changed to api_id
def update_category(api_id): # Changed to api_id
    category = FilmCategory.query.get_or_404(api_id) # Changed to api_id
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing "name" field in request body'}), 400

    try:
        category.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Category updated'})
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Category name "{data["name"]}" already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@categories_bp.route('/<int:api_id>', methods=['DELETE']) # Changed to api_id
def delete_category(api_id): # Changed to api_id
    category = FilmCategory.query.get_or_404(api_id) # Changed to api_id
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


# Register the blueprint with the app
app.register_blueprint(categories_bp)