from flask import Blueprint, render_template

path = Blueprint('category', __name__)

@path.route('/category')
def render():
    return render_template("category.html")
