from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.inventory import Inventory
from .models.user import User


from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/inventory/<seller>', methods=['GET'])
    # How do I change the second part of the path to be the seller ID? 
    # how can I make sure this button only exists for sellers?
def inventory(seller):
    seller = current_user
    inventory = Inventory.get(seller)
    return render_template('inventory.html', title='See Inventory', inventory=inventory)


class NewProdForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
        # I had an issue with Price being an integer field
    price = StringField(_l('Price'), validators=[DataRequired()])
    available = BooleanField(_l('Available'), validators=[DataRequired()])
      # this needs to be changed to quantity eventually
      # we will also need to change the schema for this to work
    seller = StringField(_l('Seller'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Product'))

@bp.route('/inventory/<seller>/add-product', methods=['GET', 'POST'])
def add_prod():
    FORM = NewProdForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        available = form.available.data
        seller = form.seller.data
        inventory = Inventory.add_prod(name, description, price, available, seller)
        return render_template('inventory.html', title='See Updated Inventory', inventory=inventory)
