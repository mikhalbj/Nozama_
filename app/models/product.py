from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, description=None, rating=None, seller=None):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        if description:
            self.description = description
        if rating:
            self.rating = rating
        if seller:
            self.seller = seller

    # given a product id, returns the product's basic information
    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, name, price, available
        FROM Product
        WHERE id = :id
        ''',
                              id=id)
        return rows[0] if rows is not None else None
    
    # given a product id, returns product information along with related review summaries
    # used when displaying product details
    @staticmethod
    def fullget(id):
        rows = app.db.execute('''
        SELECT Product.id, name, price, available, Product.description, COALESCE(ROUND(AVG(T.rating), 2), NULL) AS rate, COUNT(T.rating) AS count
        FROM Product LEFT OUTER JOIN (SELECT * FROM Review, ProductReview WHERE Review.id = ProductReview.review) AS T ON Product.id = T.product
        WHERE Product.id = :id
        GROUP BY Product.id
        ''',
                              id=id)
        return rows[0] if rows is not None else None
    
    # given a product id, returns the product's image's url; if none exists, return a dummy url
    # used when displaying search results, product details, and more
    @staticmethod
    def get_img(id):
        print(id)
        rows = app.db.execute('''
                        SELECT url
                        FROM ProductImage
                        WHERE ProductImage.product = :id
                        ''', id=id)
        return rows[0][0] if rows else "https://cdn.w600.comps.canstockphoto.com/pile-of-random-stuff-eps-vector_csp24436545.jpg"
    
    # returns the human-readable name of every category in database
    # used when dispalying categories for searching
    @staticmethod
    def get_categories():
        rows = app.db.execute('''
        SELECT name
        FROM Tag
        ''')
        print(rows)
        return [row[0] for row in rows]
    
    # constructs a query for the searching tools
    # used to display results from the search page
    @staticmethod
    def advanced_search(strng="", searchName=True, searchDesc=False, sortBy=False, availOnly=False, priceMax=False, tag=False, page=1):

    
        sel = "SELECT Product.id, Product.name, Product.price, Product.available, COALESCE(ROUND(AVG(T.rating),2), NULL) AS rate"
        gby = "GROUP BY Product.id"
        where = "WHERE "
        frm = "FROM Product LEFT OUTER JOIN (SELECT * FROM Review, ProductReview WHERE Review.id = ProductReview.review) AS T ON Product.id = T.product"
        lo = "LIMIT 25"
        sby = ""

        if searchName and eval(searchDesc):
            where += "(Product.name LIKE :strng OR Product.description LIKE :strng)"
        elif eval(searchDesc):
            where += " Product.description LIKE :strng"
        elif searchName:
            where += " Product.name LIKE :strng"
        if eval(availOnly):
            where += " AND Product.available = True"
        if priceMax:
            where += " AND Product.price < :pricemax"
        if tag:
            where += " AND ProductTag.tag = Tag.id AND Tag.name = :tag AND ProductTag.product = Product.id"
            frm += ", Tag, ProductTag"
        if sortBy == 'price':
            sby = "ORDER BY price" + "\n"
        elif sortBy == 'rating':
            sby = "ORDER BY rate DESC NULLS LAST" + "\n"
        if page and int(page) > 1:
            lo += " OFFSET "
            lo += str(25*(int(page)-1))
        
        qry = sel + "\n" + frm + "\n" + where + "\n" + gby
        qry = "SELECT * FROM ProductImage RIGHT OUTER JOIN (" + qry + ") AS SUB ON ProductImage.product = SUB.id" + "\n" + sby + lo
        print(qry)
        rows = app.db.execute(qry, strng="%"+strng+"%", tag=tag, pricemax=priceMax)
        return rows
    
    # returns the four products with the highest sum of ratings
    # used in the carousel on index page
    @staticmethod
    def popular():
        prods = app.db.execute('''
        SELECT Product.name, Product.description, ProductImage.url, Sub.product, Sub.rate, Sub.count, Product.id
        FROM (
            SELECT ProductReview.product, SUM(Review.rating) AS rate, COUNT(ProductReview.product) AS count
            FROM Review, ProductReview 
            WHERE Review.id = ProductReview.review
            GROUP BY ProductReview.product
            ORDER BY rate DESC NULLS LAST
            LIMIT 4
        ) AS Sub, Product, ProductImage
        WHERE ProductImage.product = Sub.product AND Product.id = Sub.product
        ''')
        print(prods)
        return prods
    
    # given a user id and product id, returns true if user created the product, false otherwise
    # used to conditionally display the "edit listing" on product details page
    @staticmethod
    def is_lister(pid, uid):
        rows = app.db.execute('''
        SELECT *
        FROM Product
        WHERE lister = :uid AND id = :pid
        ''',
                              pid=pid, uid=uid)
        return True if len(rows) > 0 else False


