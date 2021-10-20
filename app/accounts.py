from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.account import Account


from flask import Blueprint
bp = Blueprint('accounts', __name__)


@bp.route('/account', methods=['GET'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    account = Account.get(current_user.id)

    return render_template('account.html', title='Account', user=current_user, account=account)
