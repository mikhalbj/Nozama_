from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, url
from flask_wtf.html5 import URLField
from wtforms.widgets.html5 import URLInput, Input
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
    new_form = NewProdForm()
    edit_form = EditInventoryForm()

    if new_form.submit1.data and new_form.validate():
        name = new_form.name.data
        description = new_form.description.data
        price = new_form.price.data
        quantity = new_form.quantity.data
        url = new_form.url.data
        seller = id
        inventory = Inventory.add_prod(name = name, description = description, price = price, quantity= quantity, seller = seller, url = url)
        print('New product added')
        return redirect(url_for('inventories.inventory', id = id))
    
    if edit_form.submit2.data and edit_form.validate():
        seller = id
        inventory = Inventory.edit_inventory(edit_form.prod_id.data, edit_form.name.data, edit_form.description.data, edit_form.price.data, edit_form.quantity.data, edit_form.url.data, seller)
        print('Inventory updated')
        return redirect(url_for('inventories.inventory', id = id))

    return render_template('inventory.html', title='See Inventory', inventory=inventory, new_form = new_form, edit_form = edit_form, id = id)


class NewProdForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired()])
    url = URLField(validators=[url()])
    submit1 = SubmitField(_l('Add Product'))

class EditInventoryForm(FlaskForm):
    prod_id = IntegerField(_l('Product ID'), validators = [DataRequired()])
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired()])
    url = URLField(validators=[url()])
    submit2 = SubmitField(_l('Edit Product'))
