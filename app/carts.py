from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart
from .models.order import Order
from .models.order import OrderProduct


from flask import Blueprint
import datetime;

bp = Blueprint('carts', __name__,)

class MakeOrder(FlaskForm):
    info_submit = SubmitField('Yes')

class MoveToCart(FlaskForm):
    product = HiddenField(_l('Product ID'), validators = [DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit1 = SubmitField(_l('Submit'))

class MoveToSaved(FlaskForm):
    productx = HiddenField(_l('Product ID'), validators = [DataRequired()])
    submitx = SubmitField(_l('X'))

class RemoveItem(FlaskForm):
    delete = HiddenField(_l('Product ID'), validators = [DataRequired()])
    submit = SubmitField(_l('X'))

class RemoveFromSaved(FlaskForm):
    delete1 = HiddenField(_l('Product ID'), validators = [DataRequired()])
    submit2 = SubmitField(_l('X'))

class EditQuantity(FlaskForm):
    product1 = HiddenField(_l('Product ID'), validators = [DataRequired()])
    quantity1 = IntegerField("Quantity", validators=[DataRequired()])
    submit3 = SubmitField(_l('Save'))

@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    order_form = MakeOrder()
    cart = Cart.get_all(current_user.id)
    total = Cart.cart_total(current_user.id)
    saved = Cart.saved(current_user.id)
    remove = RemoveItem()
    move = MoveToCart()
    save = MoveToSaved()
    rfs = RemoveFromSaved()
    editquant = EditQuantity()
    
    if remove.submit.data and remove.validate():
        Cart.removeProduct(current_user.id, remove.delete.data)
        return redirect(url_for('carts.cart'))

    if editquant.submit3.data and editquant.validate():
        Cart.editQuantity(current_user.id, editquant.product1.data, editquant.quantity1.data)
        return redirect(url_for('carts.cart'))

    if rfs.submit2.data and rfs.validate():
        Cart.removeSaved(current_user.id, rfs.delete1.data)
        return redirect(url_for('carts.cart'))

    if save.submitx.data and save.validate():
        if Cart.can_save(current_user.id, save.productx.data) == False:
            flash("Product already saved!")
        else:
            Cart.save(current_user.id, save.productx.data)
            Cart.removeProduct(current_user.id, save.productx.data)
        return redirect(url_for('carts.cart'))

    if move.submit1.data and move.validate():
        if Cart.duplicate(current_user.id, move.product.data) == False:
            flash("Product already added to cart!")
        else:
            Cart.add_cart(current_user.id, move.quantity.data, move.product.data)
        return redirect(url_for('carts.cart'))

    if order_form.is_submitted() and order_form.validate():
        time = datetime.datetime.now()
        if Cart.cartcount(current_user.id) == 0:
            flash('Cannot Place Order - Cart is Empty')
        elif Cart.check_inventory(current_user.id, time) == False:
            flash('Cannot Place Order - Insufficient Product Availability')
        else:
            if Cart.get_balance(current_user.id) < Cart.cart_total(current_user.id):
                flash('Cannot Place Order - Insufficient Balance')
            else:
                Cart.place_order(current_user.id, time)
        return redirect(url_for('carts.cart'))

    return render_template('cart.html', title='Cart', cart=cart, total=total, saved=saved, order_form=order_form, remove=remove, move=move, rfs=rfs, editquant=editquant, save=save)

@bp.route('/order/<uuid:id>', methods=['GET', 'POST'])
def order(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    orderplaced = OrderProduct.get_all(id)
    total = OrderProduct.order_cost(id)
    orderID = id
    time_placed = OrderProduct.get_all(id)
    return render_template('orderpage.html', title='Order', orderplaced=orderplaced, total=total, orderID = orderID, time_placed=time_placed)

    
