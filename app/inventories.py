from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, url, InputRequired
from flask_wtf.html5 import URLField
from wtforms.widgets.html5 import URLInput, Input
from flask_babel import _, lazy_gettext as _l


from .models.inventory import Inventory
from .models.product import Product
from .models.user import User
from .models.account import Account


from flask import Blueprint
bp = Blueprint('inventories', __name__)
@bp.route('/inventory/order-fulfillment', methods = ['GET', 'POST'])
def order_fulfillment():
    id = current_user.id
    order_history = Inventory.get_order_history(id)
    return render_template('order-fulfillment.html', order_history = order_history)

@bp.route('/inventory/seller-analytics', methods = ['GET', 'POST'])
def seller_analytics():
    id = current_user.id
    analytics = Inventory.get_seller_analytics('7f52ecc5-18ca-44d4-bc6c-55c88267e09f')
    print(analytics)
    print("doggos")
    return render_template('seller-analytics.html', analytics = analytics)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    id = current_user.id
    account = Account.get(current_user.id)
    if not Account.is_seller(id):
        return redirect(url_for(account.account, id = id))
    inventory = Inventory.get(id)
    listed = Inventory.get_listed(id)

    new_form = NewProdForm()
    edit_form = EditInventoryForm()
    quantity_form = EditQuantityForm()
    remove_form = RemoveInventoryForm()

    # initialdata = {'name': 'one', 'description': '', 'price': 0, 'quantity': 0, 'url': ''}
 
    # new_form = NewProdForm(**initialdata)
    # edit_form = EditInventoryForm(**initialdata)

    if request.method == 'POST':
        print(edit_form.submit2.data)
        
        if quantity_form.submit3.data and quantity_form.validate():
            prod_id = quantity_form.prod_id.data
            quantity = quantity_form.quantity.data
            seller = id
            inventory = Inventory.edit_quantity(prod_id, quantity, seller)
            return redirect(url_for('inventories.inventory', id = id))

        if remove_form.submit4.data and remove_form.validate():
            print(remove_form.delete.data)
            Inventory.remove(id, remove_form.delete.data)
            return redirect(url_for('inventories.inventory', id = id))

        if edit_form.submit2.data and edit_form.validate():
            
            prod_id = edit_form.prod_id.data
            name = edit_form.name.data
            description = edit_form.description.data
            price = edit_form.price.data
            quantity = edit_form.quantity.data
            url = edit_form.url.data
            seller = id
            inventory = Inventory.edit_inventory(prod_id = prod_id, name = name, description = description, price = price, quantity= quantity, url = url, seller = seller)
            print('Inventory updated')
            print(prod_id)
            return redirect(url_for('inventories.inventory', id = id))

        if new_form.submit1.data and new_form.validate():
            name = new_form.name.data
            description = new_form.description.data
            price = new_form.price.data
            quantity = new_form.quantity.data
            url = new_form.url.data
            seller = id
            inventory = Inventory.add_prod(name = name, description = description, price = price, quantity= quantity, seller = seller, url = url)
            print('New product added')
            #return render_template('inventory.html', title='See Inventory', inventory=inventory, new_form = NewProdForm(), edit_form = EditInventoryForm(), id = id, order_history = order_history)
            return redirect(url_for('inventories.inventory', id = id))
        
    print(new_form.name.data)
    return render_template('inventory.html', title='See Inventory', inventory=inventory, listed = listed, new_form = NewProdForm(), edit_form = edit_form, quantity_form = quantity_form, remove = remove_form, id = id)


class NewProdForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired()])
    url = URLField(validators=[url()])
    submit1 = SubmitField(_l('Add Product'))

class EditInventoryForm(FlaskForm):
    prod_id = StringField(_l('Product ID'), validators = [DataRequired()])
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[InputRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired()])
    url = URLField(validators=[url()])
    submit2 = SubmitField(_l('Edit Product'))

class EditQuantityForm(FlaskForm):
    prod_id = StringField(_l('Product ID'), validators = [DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired()])
    submit3 = SubmitField(_l('Edit Product'))

class RemoveInventoryForm(FlaskForm):
    delete = HiddenField(_l('Product ID'), validators = [DataRequired()])
    submit4 = SubmitField(_l('X'))
