from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product


from flask import Blueprint
bp = Blueprint('product', __name__)

class SearchForm(FlaskForm):
    searchterm = StringField('Search here')
    submit = SubmitField()

@bp.route('/product_details/<uuid:id>', methods=['GET'])
def product(id):
    
    product = Product.get(id)
    return render_template('product_details.html', title='See Product', product=product)

@bp.route('/search/<argterm>', methods=['GET', 'POST'])
def search(argterm):
    
    # SEARCH TERM CANNOT INCLUDE A SLASH
    products = Product.search(argterm)
    return render_template('search.html', title='Search for Products', products=products, term=argterm)

@bp.route('/search/', methods=['GET', 'POST'])
def presearch():
    form = SearchForm()
    if form.is_submitted():
        return redirect(url_for('product.search', argterm=form.searchterm.data))
    return render_template('search.html', title='Search for Products', presearch=True, form=form)

