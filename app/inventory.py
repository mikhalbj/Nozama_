from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.inventory import Inventory
from .models.user import User


from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/inventory/<seller>', methods=['GET'])
    # How do I change the second part of the path to be the seller ID? 
    # how can I make sure this button only exists for sellers?
def inventory(seller):
    seller = current_user
    inventory = Inventory.get(seller)
    return render_template('inventory.html', title='See Inventory', inventory=inventory)
