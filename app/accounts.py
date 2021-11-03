from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.account import Account


from flask import Blueprint
bp = Blueprint('accounts', __name__)


class DepositForm(FlaskForm):
    deposit_amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    deposit_submit = SubmitField("Submit")

class WithdrawForm(FlaskForm):
    withdraw_amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    withdraw_submit = SubmitField("Submit")

class VendorForm(FlaskForm):
    vendor_amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    vendor_submit = SubmitField("Submit")

@bp.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    vendor_form = VendorForm()

    if deposit_form.deposit_submit.data and deposit_form.validate():
        print("try to deposit", deposit_form.deposit_amount.data)

    if withdraw_form.withdraw_submit.data and withdraw_form.validate():
        print("try to withdraw", withdraw_form.withdraw_amount.data)

    if vendor_form.vendor_submit.data and vendor_form.validate():
        print("try to become vendor", vendor_form.vendor_amount.data)

    account = Account.get(current_user.id)

    return render_template('account.html', title='Account', user=current_user, account=account, deposit_form=deposit_form, withdraw_form=withdraw_form, vendor_form=vendor_form)
