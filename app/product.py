from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DecimalField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product


from flask import Blueprint
bp = Blueprint('product', __name__)

class SearchForm(FlaskForm):
    searchterm = StringField('Search here')
    tag = RadioField('Filter by category')
    avail = BooleanField('Only find available items')
    maxprice = DecimalField('Only find items cheaper than:')
    searchdesc = BooleanField('Match ketwords in description:')
    submit = SubmitField()

@bp.route('/product_details/<uuid:id>', methods=['GET'])
def product(id):
    product = Product.fullget(id)
    image = Product.get_img(id)[0][1]
    quantity = Product.get_inventory(id)[0]
    return render_template('product_details.html', title='See Product', product=product, imgurl=image, num=quantity)

@bp.route('/search/<argterm>', methods=['GET', 'POST'])
def search(argterm):
    print(request.form)
    products = Product.search(strng=argterm)
    return render_template('search.html', title='Search for Products', products=products, term=argterm)


@bp.route('/advanced_search/', methods=['GET', 'POST'])
def advanced_search():
    print(request.args)
    s = request.args.get("argterm")
    a = request.args.get("avail")
    t = request.args.get("tag")
    p = request.args.get("maxprice")
    d = request.args.get("searchdesc")
    products = Product.advanced_search(strng=s, tag=t, priceMax=p, availOnly=a, searchDesc=d)
    return render_template('search.html', title='Search for Products', products=products, term=s)


@bp.route('/search/', methods=['GET', 'POST'])
def presearch():
    form = SearchForm()
    form.tag.choices = Product.get_categories()
    if form.is_submitted():
        print(request.form)
        return redirect(url_for('product.advanced_search', argterm=form.searchterm.data, tag=form.tag.data, maxprice=form.maxprice.data, avail=form.avail.data, searchdesc=form.searchdesc.data))
    return render_template('search.html', title='Search for Products', presearch=True, form=form)

