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

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Product
WHERE id = :id
''',
                              id=id)
        return rows[0] if rows is not None else None
    
    @staticmethod
    def fullget(id):
        rows = app.db.execute('''
SELECT Product.id, name, price, available, Product.description, COALESCE(ROUND(AVG(T.rating), 2), NULL) AS rate, Product.seller
FROM Product LEFT OUTER JOIN (SELECT * FROM Review, ProductReview WHERE Review.id = ProductReview.review) AS T ON Product.id = T.product
WHERE Product.id = :id
GROUP BY Product.id
''',
                              id=id)
        return rows[0] if rows is not None else None
    
    @staticmethod
    def get_img(id):
        print(id)
        rows = app.db.execute('''
                        SELECT *
                        FROM ProductImage
                        WHERE ProductImage.product = :id
                        ''', id=id)
        return rows

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available, description
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
    def get_inventory(id):
        rows = app.db.execute('''
        SELECT quantity
        FROM ProductInventory
        WHERE product = :id''', id=id)
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

