import datetime;
from flask import current_app as app

class Cart:
    def __init__(self, account_id, total):
        self.account_id = account_id
        self.total = total
    
    @staticmethod
    def get_all(account_id):
        rows = app.db.execute('''
            SELECT Product.id, Product.name, CartProduct.quantity, Product.Price*CartProduct.quantity AS "totalPrice"
            FROM CartProduct, Product
            WHERE cartProduct.account = :account_id AND Product.id = CartProduct.product
            ''',
            account_id=account_id)
        print(rows)      
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
        return rows[0][0] if rows else 0

    @staticmethod
    def cart_total(account_id):
        rows = app.db.execute('''
            SELECT SUM(Product.Price*CartProduct.quantity)
            FROM CartProduct, Product
            WHERE CartProduct.product = Product.id AND cartProduct.account = :account_id
            ''',
            account_id=account_id)
        return rows[0][0] if rows else 0.0



