from flask import current_app as app

from .order import Order

class Account:
    def __init__(self, id, balance, vendor, orders):
        self.id = id
        self.balance = balance
        self.vendor = vendor
        self.orders = orders



    @staticmethod
    def is_seller(id):
        rows = app.db.execute('''
            SELECT id
            FROM Seller
            WHERE id = :id
            ''',
            id=id)

        return True if rows is not None else False

    @staticmethod
    def get_balance(id):
        rows = app.db.execute('''
            SELECT balance
            FROM Balance
            WHERE id = :id
            ''',
            id=id)

        return rows[0] if rows is not None else False

    @staticmethod
    def get_orders(id):
        rows = app.db.execute('''
            SELECT id, placed_at
            FROM AccountOrder
            WHERE account = :id
            ''',
            id=id)

        return rows

    @staticmethod
    def get(id):

        balance = Account.get_balance(id)[0]

        seller = Account.is_seller(id)

        orders = Order.get_all(id)
        return Account(id, balance, seller, orders)
