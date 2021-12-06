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
bp = Blueprint('review', __name__)


class AddReviewForm(FlaskForm):
    author = current_user
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    rating = RadioField(_l('Rating'), choices=['1', '2', '3', '4', '5'], validators=[DataRequired()])
    submit1 = SubmitField()

@bp.route('/product_details/<uuid:id>/submitReview', methods=['GET', 'POST'])
def review(id):
    new_form = AddReviewForm()
    if new_form.submit1.data and new_form.validate():
        Review.add_prodrev(new_form.title.data, current_user.id, new_form.description.data, new_form.rating.data, uuid)
    return render_template('submitreview.html', title='New Review', user=current_user, new_form = new_form)
