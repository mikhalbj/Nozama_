from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get most popular products
    pops = Product.popular()
    # render the page by adding information to the index.html file
    return render_template('index.html', pop=pops)
