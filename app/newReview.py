from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DecimalField, SelectMultipleField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.reviewsmod import Review
from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('product', __name__)