from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash

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

        return True if len(rows) != 0 else False

    @staticmethod
    def get_balance(id):
        rows = app.db.execute('''
            SELECT balance
            FROM Balance
            WHERE id = :id
            ''',
            id=id)


        return rows[0][0] if len(rows) != 0 else 0

    @staticmethod
    def increase_balance(id, amount):
        try:
            rows = app.db.execute('''
                UPDATE Balance
                SET balance = balance + :amount
                WHERE id = :id
            ''', id=id, amount=amount)
        except Exception as err:
            print(err)
        

    @staticmethod
    def decrease_balance(id, amount):
        try:
            rows = app.db.execute('''
                UPDATE Balance
                SET balance = balance - :amount
                WHERE id = :id
            ''', id=id, amount=amount)
        except Exception as err:
            print(err)

    @staticmethod
    def become_vendor(id):
        try:
            rows = app.db.execute('''
                INSERT INTO Seller (id) VALUES (:id)
            ''', id=id)
        except Exception as err:
            print(err)

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

        # print(app.db.execute('''
        #     SELECT id, password
        #     FROM Account
        #     WHERE id = :id
        #     ''',
        #     id=id))

        # print(generate_password_hash('test'))
        # print(generate_password_hash('test2'))

        balance = Account.get_balance(id)

        seller = Account.is_seller(id)

        orders = Order.get_paginated(id)
        return Account(id, balance, seller, orders)


    @staticmethod
    def update_information(id, firstname, lastname, email, address):
        try:
            rows = app.db.execute('''
                UPDATE Account
                SET firstname = :firstname, lastname = :lastname, email = :email, address = :address
                WHERE id = :id
                RETURNING *
            ''', id=id, firstname=firstname, lastname=lastname, email=email, address=address)

            print(rows)
        except Exception as err:
            print(err)


    @staticmethod
    def update_password(id, old_password, new_password):
        try:
            rows = app.db.execute('''
                SELECT id, password
                FROM Account
                WHERE id = :id
            ''', id=id)

            if check_password_hash(rows[0][1], old_password):
                rows = app.db.execute('''
                    UPDATE Account
                    SET password = :new_password
                    WHERE id = :id
                ''', id=id, new_password=generate_password_hash(new_password))
            else:
                print('Old password does not match')
        except Exception as err:
            print(err)