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
        AND Product.seller = strng
    ''',
                                  strng = strng)       
            return [ProductInventory(*row) for row in rows]

        @staticmethod
        def search_id(seller, id):
            rows = app.db.execute('''
    SELECT id, name, quantity, seller
    FROM Product, ProductInventory
    WHERE Product.id = ProductInventory.id
        AND Product.seller = seller
        AND Product.id = id
    ''',
                                  id = id)    
                                  #not sure I understand this line   
            return [ProductInventory(*row) for row in rows]

        @staticmethod
        def search_prod(seller, prod):
            rows = app.db.execute('''
    SELECT id, name, quantity, seller
    FROM Product, ProductInventory
    WHERE Product.id = ProductInventory.id
        AND Product.seller = seller
        AND Product.name LIKE :prod
    ''',
                                  seller = seller,
                                  prod = prod)       
            return [ProductInventory(*row) for row in rows]

#commenting this out at least makes the website run!

       # @staticmethod
        # def add(name, description, price, available, seller)
          # rows = app.db.execute("""
# INSERT INTO Inventory(id, name, description, price, quantity, seller)
# VALUES(:id, :name, :description, :price, :quantity, :seller)
# # RETURNING id
# """,
#                                   id=gen_random_uuid(id),
#                                   name=name,
#                                   description=description,
#                                   price=price,
#                                   available=available
#                                   seller = seller)
#             return Inventory.get(prod_id, name, description, price, available, seller)