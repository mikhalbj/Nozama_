from flask import render_template, redirect, url_for, request
from flask import flash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.cart import Cart
from .models.order import Order
from .models.order import OrderProduct
from .models.reviewsmod import Review


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

class AddReviewForm(FlaskForm):
    productRev = HiddenField(_l('Product ID'), validators = [DataRequired()])
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    rating = RadioField(_l('Rating'), choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    submitRev = SubmitField(_l('Submit'))

class AddSellReviewForm(FlaskForm):
    sellerRev = HiddenField(_l('Seller ID'), validators = [DataRequired()])
    titleSell = StringField(_l('Title'), validators=[DataRequired()])
    descriptionSell = StringField(_l('Description'), validators=[DataRequired()])
    ratingSell = RadioField(_l('Rating'), choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    submitSellRev = SubmitField(_l('Submit'))

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
        #ensures the cart is not empty
        if Cart.cartcount(current_user.id) == 0:
            flash('Cannot Place Order - Cart is Empty')
        #ensures there is enough inventory for the number of items in cart
        elif Cart.check_inventory(current_user.id, time) == False:
            flash('Cannot Place Order - Insufficient Product Availability')
        else:
            #ensures user has enough balance to place order
            if Cart.get_balance(current_user.id) < Cart.cart_total(current_user.id):
                flash('Cannot Place Order - Insufficient Balance')
            else:
                Cart.place_order(current_user.id, time)
                flash('Order Placed! Check Account for Details')
        return redirect(url_for('carts.cart'))

    return render_template('cart.html', title='Cart', cart=cart, total=total, saved=saved, order_form=order_form, remove=remove, move=move, rfs=rfs, editquant=editquant, save=save)

@bp.route('/order/<uuid:id>', methods=['GET', 'POST'])
def order(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    addReview = AddReviewForm()
    addSellReview = AddSellReviewForm()
    orderplaced = OrderProduct.get_all(id)
    total = OrderProduct.order_cost(id)
    orderID = id
    author = current_user.id
    prodReviewed = Review.notReviewedProd
    #sellReviewed = Review.notReviewedSell

    

    time_placed = Order.get(id)[0][2]
    specificInfo = str(time_placed.year) + '/' + str(time_placed.month) + '/' + str(time_placed.day) + " " + str(time_placed.hour) + ":" + str(time_placed.minute) + ":" + str(time_placed.second)

    if OrderProduct.check_status(id) == True:
        s = "Fulfilled"
    else:
        s = "In Progress"
    
#for products:
    if addReview.submitRev.data and addReview.validate():
        print("the button for review has been pressed")
        title = addReview.title.data
        product = addReview.productRev.data
        description = addReview.description.data
        rating = addReview.rating.data
        if Review.add_prodrev(title, author, description, rating, product) == 0:
            flash("You cannot review the same product twice.")

        

#for sellers:
    if addSellReview.submitSellRev.data and addSellReview.validate():    
        titleS = addSellReview.titleSell.data
        seller = addSellReview.sellerRev.data
        descriptionS = addSellReview.descriptionSell.data
        ratingS = addSellReview.ratingSell.data

        if Review.add_sellrev(titleS, author, descriptionS, ratingS, seller) == 0:
            flash("You cannot review the same seller twice.")

    return render_template('orderpage.html', title='Order', orderplaced=orderplaced, total=total, orderID = orderID, addReview=addReview, addSellReview=addSellReview, prodReviewed = prodReviewed, time_placed=time_placed, specificInfo=specificInfo, s=s)

    
