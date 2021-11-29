from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DecimalField, SelectMultipleField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, url
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.reviewsmod import Review
from .models.cart import Cart
from .models.account import Account
from .models.inventory import Inventory


from flask import Blueprint
bp = Blueprint('product', __name__)

class SearchForm(FlaskForm):
    searchterm = StringField('Search here')
    tag = RadioField('Filter by category')
    avail = BooleanField('Only find available items')
    maxprice = DecimalField('Only find items cheaper than:')
    searchdesc = BooleanField('Match ketwords in description:')
    sort = RadioField('Sort by price or rating:', choices=['price', 'rating'])
    submit = SubmitField()

class CartAddForm(FlaskForm):
    quantity = IntegerField('How many of this item?', validators=[DataRequired()])
    submit = SubmitField()

class NextPageForm(FlaskForm):
    submit = SubmitField(_l('Next Page'), validators=[DataRequired()])

class PrevPageForm(FlaskForm):
    submit = SubmitField(_l('Previous Page'), validators=[DataRequired()])

class SellProdForm(FlaskForm):
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired()])
      # we will also need to change the schema for this to work
    optin = BooleanField(_l('I want to sell this product'), validators=[DataRequired()])
    submit = SubmitField(_l('Sell Product'))

class EditListingForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[DataRequired()])
    url = URLField(validators=[url()])
    submit2 = SubmitField(_l('Edit Product'))

@bp.route('/product_details/<uuid:id>', methods=['GET', 'POST'])
def product(id):
    form = CartAddForm()
    sellForm = SellProdForm()
    eForm = EditListingForm()
    product = Product.fullget(id)
    image = Product.get_img(id)
    sellBool = Account.is_seller(current_user.id) and not Inventory.sells(current_user.id, id)
    editBool = Product.is_lister(id, current_user.id)
    if eform.submit.data and eform.validate():
        Inventory.edit_listing(id, eform.name.data, eform.description.data, eform.price.data, eform.url.data)
    if form.submit.data and form.validate():
        Cart.add_cart(current_user.id, form.quantity.data, id)
        print("YAY")
    if sellForm.submit.data and sellForm.validate():
        Inventory.start_selling(current_user.id, sellForm.quantity.data, id)
        print("YOU DID IT!")
        return redirect(url_for('product.product_details', id=id))
    if image:
        image = image[0][1]
    else:
        image = "https://cdn.w600.comps.canstockphoto.com/pile-of-random-stuff-eps-vector_csp24436545.jpg"
    quantity = Product.get_inventory(id)[0]
    reviews = Review.get(id)
    return render_template('product_details.html', title='See Product', product=product, imgurl=image, num=quantity, cartform=form, review=reviews, sf=sellForm, sb=sellBool, edit_form=eform, eb=editBool)

@bp.route('/search/<argterm>', methods=['GET', 'POST'])
def search(argterm):
    print(request.form)
    products = Product.search(strng=argterm)
    return render_template('search.html', title='Search for Products', products=products, term=argterm)


@bp.route('/advanced_search/', methods=['GET', 'POST'])
def advanced_search():
    s = request.args.get("argterm")
    a = request.args.get("avail")
    t = request.args.get("tag")
    p = request.args.get("maxprice")
    d = request.args.get("searchdesc")
    sby = request.args.get("sort")
    pg = request.args.get("page")
    products = Product.advanced_search(strng=s, tag=t, priceMax=p, availOnly=a, searchDesc=d, sortBy=sby, page=pg)
    if not pg:
        pg = 1
    
    pp = url_for('product.advanced_search',argterm=s, tag=t, maxprice=p, avail=a, searchdesc=d, sort=sby, page=(int(pg)-1))
    np = url_for('product.advanced_search',argterm=s, tag=t, maxprice=p, avail=a, searchdesc=d, sort=sby, page=(int(pg)+1))
    
    return render_template('search.html', title='Search for Products', products=products, term=s, page=int(pg), pages=bool(len(products)==25), np=np, pp=pp)


@bp.route('/search/', methods=['GET', 'POST'])
def presearch():
    form = SearchForm()
    form.tag.choices = Product.get_categories()
    if form.is_submitted():
        print(request.form)
        return redirect(url_for('product.advanced_search', argterm=form.searchterm.data, tag=form.tag.data, maxprice=form.maxprice.data, avail=form.avail.data, searchdesc=form.searchdesc.data, sort=form.sort.data))
    return render_template('search.html', title='Search for Products', presearch=True, form=form)



