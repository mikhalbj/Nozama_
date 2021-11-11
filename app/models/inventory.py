# Creating the inventory page based on a typed-in seller

from flask import current_app as app

class Inventory:
        def __init__(self, id, prod_id, name, available):
            self.id = id
            self.prod_id = prod_id
            self.name = name
            self.available = available

        @staticmethod
        def get(id):
            rows = app.db.execute('''
    SELECT Product.id, name, quantity, seller, description
    FROM Product, ProductInventory
    WHERE Product.id = ProductInventory.product
        AND Product.seller = :id
    ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def add_prod(name, description, price, quantity, seller):
            rows = app.db.execute('''
    INSERT INTO Product(name, description, price, available, seller)
    VALUES(:name, :description, :price, true, :seller)
    RETURNING id
    ''',
                                  name=name,
                                  description=description,
                                  price=price,
                                  seller = seller)
            id = rows[0][0]
            rows = app.db.execute('''
    INSERT INTO ProductInventory(product, quantity)
    VALUES(:id, :quantity)
    RETURNING product
    ''',
                                  id = id, 
                                  quantity = quantity)
            print()
            return Inventory.get(seller)

            
    #     @staticmethod
    #     def search_id(id):
    #         rows = app.db.execute('''
    # SELECT id, name, quantity, seller
    # FROM Product, ProductInventory
    # WHERE Product.id = ProductInventory.id
    #     AND Product.seller = :seller
    #     AND Product.id = :id
    # ''',
    #                               id = id)    
    #                               #not sure I understand this line   
    #         return [ProductInventory(*row) for row in rows]

    #     @staticmethod
    #     def search_prod(seller, prod):
    #         rows = app.db.execute('''
    # SELECT id, name, quantity, seller
    # FROM Product, ProductInventory
    # WHERE Product.id = ProductInventory.id
    #     AND Product.seller = :seller
    #     AND Product.name LIKE :prod
    # ''',
    #                               seller = seller,
    #                               prod = prod)       
    #         return [ProductInventory(*row) for row in rows]
