from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('carts', __name__,)

class MakeOrder(FlaskForm):
    info_address = StringField("Address", validators=[DataRequired()])
    info_submit = SubmitField()

class RemoveItem(FlaskForm):
    info_submit = SubmitField()

@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    order_form = MakeOrder()
    cart = Cart.get_all(current_user.id)
    total = Cart.cart_total(current_user.id)
    saved = Cart.saved(current_user.id)
    remove = RemoveItem()
    
    if order_form.is_submitted() and order_form.validate():
        Cart.place_order(current_user.id)
        return redirect(url_for('carts.cart'))

    if remove.is_submitted():
        Cart.remove(current_user.id, remove.form.get('productId'))
        return redirect(url_for('carts.cart'))

    return render_template('cart.html', title='Cart', cart=cart, total=total, saved=saved, order_form=order_form, remove=remove)
