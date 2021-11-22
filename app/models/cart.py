import datetime;
from flask import current_app as app

class Cart:
    def __init__(self, account_id, total):
        self.account_id = account_id
        self.total = total
    
    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name, CartProduct.quantity, CAST(Product.Price*CartProduct.quantity AS DECIMAL(10,2)) AS "totalPrice"
            FROM CartProduct, Product
            WHERE cartProduct.account = :account_id AND Product.id = CartProduct.product
            ''',
            account_id=account_id)     
        return rows if rows is not None else None


    @staticmethod
    def place_order(account_id):
        rows = app.db.execute('''
            INSERT INTO AccountOrder(account, placed_at)
            VALUES(:account_id, :time)
            RETURNING id
            ''',
            account_id = account_id,
            time = datetime.datetime.now())
        id = rows[0][0]

        #rows = app.db.execute('''
            #INSERT INTO AccountOrderProduct(account_order, product, seller, quantity, price, status, shipped_at, delivered_at)
            #SELECT AccountOrder.id, pv.product, seller, pv.quantity, p.price, NULL, NULL, NULL
            #FROM AccountOrder, Product AS p 
            #JOIN ProductInventory pv ON p.id=pv.product
            #JOIN CartProduct cp ON p.id=cp.product
            #WHERE AccountOrder.account = :account_id AND placed_at = :time AND cp.Account = :account_id
            #RETURNING account_order
            #''',
            #account_id = account_id,
            #time = datetime.datetime.now())
        #id = rows[0][0]

        rows = app.db.execute('''
        DELETE FROM CartProduct WHERE account = :account_id RETURNING account
        ''',
        account_id = account_id
        )
        return rows if rows is not None else None

    @staticmethod
    def add_cart(account_id, quantity, id):
        rows = app.db.execute('''
        INSERT INTO CartProduct(account, product, quantity)
        VALUES(:account_id, :prod_id, :quantity)
        RETURNING account
        ''',
            account_id = account_id,
            prod_id = id,
            quantity = quantity)
        return True
    
    @staticmethod
    def cart_total(account_id):
        rows = app.db.execute('''
            SELECT SUM(Product.Price*CartProduct.quantity)
            FROM CartProduct, Product
            WHERE CartProduct.product = Product.id AND cartProduct.account = :account_id
            ''',
            account_id=account_id)
        return rows[0][0] if rows else 0.0

    @staticmethod
    def saved(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name
            FROM SavedProduct, Product
            WHERE SavedProduct.account = :account_id AND Product.id = SavedProduct.product
            ''',
            account_id=account_id)     
        return rows if rows is not None else None

