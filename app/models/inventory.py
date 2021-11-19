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
        AND ProductInventory.seller = :id
    ''',
                                  id = id) 
            print(rows)      
            return rows if rows is not None else None

        @staticmethod
        def add_prod(name, description, price, quantity, seller, url):
            rows = app.db.execute('''
    INSERT INTO Product(name, description, price, available)
    VALUES(:name, :description, :price, true)
    RETURNING id
    ''',
                                  name=name,
                                  description=description,
                                  price=price)
            id = rows[0][0]
            rows = app.db.execute('''
    INSERT INTO ProductInventory(product, seller, quantity)
    VALUES(:id, :seller, :quantity)
    RETURNING product
    ''',
                                  id = id, 
                                  seller = seller,
                                  quantity = quantity)
            rows = app.db.execute('''
    INSERT INTO ProductImage(product, url)
    VALUES(:id, :url)
    RETURNING product
    ''',
                                  id = id, 
                                  url = url)
            return Inventory.get(seller)

        @staticmethod
        def edit_inventory(prod_id, name, description, price, quantity, url, seller):
            rows = app.db.execute('''
    UPDATE Product
    SET name= :name, description= :description, price=:price, quantity = :quantity, url = :url
    WHERE id = :prod_id
    RETURNING *
    ''',
                                  prod_id = prod_id,
                                  name=name,
                                  description=description,
                                  price=price,
                                  quantity = quantity,
                                  url = url)
            rows = app.db.execute('''
    UPDATE ProductInventory
    SET quantity = :quantity
    WHERE product = :prod_id AND seller = :seller
    RETURNING *
    ''',
                                  prod_id = prod_id, 
                                  quantity = quantity,
                                  seller = seller)
            rows = app.db.execute('''
    UPDATE ProductImage
    SET url =:url
    WHERE product = :prod_id
    RETURNING *
    ''',
                                  prod_id = prod_id, 
                                  url = url)
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
