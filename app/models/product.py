from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Product
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Product
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_categories():
        rows = app.db.execute('''
        SELECT name
        FROM Tag
        ''')
        print(rows)
        return [row[0] for row in rows]
    
    @staticmethod
    def search(strng):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Product
WHERE name LIKE :strng
''',
                              strng="%"+strng+"%")
        return [Product(*row) for row in rows]

    # THIS RETURNS NOTHING IF A PRODUCT HAS NO REVIEWS!!!
    @staticmethod
    def advanced_search(strng="", searchName=True, searchDesc=False, sortbyPrice=False, availOnly=False, priceMax=False, tag=False):

    
        sel = "SELECT Product.id, Product.name, Product.price, Product.available, COALESCE(AVG(Review.rating), NULL) AS rate"
        gby = "GROUP BY Product.id"
        where = "WHERE Review.id = ProductReview.review AND ProductReview.product = Product.id"
        frm = "FROM Product, Review, ProductReview"
        
        if searchName:
            where += " AND Product.name LIKE :strng"
        if searchDesc:
            where += " AND Product.description LIKE :strng"
        if availOnly:
            where += " AND Product.available = True"
        if priceMax:
            where += " AND Product.price < :pricemax"
        if tag:
            where += " AND ProductTag.tag = Tag.id AND Tag.name = :tag"
            frm += ", Tag, ProductTag"
        
        qry = sel + "\n" + frm + "\n" + where + "\n" + gby
        print(qry)
        rows = app.db.execute(qry, strng="%"+strng+"%", tag=tag, pricemax=priceMax)
        print(rows)
        #return rows
        return rows

