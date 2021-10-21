# Creating the inventory page based on a typed-in seller

from flask import current_app as app

class Inventory:
        def __init__(self, id, name, quantity, seller):
            self.id = id
            self.name = name
            self.quantity = quantity
            self.seller = seller

        @staticmethod
        def get(strng):
            rows = app.db.execute('''
    SELECT id, name, quantity, seller
    FROM Product, ProductInventory
    WHERE Product.id = ProductInventory.id
        AND Product.seller LIKE :strng
    ''',
                                  strng = strng)       
            return [ProductInventory(*row) for row in rows]
