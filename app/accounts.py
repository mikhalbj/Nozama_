from logging import info
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SubmitField, StringField, PasswordField, HiddenField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
import json
import datetime

from .models.user import User
from .models.order import Order
from .models.account import Account
from .models.reviewsmod import Review


from flask import Blueprint
bp = Blueprint('accounts', __name__)


class DepositForm(FlaskForm):
    deposit_amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    deposit_submit = SubmitField("Submit")

class WithdrawForm(FlaskForm):
    withdraw_amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    withdraw_submit = SubmitField("Submit")

class VendorForm(FlaskForm):
    vendor_confirm = BooleanField("Confirm", validators=[DataRequired()])
    vendor_submit = SubmitField("Submit")

class InformationForm(FlaskForm):
    info_firstname = StringField("First Name", validators=[DataRequired()])
    info_lastname = StringField("Last Name", validators=[DataRequired()])
    info_email = StringField("Email", validators=[DataRequired(), Email()])
    info_address = StringField("Address", validators=[DataRequired()])
    info_submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    pass_currpass = PasswordField(_l('Password'), validators=[DataRequired()])
    pass_newpass = PasswordField(_l('New Password'), validators=[DataRequired()])
    pass_newpass2 = PasswordField(
        _l('Repeat New Password'), validators=[DataRequired(),
                                           EqualTo('pass_newpass')])
    pass_submit = SubmitField("Submit")

class EditReviewForm(FlaskForm):
    productRev = HiddenField(_l('Product ID'), validators = [DataRequired()])
    RevID = HiddenField(_l('Review ID'), validators = [DataRequired()])
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    rating = RadioField(_l('Rating'), choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    submitRev = SubmitField(_l('Submit'))

class RemoveReview(FlaskForm):
    delete1 = HiddenField(_l('Review ID'), validators = [DataRequired()])
    submitDeleteProdReview = SubmitField(_l('X'))

class RemoveSellReview(FlaskForm):
    delete2 = HiddenField(_l('Review ID'), validators = [DataRequired()])
    submitDeleteSellReview = SubmitField(_l('X'))


@bp.route('/account/<id>', methods=['GET', 'POST'])
def public(id):

    user = User.get(id)
    account = Account.get(id)
    review = Review.getSellRev(id)
    addReview = EditReviewForm()
    prodReviews = Review.review_history(id)
    sellReviews = Review.review_historySell(id)
    count = Review.countSell(id)
    author = current_user.id
    removeProdRev = RemoveReview()
    removeSellRev = RemoveSellReview()

    if removeProdRev.submitDeleteProdReview.data and removeProdRev.validate():
        Review.removeReview(current_user.id, removeProdRev.delete1.data)
        
    if removeSellRev.submitDeleteSellReview.data and removeSellRev.validate():
        Review.removeSellReview(current_user.id, removeSellRev.delete2.data)


    if addReview.submitRev.data and addReview.validate():
        print("the button for review has been pressed")
        title = addReview.title.data
        product = addReview.productRev.data
        description = addReview.description.data
        rating = addReview.rating.data
        prodRevID = addReview.RevID.data
        edit_time = datetime.datetime.now()
        Review.edit_review(prodRevID, title, description, rating, edit_time)

    return render_template('public_account.html', count = count, review = review, user=user, account=account, rfs = removeProdRev, rss = removeSellRev, addRev = addReview, prodReviews = prodReviews, sellReviews = sellReviews)

@bp.route('/account/orders', methods=['GET'])
def get_account_orders():
    if not current_user.is_authenticated:
        return json.dumps('[]')

    page = 1 if request.args.get('page') == None else int(request.args.get('page'))
    limit = 10 if request.args.get('limit') == None else int(request.args.get('limit'))

    offset = (page - 1) * limit

    orders = Order.get_paginated(current_user.id, limit=limit, offset=offset)

    return json.dumps([Order.toJSON(order) for order in orders])

@bp.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    vendor_form = VendorForm()
    info_form = InformationForm()
    pass_form = PasswordForm()

    if deposit_form.deposit_submit.data and deposit_form.validate():
        Account.increase_balance(current_user.id, deposit_form.deposit_amount.data)

    if withdraw_form.withdraw_submit.data and withdraw_form.validate():
        Account.decrease_balance(current_user.id, withdraw_form.withdraw_amount.data)

    if vendor_form.vendor_submit.data and vendor_form.validate():
        if (vendor_form.vendor_confirm.data):
            Account.become_vendor(current_user.id)

    if info_form.info_submit.data and info_form.validate():
        Account.update_information(current_user.id, info_form.info_firstname.data, info_form.info_lastname.data, info_form.info_email.data, info_form.info_address.data)

    if pass_form.pass_submit.data and pass_form.validate():
        Account.update_password(current_user.id, pass_form.pass_currpass.data, pass_form.pass_newpass.data)

    account = Account.get(current_user.id)

    return render_template('account.html', title='Account', user=current_user, account=account, deposit_form=deposit_form, withdraw_form=withdraw_form, vendor_form=vendor_form, info_form=info_form, pass_form=pass_form)

