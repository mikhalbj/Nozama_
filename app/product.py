from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DecimalField, SelectMultipleField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, url, InputRequired
from flask_wtf.html5 import URLField
from wtforms.widgets.html5 import URLInput, Input
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.reviewsmod import Review
from .models.cart import Cart
from .models.account import Account
from .models.inventory import Inventory


from flask import Blueprint
bp = Blueprint('product', __name__)

# form on the search page to input search query parameters
class SearchForm(FlaskForm):
    searchterm = StringField('Search for:')
    tag = RadioField('Filter by category:')
    avail = BooleanField('Only find available items:')
    maxprice = DecimalField('Only find items cheaper than:')
    searchdesc = BooleanField('Match keywords in description:')
    sort = RadioField('Sort products by:', choices=['price', 'rating'])
    submit = SubmitField()

# form in the cartModal to add a product to user's cart from product details page
class CartAddForm(FlaskForm):
    quantity = IntegerField('How many of this item?', validators=[DataRequired()])
    submit = SubmitField()

# form in the saveModel to save a product for later from product details apge
class SaveProdForm(FlaskForm):
    save = SubmitField(_l('Save For Later'), validators=[DataRequired()])

# form in the sellModal for a vendor to begin selling a product from product details page
class SellProdForm(FlaskForm):
    q = IntegerField(_l('Quantity'), validators=[InputRequired()])
    optin = BooleanField(_l('I confirm I am selling this product'), validators=[DataRequired()])
    s = SubmitField(_l('Sell Product'))

# form in editModal to edit product details if user created the product being viewed
class EditListingForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), places = 2, validators=[InputRequired()])
    url = URLField(validators=[url()])
    tag =  SelectField(u'Tag', choices=[(0, 'cooking'), (1, 'food'), (2, 'beauty'), (3, 'decor'), (4, 'furniture'), (5, 'education'), (6, 'office supplies'), (7, 'sports'), (8, 'technology'), (9, 'music'), (10, 'art')])
    submit2 = SubmitField(_l('Edit Product'))

# prodcut details page
@bp.route('/product_details/<uuid:id>', methods=['GET', 'POST'])
def product(id):
    
    # perform checks on user's identity to conditionally display buttons for proper functionality
    if not current_user.is_authenticated:
        saveBool = False
        sellBool = False
        editBool = False
    else:
        saveBool = Cart.can_save(current_user.id, id)
        sellBool = Account.is_seller(current_user.id) and not Inventory.sells(current_user.id, id)
        editBool = Product.is_lister(id, current_user.id)
    
    # instantiate and define behavior for adding to cart form
    form = CartAddForm()
    if form.submit.data and form.validate():
        if Cart.duplicate(current_user.id, id) == False:
            flash("Product already added to cart!")
        else:
            Cart.add_cart(current_user.id, form.quantity.data, id)

    # instantiate and define behavior for begin selling form
    sellForm = SellProdForm()
    if sellForm.s.data and sellForm.validate():
        Inventory.start_selling(current_user.id, sellForm.q.data, id)
        return redirect(url_for('product.product', id=id))

    # instantiate and define behavior for edit listing form
    eForm = EditListingForm()
    if eForm.submit2.data and eForm.validate():
        Inventory.edit_inventory(id, eForm.name.data, eForm.description.data, eForm.price.data, eForm.url.data, eForm.tag.data)
        return redirect(url_for('product.product', id=id))
    
    # instantiate and define behavior for save for later form
    saveForm = SaveProdForm()
    if saveForm.save.data and saveForm.validate():
        if saveBool:
            Cart.save(current_user.id, id)
            flash('The product is saved for later!')
        else:
            flash('You\'ve already saved this product!')
    
    # get data for product to dispaly
    product = Product.fullget(id)
    tags = Product.get_tags(id)
    print(tags)
    image = Product.get_img(id)
    reviews = Review.getProdRev(id)
    sellers = Inventory.all_sellers(id)
    
    return render_template('product_details.html', title='See Product', product=product, imgurl=image, cartform=form, review=reviews, sf=sellForm, sb=sellBool, sellers=sellers, saveform=saveForm, edit_form=eForm, eb=editBool, tag=tags)

# search results page
@bp.route('/advanced_search/', methods=['GET', 'POST'])
def advanced_search():
    # extract query parameters from HTTP request
    s = request.args.get("argterm")
    a = request.args.get("avail")
    t = request.args.get("tag")
    p = request.args.get("maxprice")
    d = request.args.get("searchdesc")
    sby = request.args.get("sort")
    pg = request.args.get("page")

    # search database for matching products using API method
    products = Product.advanced_search(strng=s, tag=t, priceMax=p, availOnly=a, searchDesc=d, sortBy=sby, page=pg)
    
    # pre-define URLS for pagination buttons
    if not pg:
        pg = 1
    pp = url_for('product.advanced_search',argterm=s, tag=t, maxprice=p, avail=a, searchdesc=d, sort=sby, page=(int(pg)-1))
    np = url_for('product.advanced_search',argterm=s, tag=t, maxprice=p, avail=a, searchdesc=d, sort=sby, page=(int(pg)+1))
    
    return render_template('search.html', title='Search for Products', products=products, term=s, page=int(pg), pages=bool(len(products)==25), np=np, pp=pp)

# search form page
@bp.route('/search/', methods=['GET', 'POST'])
def presearch():
    # instantiate and define behavior for search form
    form = SearchForm()
    form.tag.choices = Product.get_categories()
    if form.is_submitted():
        return redirect(url_for('product.advanced_search', argterm=form.searchterm.data, tag=form.tag.data, maxprice=form.maxprice.data, avail=form.avail.data, searchdesc=form.searchdesc.data, sort=form.sort.data))
    return render_template('search.html', title='Search for Products', presearch=True, form=form)



