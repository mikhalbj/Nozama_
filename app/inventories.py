from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.inventory import Inventory
from .models.product import Product
from .models.user import User
from .models.account import Account


from flask import Blueprint
bp = Blueprint('inventories', __name__)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    id = current_user.id
    account = Account.get(current_user.id)
    if not Account.is_seller(id):
        return redirect(url_for(account.account, id = id))
    inventory = Inventory.get(id)
    form = NewProdForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        quantity = form.quantity.data
        # url = form.URL.data
        seller = id
        inventory = Inventory.add_prod(name = name, description = description, price = price, quantity= quantity, seller = seller)
        return redirect(url_for('inventories.inventory', id = id))
    return render_template('inventory.html', title='See Inventory', inventory=inventory, form = form, id = id)


class NewProdForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
        # I had an issue with Price being an integer field
    price = DecimalField(_l('Price'), places = 2, validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired()])
      # we will also need to change the schema for this to work
    # URL = StringField(_l('Image URL'))
    submit = SubmitField(_l('Add Product'))
