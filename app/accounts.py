from logging import info
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SubmitField, StringField, PasswordField
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

@bp.route('/account/<id>', methods=['GET', 'POST'])
def public(id):
    return '<html><body>Hello</body></html>'

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
